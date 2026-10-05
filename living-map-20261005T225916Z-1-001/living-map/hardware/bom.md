# Bill of Materials

> `Team [ANONYMIZED] — Phase 1 Submission | Independent Submission`
> **Prototype BOM — Sprint S4 (17–23 Nov 2026)**

All unit costs are estimates subject to change. Final costs will be recorded after procurement.

## Components

| Component | QTY | Purpose | Target Part | Unit Cost (Est.) | Notes |
|-----------|-----|---------|-------------|-----------------|-------|
| RPLiDAR A1M8 | 2 | 2D LiDAR for Writer and Executor | Slamtec A1M8 | $35.00 | 12 m range, 360°, 8000 samples/s |
| Raspberry Pi 4B | 3 | Robot controllers (×2) + ONA gateway (×1) | RPi 4B 4 GB | $35.00 | Python controller; ROS2 Humble optional |
| ESP32-S3 DevKit | 8 | Beacon MCUs (×4 deployed + 4 spare) | Espressif ESP32-S3-DevKitC-1 | $35.00 | Dual-core 240 MHz, deep sleep <10 µA |
| SX1278 LoRa Module | 12 | RF comms — robots (×4), beacons (×8), ONA (×2), spare (×2) | HopeRF RFM95W 433 MHz | $35.00 | LoRa SF7 BW125; up to 10 km LoS |
| BNO055 IMU | 2 | Orientation + gyro for dead reckoning | Bosch BNO055 breakout | $35.00 | 9-DOF; I2C; Writer + Executor |
| BME680 Gas Sensor | 1 | Gas/VOC detection on Writer | Bosch BME680 breakout | $35.00 | VOC, CO2, humidity, pressure |
| MG995 Servo | 2 | Beacon dispenser magazine (×1 Writer + 1 spare) | MG995 metal gear | $35.00 | 11 kg·cm torque; 5 V supply |
| LiPo 5000 mAh 3S | 4 | Robot power (×2 robots) + ONA gateway (×1) + spare (×1) | Generic 3S 11.1 V | $35.00 | ~30 min mission endurance per charge |
| CR2032 Coin Cell | 16 | Beacon power (×8 deployed + 8 spare) | Generic | $35.00 | 3 V, 220 mAh; target >7 days runtime |
| IP54 ABS Enclosure | 8 | Beacon weatherproofing | Hammond 1591XXCSBK | $35.00 | 90 × 36 × 25 mm; fits ESP32-S3 + RFM95W |
| LTE Router | 1 | ONA → Command Post uplink | GL.iNet GL-X750 | $35.00 | 4G LTE; failover to satellite |
| Differential Drive Chassis | 2 | Robot base (Writer + Executor) | Custom / 3D-printed | $35.00 | ~30 cm wheelbase; 65 mm wheels |
| Buck Converter (5V/3A) | 6 | Step down from 3S LiPo to RPi + sensors | LM2596 module | $35.00 | One per robot compute + ONA |
| JST Connectors + Wiring | 1 lot | Internal robot wiring | Generic | $35.00 | JST-XH 2.54 mm; various lengths |
| M3 Fasteners | 1 lot | Chassis + mount assembly | Generic stainless M3 | $35.00 | 20× M3×10, 20× M3×20, 40× nuts |
| microSD 32 GB | 3 | RPi OS + ONA SQLite store | Samsung EVO | $35.00 | One per RPi |

## Total Budget

| Line | Cost |
|------|------|
| Total estimated | .00 (Estimated BOM) |
| Procurement deadline | 03 Nov 2026 (before Sprint S4) |
