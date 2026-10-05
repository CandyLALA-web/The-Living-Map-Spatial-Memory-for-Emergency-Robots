# System Evaluation & Benchmark Metrics
**Team [ANONYMIZED] — Phase 1 Submission** 
*Independent Submission* 
Environment: Mines / Tunnels | Evaluation Trials: N = 20

---

## 1. Quantitative Benchmark Results

| Metric | Target | Measured Result | Status | Evaluation Protocol |
|---|---|---|---|---|
| **Map Coverage IoU** | $\ge 0.80$ | **0.842** | PASS | 2D log-odds grid compared to ground-truth Webots tunnel floorplan |
| **Beacon Geodetic Position Error** | $\le 2.0$ m | **0.34 m RMS** | PASS | Euclidean disparity between translated GPS and supervisor ground truth |
| **Event-to-Dashboard Latency** | $\le 10.0$ s | **2.84 s** | PASS | Elapsed wall-clock from hazard threshold detection to Command Post map display |
| **Mission Success Rate** | $\ge 0.80$ | **0.95 (19/20)** | PASS | Executor successfully reaches target in randomized failure injection scenarios |
| **Mean Time to Target** | $\le 90$ s | **46.2 s** | PASS | Autonomous transit time following the inherited beacon chain |

---

## 2. Statistical Analysis
All metrics gathered over $N = 20$ randomized fault-injection runs in Webots R2023b, including emulated RF burst interference, simulated Writer motor stall, and post-collapse corridor blockage.
