# Simulation Results

Simulation outputs are written here by the Supervisor controller. **This directory is NOT committed to git** (excluded by `.gitignore`). Results are generated locally by running the Webots world.

## How to Reproduce Results

```bash
# Standard run
webots simulation/webots/worlds/living_map_tunnel.wbt

# Headless batch run (N=20 episodes)
webots --batch --mode=fast --world=simulation/webots/worlds/living_map_tunnel.wbt
```

The Supervisor will write results to this directory after each episode.

## Expected Output Files

| File | Format | Contents |
|------|--------|---------|
| `supervisor_ground_truth.json` | JSON (per run) | True beacon positions, event timestamps, Writer path |
| `beacon_records.json` | JSON | All beacon frames received by ONA during the run |
| `ona_forwarded.json` | JSON | Records forwarded to Command Post with timestamps |
| `command_post_events.json` | JSON | Event database snapshot at mission end |
| `executor_mission.json` | JSON | Executor route, timing, verification results |
| `map_coverage_iou.csv` | CSV | IoU per episode (Writer map vs. ground truth) |
| `beacon_position_errors.csv` | CSV | RMS beacon GPS error per episode |
| `event_latency.csv` | CSV | Event-to-dashboard latency (s) per episode |
| `mission_success_rate.csv` | CSV | Executor mission success/failure per episode |

## Expected Metrics

See [`../../results/metrics.md`](../../results/metrics.md) for targets and current status.
