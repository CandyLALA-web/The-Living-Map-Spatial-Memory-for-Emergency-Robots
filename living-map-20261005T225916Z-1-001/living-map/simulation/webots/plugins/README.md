# Physics and Radio Plugins

Place Webots physics and radio plugins here.

## Expected Plugins

### `radio_propagation_plugin`
Models tunnel RF attenuation for LoRa 433 MHz in rock/concrete:
- **Effective range**: ~6 m (worst-case mine tunnel attenuation model)
- Attenuation model: path-loss exponent n ≈ 3.5 (rock/concrete enclosed space)
- Applied to all channels (ch1, ch2, ch3)
- Webots API: `wb_emitter_set_range()` + custom `physics_plugin.c` for shadow zones

This approximates measured LoRa 433 MHz performance in mine-scale corridors. The 6 m range is conservative; actual LoRa SF7 range in tunnels can reach 15–30 m depending on wall material.

### `gas_dispersion_plugin`
Models gas concentration field for the GAS_LEAK event:
```
c(d) = c0 · exp(−d / L) + noise
```
where:
- `c0` = peak concentration at source (configurable, default 1.0)
- `d` = distance from emission point (m)
- `L` = decay length (default 5 m)
- `noise` ~ Gaussian(0, 0.02)

The Supervisor reads the concentration at the Writer Robot's position each timestep and injects it into a virtual sensor channel read by the `writer_robot` controller.

## Plugin Language
Webots physics plugins are written in **C** (`.c` / `.h`). The radio and gas plugins will be compiled by Webots automatically on first run.
