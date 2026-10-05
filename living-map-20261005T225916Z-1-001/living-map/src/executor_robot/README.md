# Executor Robot — Platform-Independent Source

Source code for the Executor Robot, structured for hardware deployment.

## Purpose

Mirrors the Webots controller logic (`simulation/webots/controllers/executor_robot/`) for deployment on physical hardware.

## Hardware Target

Same chassis and sensor suite as the Writer Robot:

| Component | Part |
|-----------|------|
| Compute | Raspberry Pi 4B (4 GB) |
| LiDAR | Slamtec RPLiDAR A1M8 (12 m, 360°, 8000 samples/s) — **mandatory** |
| IMU | Bosch BNO055 (9-DOF, I2C) — **mandatory** |
| Radio | HopeRF RFM95W 433 MHz (SX1278 LoRa, SPI) |
| Gas Sensor | Bosch BME680 — **optional** (supported if fitted) |
| Power | LiPo 5000 mAh 3S |

> **No beacon dispenser required.** The Executor does not drop new beacons but can refresh existing beacon records (re-write via ch2).

## Shared Code

Same shared libraries as Writer Robot: `beacon_codec.py`, `frame_translation.py`, `confidence.py`.

## Build / Run

```bash
# Without ROS2:
python3 src/executor_robot/executor_robot.py --config config/executor_default.yaml

# With ROS2 Humble:
colcon build --packages-select executor_robot
ros2 run executor_robot executor_robot
```
