# The Living Map: Spatial Memory for Emergency Robots

> **IEEE RAS × IEEE AESS Tunisia Section — TSYP14 Technical Challenge, Phase 1**
> `Team [ANONYMIZED] — Phase 1 Submission | Independent Submission`

---

## Summary

The Living Map is a distributed spatial-memory system for GPS-denied mine tunnel search-and-rescue. A **Writer Robot** autonomously explores the tunnel, building a 2D occupancy-grid map with a LiDAR-based frontier planner, and physically depositing battery-powered RF beacon nodes at junctions, hazard sites, and link-keeping waypoints. Each beacon stores a **16-byte signed frame** (event type, local coordinates, confidence, CRC-16) and re-broadcasts it every 2 s on LoRa 433 MHz. An **Outside Network Area (ONA) Gateway** at the tunnel entrance listens on ch1, validates frames, ages confidence values, translates local coordinates to WGS-84 GPS, and forwards records via store-and-forward uplink to a remote **Command Post**, which maintains a live operational map. When the Command Post dispatches a mission, the ONA briefs an **Executor Robot** via ch3 with a pre-loaded beacon route, hazard list, and mission target — enabling fully autonomous, informed navigation through a zone the Executor has never entered.

**Chosen Environment:** Mines / Tunnels

---

## Architecture

See interactive architecture presentation at [`docs/architecture/d1-system-architecture.html`](docs/architecture/d1-system-architecture.html) or the complete gallery at [`docs/architecture/all-diagrams-viewer.html`](docs/architecture/all-diagrams-viewer.html).

---

## Demo

Simulation world and controller baseline established in `simulation/webots/` for Phase 2 implementation.

---

## Opening the Webots Simulation

1. Install **Webots R2023b** or later from [cyberbotics.com](https://cyberbotics.com).
2. Open the world file:
 ```
 simulation/webots/worlds/living_map_tunnel.wbt
 ```
3. Press **Play**. The Supervisor controller starts automatically and writes logs to `simulation/webots/results/`.
4. See [`simulation/webots/README.md`](simulation/webots/README.md) for full instructions.

---

## Repository Map

| Path | Purpose |
|------|---------|
| `simulation/webots/` | **Webots-only** simulation (worlds, controllers, PROTOs, plugins) |
| `src/` | Platform-independent source code (mirrors controllers for hardware) |
| `hardware/` | Bill of materials, wiring diagrams, beacon drop mechanism |
| `docs/` | Technical report, design references, architecture diagrams |
| `tests/` | Unit and integration test suite |
| `results/` | Simulation outputs (not committed — generated locally) |

---

## Phase 1 Deliverable Index

| Deliverable | File |
|-------------|------|
| Technical Report (PDF, <=6 pp.) | [`docs/technical-report.pdf`](docs/technical-report.pdf) |
| Implementation Plan (PDF) | [`docs/implementation-plan.pdf`](docs/implementation-plan.pdf) |
| Failure Modes Analysis FMECA (PDF) | [`docs/failure-cases.pdf`](docs/failure-cases.pdf) |
| Architecture Diagrams Suite (Interactive HTML) | [`docs/architecture/all-diagrams-viewer.html`](docs/architecture/all-diagrams-viewer.html) |
| Simulation World & Controllers | [`simulation/webots/`](simulation/webots/) |
| Bill of Materials | [`hardware/bom.md`](hardware/bom.md) |
| Validation Metrics | [`results/metrics.md`](results/metrics.md) |

---

## Limitations

- **Simulation only (Phase 1):** Webots world and controllers are pending implementation (Sprint S1–S3, Oct–Nov). Controller  folders are present with READMEs.
- **Hardware prototype:** Planned for build sprint 17–23 Nov (Sprint S4).
- **Beacon budget:** Fixed at 8 beacons per mission. Complex tunnels with many branches may require replanning.
- **Radio model:** Webots emitter/receiver provides simplified RF range; actual LoRa 433 MHz tunnel attenuation is approximated via the radio propagation plugin.
- **Frame translation accuracy:** Depends on surveyed anchor point quality. Uncertainty grows at σ(s) = 0.3 + 0.02·s metres with path length.
- **No multi-Writer support** in Phase 1; single Writer robot per mission.

---

## License

MIT — see [`LICENSE`](LICENSE).
