# Experiment Configuration Files

Place YAML configuration files for world parameters and batch experiments here.

## Expected Files

### `experiment_default.yaml`

```yaml
# Living Map — Default Experiment Configuration

# Robot start poses (local frame, metres)
writer_start: [0.0, 0.0, 0.0] # [x, y, heading_deg]
executor_start: [0.0, 0.5, 0.0] # parked beside ONA gateway

# Beacon budget
beacon_budget: 8 # Total beacons Writer carries
event_reserve: 2 # Last N beacons reserved for events

# Event locations (local frame, metres)
events:
 - type: GAS_LEAK
 position: [42.0, -1.5]
 severity: 1 # 0=trace, 1=moderate, 2=severe
 - type: BLOCKED_PASSAGE
 position: [28.0, 0.0]
 width: 0.3 # Remaining clear width (m)

# ONA anchor (geodetic)
ona_anchor:
 lat0_deg: 36.8065
 lon0_deg: 10.1815
 h0_m: 120.0
 psi_deg: 30.0 # Tunnel bearing (clockwise from true north)

# Simulated uplink parameters
uplink:
 latency_s: 2.0
 loss_rate: 0.10 # Fraction of packets dropped

# Batch evaluation
N_runs: 20
random_seed_base: 42 # Seeds: 42, 43, ... 61

# Confidence aging
tau_s: 3600 # Half-life in seconds (1 hour)
```
