# Executor Robot Controller

**File:** `executor_robot.py`

## Implements

### ONA Briefing Reception
Received via **ch3** from ONA gateway before tunnel entry:
- Target event: `(beacon_id, event_type, GPS coords, local coords)`
- Ordered beacon route: list of `(beacon_id, heading_deg, dist_m)`
- Hazard list: `[(beacon_id, event_type, confidence, local_coords)]`
- No-go segments: `[(from_id, to_id)]`
- Mission clock T0 (for confidence age computation)

### Beacon-Guided Navigation FSM

```
FOLLOW_CHAIN → VERIFY → EXECUTE → REPORT
```

| State | Entry condition | Action | Exit condition |
|-------|----------------|--------|----------------|
| `FOLLOW_CHAIN` | Default | Drive toward beacon k using stored heading + distance; confirm by RSSI peak | RSSI peak detected (at beacon k) |
| `VERIFY` | Beacon record AGING (c 0.25–0.6) or STALE (c < 0.25) | Re-sense environment; slow down near gas | Verification complete |
| `EXECUTE` | Within 1 m of target beacon | Take measurement; write refreshed beacon record (ch2) | Measurement recorded |
| `REPORT` | Task complete or abort | Transmit result via ONA (beacon relay + ch3 uplink) | ACK from ONA |

On BLOCKED segment: mark BLOCKED in own occupancy grid, attempt alternate branch, or abort + REPORT.

### Signal-Strength Homing
The Executor drives toward increasing RSSI on ch1 to locate each beacon in the chain, compensating for accumulated odometry drift.

### Continuous Behaviours
- LiDAR local obstacle avoidance (VFH)
- Own occupancy grid construction (5 cm cells)
- Beacon record refresh: update TIMESTAMP, CONFIDENCE, clear STALE events
- New event detection (extends living map dynamically)

### Hardware
Same chassis as Writer Robot. Sensors: 2D LiDAR, IMU, wheel encoders, LoRa radio (ch1 + ch3). Gas sensor optional but supported.
