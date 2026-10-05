"""Living Map - Outside Network Area (ONA).

Pipeline: raw frame -> decode + CRC -> dedup -> translate to GPS -> outbox (SQLite)
-> uplink (memory simulation or MQTT). The outbox gives store-and-forward.
"""
import json
import math
import sqlite3

from beacon import Beacon, confidence, trust_level
from frame_translation import Anchor, gps_to_local, local_to_gps, sigma_m


class MemoryUplink:
    """Simulated uplink. Set online=False to simulate an outage."""

    def __init__(self):
        self.online = True
        self.sent = []

    def publish(self, topic: str, payload: str) -> bool:
        if not self.online:
            return False
        self.sent.append((topic, payload))
        return True


class MqttUplink:
    """Real uplink to an MQTT broker (needs: pip install paho-mqtt)."""

    def __init__(self, host: str = "localhost", port: int = 1883):
        import paho.mqtt.client as mqtt
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.connect_async(host, port)   # retries by itself if broker is down
        self.client.loop_start()

    def publish(self, topic: str, payload: str) -> bool:
        try:
            info = self.client.publish(topic, payload, qos=1)
            if info.rc != 0:
                return False
            info.wait_for_publish(timeout=2)
            return info.is_published()
        except Exception:
            return False


class ONA:
    def __init__(self, anchor: Anchor, mission_id: int = 0, uplink=None,
                 db_path: str = ":memory:"):
        self.anchor = anchor
        self.mission_id = mission_id
        self.uplink = uplink or MemoryUplink()
        self.db = sqlite3.connect(db_path)
        self.db.executescript("""
            CREATE TABLE IF NOT EXISTS seen(
                beacon_id INTEGER, mission_id INTEGER, t INTEGER, state INTEGER,
                PRIMARY KEY(beacon_id, mission_id));
            CREATE TABLE IF NOT EXISTS outbox(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT, payload TEXT, sent INTEGER DEFAULT 0);
        """)
        self.stats = {"ok": 0, "corrupt": 0, "duplicate": 0, "wrong_mission": 0}

    # ---- inbound: Writer / Executor reports -------------------------------
    def handle_frame(self, raw: bytes, now_s: int) -> str:
        try:
            b = Beacon.decode(raw)
        except ValueError:
            self.stats["corrupt"] += 1
            return "corrupt"
        if b.mission_id != self.mission_id:
            self.stats["wrong_mission"] += 1
            return "wrong_mission"

        row = self.db.execute(
            "SELECT t, state FROM seen WHERE beacon_id=? AND mission_id=?",
            (b.beacon_id, b.mission_id)).fetchone()
        newer = row is None or (b.t_written_s, int(b.state)) > (row[0], row[1])
        if not newer:
            self.stats["duplicate"] += 1
            return "duplicate"

        x_m, y_m = b.x_cm / 100, b.y_cm / 100
        lat, lon = local_to_gps(x_m, y_m, self.anchor)
        dist = math.hypot(x_m, y_m)
        conf = confidence(b, now_s)
        event = {
            "mission_id": b.mission_id, "beacon_id": b.beacon_id,
            "type": b.etype.name, "severity": b.severity, "state": b.state.name,
            "x_cm": b.x_cm, "y_cm": b.y_cm,
            "lat": round(lat, 7), "lon": round(lon, 7),
            # path length is unknown here: assume 1.5x the straight distance
            "sigma_m": round(sigma_m(dist * 1.5, dist), 2),
            "t_written_s": b.t_written_s,
            "confidence": round(conf, 3), "trust": trust_level(conf),
        }
        self.db.execute("INSERT OR REPLACE INTO seen VALUES (?,?,?,?)",
                        (b.beacon_id, b.mission_id, b.t_written_s, int(b.state)))
        self.db.execute("INSERT INTO outbox(topic, payload) VALUES (?,?)",
                        (f"livingmap/{self.mission_id}/events", json.dumps(event)))
        self.db.commit()
        self.stats["ok"] += 1
        self.flush()
        return "ok"

    # ---- outbound: store-and-forward ---------------------------------------
    def flush(self) -> int:
        """Send queued messages in order. Stops at the first failure."""
        sent = 0
        rows = self.db.execute(
            "SELECT id, topic, payload FROM outbox WHERE sent=0 ORDER BY id").fetchall()
        for id_, topic, payload in rows:
            if not self.uplink.publish(topic, payload):
                break
            self.db.execute("UPDATE outbox SET sent=1 WHERE id=?", (id_,))
            sent += 1
        self.db.commit()
        return sent

    def pending(self) -> int:
        return self.db.execute("SELECT COUNT(*) FROM outbox WHERE sent=0").fetchone()[0]

    # ---- briefing: command post (GPS) -> Executor (Writer frame) -----------
    def make_briefing(self, mission: dict) -> dict:
        def to_local(p: dict) -> dict:
            x, y = gps_to_local(p["lat"], p["lon"], self.anchor)
            return {"beacon_id": p.get("beacon_id"),
                    "x_cm": round(x * 100), "y_cm": round(y * 100)}
        return {
            "mission_id": self.mission_id,
            "target": to_local(mission["target"]),
            "hazards": [to_local(h) for h in mission.get("hazards", [])],
            "timeout_s": mission.get("timeout_s", 900),
            "clock_epoch_s": mission.get("clock_epoch_s", 0),
            "safe_temp_c": mission.get("safe_temp_c", 60),
        }


if __name__ == "__main__":
    from beacon import EventType, State

    up = MemoryUplink()
    ona = ONA(Anchor(36.8430, 10.1950, 30.0), uplink=up)
    fire = Beacon(5, 4, 6, EventType.FIRE, 3, State.DETECTED, 420, 150, 90, 720)
    raw = fire.encode()
    print("valid     ->", ona.handle_frame(raw, 800))
    print("duplicate ->", ona.handle_frame(raw, 810))
    bad = bytearray(raw); bad[5] ^= 0xFF
    print("corrupted ->", ona.handle_frame(bytes(bad), 820))
    up.online = False
    victim = Beacon(8, 7, 0, EventType.VICTIM, 5, State.DETECTED, 900, -200, 0, 900)
    print("offline   ->", ona.handle_frame(victim.encode(), 950), "| pending:", ona.pending())
    up.online = True
    print("flushed   ->", ona.flush(), "| pending:", ona.pending())
    for topic, payload in up.sent:
        print(topic, payload)
    print("stats:", ona.stats)