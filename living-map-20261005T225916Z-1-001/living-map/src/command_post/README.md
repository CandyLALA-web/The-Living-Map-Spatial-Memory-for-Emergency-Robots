# Command Post — Dashboard and Mission Planner

Remote operations hub software for the Command Post.

## Hardware Target

Any laptop or server with Python 3.10+ and network connectivity (LTE or satellite uplink from ONA gateway).

## Role

The Command Post has **no direct link** to any robot. All data arrives through the ONA gateway uplink. All commands are dispatched through the ONA gateway.

## Components

### Ingestion Server
- **TCP listener** receiving forwarded beacon records from ONA uplink
- Validates sequence numbers, sends ACKs
- Writes records to SQLite event database

### Event Database
- **SQLite** table: `events (beacon_id, event_type, timestamp, local_x, local_y, gps_lat, gps_lon, gps_alt, confidence, flags, received_at)`
- Keyed by `(beacon_id, timestamp)` for de-duplication
- Auto-aging: confidence recomputed on every read

### Live Map
- GPS-coordinate map (latitude/longitude) rendered in browser (Leaflet.js) or desktop (Matplotlib + cartopy)
- Beacon events shown with icons: = GAS_LEAK, = BLOCKED_PASSAGE, • = breadcrumb
- Opacity proportional to current confidence `c` (fully opaque = FRESH, faded = AGING, strikethrough = STALE)
- Uncertainty circle of radius σ(s) = 0.3 + 0.02·s drawn around each event
- Data age shown in tooltip (hover)
- Auto-refresh every **5 s** from event database

### Mission Planner
- Operator selects target event from live map
- System generates beacon chain route (nearest-neighbour ordering by local distance)
- Flags hazards and no-go segments in route
- Packages mission briefing JSON

### Briefing Builder
Mission packet format:
```json
{
 "target": {"beacon_id": 3, "event_type": "GAS_LEAK", "gps": [36.80682, 10.18175, 120.0]},
 "route": [{"beacon_id": 1, "heading_deg": 32.1, "dist_m": 12.4}, {"beacon_id": 2, "heading_deg": 31.8, "dist_m": 13.1}],
 "hazards": [{"beacon_id": 3, "event": "GAS_LEAK", "confidence": 0.82}],
 "no_go": [],
 "T0_utc": "2026-11-15T09:00:00Z"
}
```
Transmitted to ONA gateway via TCP; ONA forwards to Executor on ch3.

## Run

```bash
# Start Command Post server (ingestion + mission planner + live map)
python3 src/command_post/server.py --host 0.0.0.0 --port 9000

# Simulation mode (inject latency/loss for testing)
python3 src/command_post/server.py --latency 2.0 --loss 0.1
```

Open live map at: `http://localhost:9000/map`
