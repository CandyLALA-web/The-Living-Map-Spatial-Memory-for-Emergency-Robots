# Controllers

Each robot controller lives in its own subfolder **named identically to the controller** — this is a Webots requirement.

## Structure

```
controllers/
 writer_robot/
 writer_robot.py # Main controller
 writer_robot.json # Optional config (start pose, beacon budget, etc.)
 executor_robot/
 executor_robot.py
 executor_robot.json
 outside_network/
 outside_network.py
 outside_network.json
```

## Controllers

| Controller | Robot | Description |
|-----------|-------|-------------|
| `writer_robot` | Writer Robot | LiDAR mapping, frontier exploration, FSM, event detection, beacon drop |
| `executor_robot` | Executor Robot | ONA briefing reception, chain-following FSM, report transmission |
| `outside_network` | ONA Gateway | ch1 listener, CRC validation, frame translation, store-and-forward, ch3 briefing |

## Supervisor

A `supervisor` controller (not listed as a robot controller) manages the episode lifecycle, injects events, records ground-truth metrics, and handles batch runs.

## Shared Libraries

Common code is in `../libraries/` and imported by all controllers:
- `beacon_codec.py`
- `frame_translation.py`
- `confidence.py`
