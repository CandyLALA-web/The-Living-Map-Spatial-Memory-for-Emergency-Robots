# Outside Network Area (ONA) Gateway Controller

**File:** `outside_network.py`

## Implements

### ch1 Listener
- Receives beacon broadcast frames (LoRa 433 MHz, ch1) from all beacons in range of tunnel entrance
- Validates **CRC-16/CCITT-FALSE** over bytes 0–13
- **De-duplicates** by `(beacon_id, timestamp)` — discards exact retransmissions

### Confidence Aging
Computes current confidence from stored beacon confidence and elapsed time:
```
c_now = c_write * 2^(-(t_now - T_write) / τ)
```
where τ = 3600 s (1-hour half-life, configurable).

Classification:
- `FRESH`: c ≥ 0.6
- `AGING`: 0.25 ≤ c < 0.6
- `STALE`: c < 0.25

### Local-to-GPS Frame Translation
Uses `frame_translation.py` from `../libraries/`. Anchor parameters (lat0, lon0, h0, ψ) loaded from `../config/experiment_default.yaml`.

### Store-and-Forward Queue
- **SQLite-backed** persistent queue (survives gateway reboots)
- Each record carries a sequence number
- Delivery confirmed by **ACK** from Command Post (TCP)
- Unacknowledged messages retried with **exponential backoff**: 2 s, 4 s, 8 s … max 120 s
- Queue depth monitored; dashboard shows warning if depth > 50 records

### Simulated Uplink
In Webots, a TCP socket with configurable latency and packet-loss rate is provided by the Supervisor:
```bash
python command_post/server.py --latency 2.0 --loss 0.1
```

### Executor Briefing Dispatch
On receiving a mission packet from the Command Post, the ONA gateway:
1. Validates and de-serialises the briefing JSON
2. Encodes it into a ch3 transmission packet
3. Broadcasts on **ch3** when Executor is within range at tunnel entrance
4. Awaits ACK from Executor controller before clearing the queue entry
