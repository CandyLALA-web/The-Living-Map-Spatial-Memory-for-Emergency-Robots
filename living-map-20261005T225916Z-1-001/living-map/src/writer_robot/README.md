# Writer Robot — Platform-Independent Source

Source code for the Writer Robot, structured for hardware deployment.

## Purpose

Mirrors the Webots controller logic (`simulation/webots/controllers/writer_robot/`) for deployment on physical hardware. Designed to run with or without a ROS2 layer.

## Hardware Target

| Component | Part |
|-----------|------|
| Compute | Raspberry Pi 4B (4 GB) |
| LiDAR | Slamtec RPLiDAR A1M8 (12 m, 360°, 8000 samples/s) |
| IMU | Bosch BNO055 (9-DOF, I2C) |
| Gas Sensor | Bosch BME680 (VOC, CO2, humidity, pressure) |
| Radio | HopeRF RFM95W 433 MHz (SX1278 LoRa, SPI) |
| Beacon Dispenser | MG995 servo + 8-slot rotary magazine |
| Power | LiPo 5000 mAh 3S |
| Middleware | ROS2 Humble (optional) |

## Shared Code

The libraries `beacon_codec.py`, `frame_translation.py`, and `confidence.py` from `simulation/webots/libraries/` are symlinked or copied here for hardware use. Any changes to shared logic must be kept in sync.

## Build / Run

```bash
# Without ROS2:
python3 src/writer_robot/writer_robot.py --config config/writer_default.yaml

# With ROS2 Humble:
colcon build --packages-select writer_robot
ros2 run writer_robot writer_robot
```
