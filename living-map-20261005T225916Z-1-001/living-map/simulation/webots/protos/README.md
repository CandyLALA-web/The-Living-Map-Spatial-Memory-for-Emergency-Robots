# Custom PROTO Files

Place custom Webots PROTO node definitions here.

## Expected Files

### `WriterRobot.proto`
Differential-drive ground robot for tunnel exploration:
- **Drive**: 2-wheel differential drive, ~30 cm wheelbase
- **LiDAR**: 2D, 360°, 12 m range (5760 samples/scan) — Webots `DistanceSensor` array or `Lidar` node
- **IMU**: `InertialUnit` node (heading, pitch, roll)
- **Wheel Encoders**: `PositionSensor` on each drive motor
- **Beacon Dispenser**: `Servo`-driven rotary magazine, 8-slot
- **RF**: `Emitter`/`Receiver` pair on **ch1** (beacon receive) + `Emitter`/`Receiver` pair on **ch2** (beacon write)

### `ExecutorRobot.proto`
Same chassis as WriterRobot:
- Identical drive, LiDAR, IMU, encoders
- **RF**: `Emitter`/`Receiver` on **ch1** (beacon receive) + `Emitter`/`Receiver` on **ch3** (ONA briefing/reporting)
- No beacon dispenser required (but stub slot present for hardware parity)

### `Beacon.proto`
Stationary node dropped by Writer onto tunnel floor:
- **RF**: `Emitter`/`Receiver` on **ch1** (broadcast) + `Emitter`/`Receiver` on **ch2** (receive write commands)
- `LED` node (status indicator — green=FRESH, yellow=AGING, red=STALE, blue=LOW_BATTERY)
- Battery monitor: `supervisor`-managed countdown; sets `LOW_BATTERY` flag when < 20%

## PROTO Naming Convention

```
<RobotName>.proto # PascalCase, must match node type name inside PROTO
```
