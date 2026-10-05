"""Living Map - beacon message codec (15 bytes, little-endian)."""
import struct
from dataclasses import dataclass
from enum import IntEnum

# Layout: id, prev, next, type<<4|sev, ver<<2|state, x, y, heading, ts, mission, crc16
_BODY = "<BBBBBhhBHB"          # 13 bytes
_FULL = _BODY + "H"            # 15 bytes
SIZE = struct.calcsize(_FULL)
VERSION = 1
TS_UNIT_S = 10                 # timestamp unit: 10 s (uint16 -> ~7.5 days)


class EventType(IntEnum):
    ANCHOR = 0
    FIRE = 1
    VICTIM = 2
    SMOKE = 3
    BLOCKED = 4
    INTERSECTION = 5
    EXIT = 6


class State(IntEnum):
    DETECTED = 0
    TREATED = 1
    ASSISTED = 2
    EXPIRED = 3


# Half-life per event type, in seconds
HALF_LIFE_S = {
    EventType.FIRE: 180, EventType.SMOKE: 600, EventType.VICTIM: 3600,
    EventType.BLOCKED: 7200, EventType.INTERSECTION: 10**6,
    EventType.EXIT: 10**6, EventType.ANCHOR: 10**6,
}


def crc16_ccitt(data: bytes, crc: int = 0xFFFF) -> int:
    for b in data:
        crc ^= b << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) & 0xFFFF if crc & 0x8000 else (crc << 1) & 0xFFFF
    return crc


@dataclass
class Beacon:
    beacon_id: int
    prev_id: int
    next_id: int
    etype: EventType
    severity: int          # 0-15
    state: State
    x_cm: int              # Writer private frame
    y_cm: int
    heading_deg: float     # direction to next beacon
    t_written_s: int       # mission clock, seconds
    mission_id: int = 0

    def encode(self) -> bytes:
        body = struct.pack(
            _BODY, self.beacon_id, self.prev_id, self.next_id,
            (int(self.etype) << 4) | (self.severity & 0xF),
            (VERSION << 2) | int(self.state),
            self.x_cm, self.y_cm,
            round(self.heading_deg % 360 * 256 / 360) & 0xFF,
            (self.t_written_s // TS_UNIT_S) & 0xFFFF,
            self.mission_id,
        )
        return body + struct.pack("<H", crc16_ccitt(body))

    @classmethod
    def decode(cls, raw: bytes) -> "Beacon":
        if len(raw) != SIZE:
            raise ValueError(f"bad length {len(raw)}")
        if crc16_ccitt(raw[:-2]) != struct.unpack("<H", raw[-2:])[0]:
            raise ValueError("CRC mismatch")
        bid, prev, nxt, ts_, vs, x, y, hd, ts, mid, _ = struct.unpack(_FULL, raw)
        return cls(bid, prev, nxt, EventType(ts_ >> 4), ts_ & 0xF,
                   State(vs & 0x3), x, y, hd * 360 / 256, ts * TS_UNIT_S, mid)


def confidence(b: Beacon, now_s: int) -> float:
    """0..1, exponential decay with a per-type half-life."""
    age = max(0, now_s - b.t_written_s)
    return 0.5 ** (age / HALF_LIFE_S[b.etype])


def trust_level(c: float) -> str:
    return "TRUST" if c > 0.7 else "REVERIFY" if c >= 0.3 else "OBSOLETE"


if __name__ == "__main__":
    fire = Beacon(5, 4, 6, EventType.FIRE, 3, State.DETECTED, 420, 150, 90, 720)
    raw = fire.encode()
    print(len(raw), "bytes:", raw.hex(" "))
    back = Beacon.decode(raw)
    print(back)
    for age in (0, 180, 600):
        c = confidence(back, back.t_written_s + age)
        print(f"age {age:>4}s -> confidence {c:.2f} -> {trust_level(c)}")
    corrupted = bytearray(raw); corrupted[5] ^= 0xFF
    try:
        Beacon.decode(bytes(corrupted))
    except ValueError as e:
        print("corruption detected:", e)