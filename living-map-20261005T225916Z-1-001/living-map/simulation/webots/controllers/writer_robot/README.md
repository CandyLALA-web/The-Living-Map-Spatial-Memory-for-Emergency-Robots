# Writer Robot Controller

**File:** `writer_robot.py`

## Implements

### 2D Occupancy Grid Mapping
- Grid resolution: **5 cm cells**
- Update rule: **log-odds** (p_occ=0.7, p_free=0.3)
- Map size: auto-expanding up to 200 m × 10 m tunnel extent

### Frontier-Based Exploration
- Frontier detection: BFS on free/unknown boundary cells
- Path planning: **A\*** on occupancy grid (4-connected or 8-connected)
- Local obstacle avoidance: Vector Field Histogram (VFH)
- Fallback: **wall-following** in long featureless corridors

### FSM

```
IDLE → EXPLORE → INVESTIGATE → DEPLOY → EXPLORE (loop) → RETURN → IDLE
```

| State | Entry condition | Action | Exit condition |
|-------|----------------|--------|----------------|
| IDLE | Start / mission reset | Wait for GO command | GO received |
| EXPLORE | Default | A* to next frontier; build map | Event detected or budget milestone |
| INVESTIGATE | Event candidate detected | Slow approach; confirm sensor reading | Confirmed / false positive |
| DEPLOY | Event confirmed OR drop policy triggered | Halt; write beacon frame (ch2); drop beacon | Beacon acknowledged by supervisor |
| RETURN | Map complete OR budget exhausted | A* back to entrance | Entrance reached |

### Event Detection

| Event | Trigger | Sensor |
|-------|---------|--------|
| `GAS_LEAK` | Gas concentration > threshold (c > 0.15) | Virtual gas sensor (supervisor-fed channel); BME680 in hardware |
| `BLOCKED_PASSAGE` | LiDAR scan shows occupied cells in previously-free map segment (grid diff > 3 consecutive cells) | LiDAR DistanceSensor array |

### Beacon Drop Policy
1. **Event beacon** — on first detection or severity upgrade
2. **Link-keeping beacon** — when last beacon RSSI falls to ~70% of range (≈ 4.2 m from last beacon)
3. **Junction beacon** — at every tunnel fork
4. **Budget**: 8 beacons total; last 2 reserved for events

### Dead-Reckoning Pose Estimation
- Integrate wheel encoder odometry + IMU gyro heading
- Uncertainty: σ grows at **0.02 m per metre** of travel
- Re-anchor: reset σ to 0.05 m when passing a known beacon (signal-strength peak = known position)
