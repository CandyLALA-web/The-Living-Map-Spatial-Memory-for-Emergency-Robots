# Hardware Design Files

Hardware design files, bill of materials, wiring diagrams, and mechanical designs.

> **PROTOTYPE STATUS:** Planned for 17–23 Nov 2026 build sprint (Sprint S4).

## System Overview

| Subsystem | Quantity | Description |
|-----------|---------|-------------|
| Writer Robot | 1 | Differential-drive explorer; LiDAR + IMU + gas sensor + beacon magazine |
| Executor Robot | 1 | Identical chassis; LiDAR + IMU; no magazine required |
| Beacon Nodes | 4+ | ESP32-S3 + LoRa 433MHz; CR2032 powered; IP54 enclosure |
| ONA Gateway | 1 | Raspberry Pi 4B + dual LoRa radios + LTE router |
| Command Post | 1 | Laptop/server (no special hardware) |

## Robot Chassis Spec

- **Drive**: 2-wheel differential drive
- **Wheelbase**: ~30 cm
- **Wheel diameter**: 65 mm
- **Max speed**: 0.5 m/s (nominal exploration: 0.2 m/s)
- **Clearance**: 50 mm (for debris field traversal)
- **Payload**: LiDAR + RPi 4B + battery + beacon magazine (Writer)

## Build Sprint Plan

| Week | Dates | Activity |
|------|-------|---------|
| S4a | 17–20 Nov | Chassis fabrication (3D print); electronics assembly; Writer wiring |
| S4b | 21–23 Nov | Executor wiring; beacon node assembly (×4); ONA gateway assembly |

## See Also

- [`bom.md`](bom.md) — Full bill of materials
- [`wiring/`](wiring/) — Wiring diagrams and schematics
- [`beacon_drop_mechanism/`](beacon_drop_mechanism/) — Servo-driven rotary magazine
