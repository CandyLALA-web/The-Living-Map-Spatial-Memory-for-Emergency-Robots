# Outside Network Area (ONA) Gateway — Platform-Independent Source

Gateway software for the ONA node at the tunnel entrance.

## Hardware Target

| Component | Part |
|-----------|------|
| Compute | Raspberry Pi 4B (4 GB) |
| RF (ch1) | HopeRF RFM95W 433 MHz (SX1278 LoRa, SPI) — listener |
| RF (ch3) | Second RFM95W 433 MHz — Executor briefing |
| Uplink | GL.iNet GL-X750 LTE router (primary); satellite modem (fallback) |
| Storage | 32 GB microSD (store-and-forward SQLite queue) |

## Implements

### ch1 RF Listener
Continuously receives beacon frames from all beacons within ~6 m of tunnel entrance on 433 MHz LoRa ch1.

### CRC-16 Validation + De-duplication
- Drop frames with CRC mismatch
- De-duplicate by `(beacon_id, timestamp)` — keep first, discard repeats
- Log all accepted frames to SQLite with reception timestamp

### Confidence Aging Computation
All stored beacon records are aged using: `c_now = c_write · 2^(-(t_now - T_write) / τ)`

### Local-to-GPS Frame Translation
Uses `frame_translation.py` shared library. Anchor loaded from config file at startup.

### Store-and-Forward Queue
- **SQLite-backed**: all outbound records survive power-cycles
- Sequence-numbered delivery; ACK required from Command Post
- Exponential backoff retry: 2 s → 4 s → 8 s → … max 120 s
- Queue depth alert logged if > 50 pending records
- Uplink via TCP socket to Command Post (LTE primary, satellite fallback)

### Mission Briefing Dispatch
On receiving a mission packet from Command Post via TCP uplink:
1. Validate and deserialise JSON
2. Queue as ch3 priority transmission
3. Broadcast on ch3 when Executor is within range (RSSI threshold met)
4. Await Executor ACK; retry if no ACK within 10 s (max 3 retries)

## Run

```bash
python3 src/outside_network/ona_gateway.py --config config/ona_default.yaml
```
