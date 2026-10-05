# Webots Simulation

> `Team [ANONYMIZED] — Phase 1 Submission | Independent Submission`

**Webots is the ONLY simulator used in this project.** No Gazebo, ROS, Unity, or Isaac Sim.

---

## Folder Structure

```
simulation/webots/
 worlds/ # Webots world files (*.wbt)
 controllers/ # Robot controller programs (one subfolder per controller)
 writer_robot/
 executor_robot/
 outside_network/
 protos/ # Custom PROTO node definitions
 plugins/ # Physics and radio plugins
 libraries/ # Shared Python libraries (beacon_codec, frame_translation, confidence)
 resources/ # Meshes, textures, and maps
 config/ # Experiment configuration YAML files
 results/ # Simulation outputs (not committed to git)
```

---

## Required Webots Version

**Webots R2023b or later.**
Download from: https://cyberbotics.com

---

## Opening the World

1. Launch Webots.
2. `File → Open World…` → navigate to `simulation/webots/worlds/living_map_tunnel.wbt`.
3. Press **Play ()**. The Supervisor controller starts all sub-controllers automatically.
4. Logs and metrics are written to `simulation/webots/results/`.

> **Note:** The world file `living_map_tunnel.wbt` is prepared for simulation execution.

---

## RF Channel Assignments

| Channel | Direction | Purpose |
|---------|-----------|---------|
| **ch1** | Broadcast (beacons → all) | Beacon record broadcast every 2 s; gossip relay |
| **ch2** | Writer → Beacon | Writer programs a beacon node at drop time (initial frame write) |
| **ch3** | ONA ↔ Executor | ONA briefs Executor before entry; Executor sends reports back via ONA |

All channels simulate LoRa 433 MHz with a maximum range of **6 m** in the tunnel environment (modelled by the radio propagation plugin).

---

## Running Headless (Batch Evaluation)

```bash
webots --batch --mode=fast --world=simulation/webots/worlds/living_map_tunnel.wbt
```

The Supervisor will run `N_runs` (default 20) episodes automatically and write metrics to `simulation/webots/results/`.

---

## See Also

- [`worlds/README.md`](worlds/README.md)
- [`controllers/README.md`](controllers/README.md)
- [`protos/README.md`](protos/README.md)
- [`plugins/README.md`](plugins/README.md)
- [`libraries/README.md`](libraries/README.md)
- [`config/README.md`](config/README.md)
- [`results/README.md`](results/README.md)
