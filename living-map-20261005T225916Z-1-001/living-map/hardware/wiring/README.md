# Wiring Diagrams and PCB Schematics

> **PENDING** — To be produced during Sprint S4 hardware build (17–23 Nov 2026).

## Expected Files

| File | Format | Contents |
|------|--------|---------|
| `writer_robot_wiring.pdf` | PDF | Full wiring diagram: RPi 4B → RPLiDAR A1M8, BNO055 IMU, BME680 gas sensor, RFM95W LoRa (SPI), MG995 servo, LiPo + buck converter, wheel encoder connections |
| `executor_robot_wiring.pdf` | PDF | Same as Writer minus gas sensor and servo magazine |
| `ona_gateway_wiring.pdf` | PDF | RPi 4B → dual RFM95W LoRa (ch1 + ch3), GL.iNet LTE router (Ethernet), LiPo power |
| `beacon_node_schematic.pdf` | PDF | ESP32-S3 → RFM95W LoRa (SPI), CR2032 battery, LED indicators, I2C pads |

## Wiring Notes (Preliminary)

### SPI Bus (RPi 4B → RFM95W)
- MOSI: GPIO 10 (SPI0_MOSI)
- MISO: GPIO 9 (SPI0_MISO)
- SCLK: GPIO 11 (SPI0_SCLK)
- CS ch1: GPIO 8 (SPI0_CE0)
- CS ch3 (ONA only): GPIO 7 (SPI0_CE1)
- DIO0 (interrupt): GPIO 25

### I2C Bus (RPi 4B → BNO055 + BME680)
- SDA: GPIO 2
- SCL: GPIO 3
- BNO055 address: 0x28 (ADR pin low)
- BME680 address: 0x76 (SDO pin low)

### RPLiDAR (USB)
- USB UART adapter → RPi USB port
- Driver: `rplidar` Python package

### MG995 Servo (Writer)
- Signal: GPIO 18 (PWM)
- Power: 5 V from dedicated buck converter (NOT from RPi 5 V pin)
