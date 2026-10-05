# Shared Controller Libraries

Shared Python libraries imported by all Webots controllers. Place library files here.

## Expected Libraries

### `beacon_codec.py`
Encode and decode the 16-byte beacon frame:
- `encode_frame(type, flags, timestamp, beacon_id, confidence, local_x, local_y, local_theta, frame_id, ttl) → bytes[16]`
- `decode_frame(data: bytes) → dict`
- `compute_crc16(data: bytes[0:14]) → int` — CRC-16/CCITT-FALSE polynomial 0x1021
- `validate_frame(data: bytes) → bool` — checks length and CRC

### `frame_translation.py`
Local ↔ GPS coordinate transforms:
- `local_to_gps(x, y, z, lat0, lon0, h0, psi_deg) → (lat, lon, alt)`
- `gps_to_local(lat, lon, alt, lat0, lon0, h0, psi_deg) → (x, y, z)`
- `position_uncertainty(path_length_m) → float` — σ = 0.3 + 0.02·s

### `confidence.py`
Confidence aging utilities:
- `age_confidence(c_write, t_write, t_now, tau=3600) → float` — c = c_write · 2^(-(t-T)/τ)
- `classify_confidence(c) → str` — returns `'FRESH'`, `'AGING'`, or `'STALE'`
- `encode_confidence(c_float) → int` — maps [0.0, 1.0] → [0, 255]
- `decode_confidence(c_byte) → float` — maps [0, 255] → [0.0, 1.0]

## Usage in Controllers

```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../libraries'))
from beacon_codec import encode_frame, decode_frame, validate_frame
from frame_translation import local_to_gps
from confidence import age_confidence, classify_confidence
```
