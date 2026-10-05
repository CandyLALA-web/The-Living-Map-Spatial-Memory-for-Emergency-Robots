# Beacon Firmware and Codec

Beacon firmware and the shared 16-byte codec library.

## MCU Target

| Component | Part |
|-----------|------|
| MCU | Espressif ESP32-S3 (dual-core 240 MHz, Wi-Fi/BT, deep sleep < 10 µA) |
| Radio | HopeRF RFM95W 433 MHz (SX1278 LoRa, SPI) |
| Battery | CR2032 (3 V, 220 mAh) |
| Enclosure | 90 × 36 × 25 mm ABS, IP54 target |

## Implements

### 16-byte Frame Encode/Decode
See `beacon_codec.py` in `simulation/webots/libraries/` for the canonical implementation. Firmware mirrors this in C/MicroPython.

### CRC-16
CRC-16/CCITT-FALSE (polynomial 0x1021, init 0xFFFF) over bytes 0–13.

### ch1 Broadcast
Every **2 s ± 0–500 ms** random jitter (ALOHA-style collision avoidance). Duty cycle < 3% (13 ms airtime per frame at SF7 BW125).

### ch2 Write Reception
Listens for a write command from the Writer Robot. On valid CRC, stores the received frame as the beacon's primary record.

### Gossip Relay
Periodically relays the **3 freshest neighbour records** (by confidence) heard on ch1, with `TTL` field decremented by 1. Records with TTL = 0 are not relayed. `RELAY` flag set in byte 0.

### Confidence Aging
On each broadcast, recomputes current confidence: `c_now = c_write · 2^(-(t-T)/τ)`. If `c_now < 0.25` (STALE), marks record for erasure after 3 more broadcasts.

### Low-Battery Flag
Battery voltage monitored via ADC. Sets `LOW_BATTERY` flag in frame byte 0 when V < 2.4 V (≈ 20% CR2032 capacity).

## Target Battery Life

- Broadcast: 13 ms × 0.5 × 30 mA = 0.195 mJ per frame
- At 1 frame / 2 s: ~0.1 mJ/s average active energy
- Deep sleep between broadcasts: ~10 µA × 3 V × 1.987 s ≈ 0.060 mJ/s
- Total: ~0.16 mJ/s → 220 mAh × 3 V × 3600 / (0.16 × 10^-3) ≈ **14 days** (theoretical)
- Target (with margin): **> 7 days**
