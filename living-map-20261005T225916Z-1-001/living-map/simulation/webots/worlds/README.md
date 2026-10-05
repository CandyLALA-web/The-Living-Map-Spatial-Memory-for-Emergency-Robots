# Webots Worlds

Place Webots world files (`*.wbt`) here.

## Expected File

**`living_map_tunnel.wbt`** — the mine tunnel world containing:

- Tunnel geometry with falling beam obstacle
- Debris field scattered across tunnel floor
- Two pipes running along tunnel walls
- Gas-leak emission point (at approximately x=42 m, y=-1.5 m in local frame)
- Writer Robot PROTO instance with start pose at tunnel entrance
- Executor Robot PROTO instance (docked at ONA gateway, enters on briefing)
- ONA Gateway node (Supervisor-managed, at tunnel entrance)
- Supervisor controller (orchestrates episodes, injects events, logs metrics)

## File Naming Convention

```
<scenario_name>.wbt
```

Examples:
- `living_map_tunnel.wbt` — primary mine tunnel scenario
- `living_map_tunnel_nogas.wbt` — variant without gas event (navigation-only test)
- `living_map_tunnel_multiblock.wbt` — multiple blocked-passage events
