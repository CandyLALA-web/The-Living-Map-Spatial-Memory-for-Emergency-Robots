# Frame Translation Library

Shared coordinate transform library used by ONA gateway and Command Post.

## Purpose

Converts between the **local tunnel frame** (origin at ONA anchor, x along tunnel axis) and **WGS-84 GPS** (latitude, longitude, altitude) for Command Post display and mission planning.

## Coordinate Frames

| Frame | Origin | Axes | Units |
|-------|--------|------|-------|
| **Local** | ONA anchor (tunnel entrance) | +x: into tunnel, +y: left, +z: up | metres |
| **GPS (WGS-84)** | Earth centre | lat, lon, alt | degrees, degrees, metres |

## ONA Anchor Parameters

Obtained from:
1. **Averaged GPS fix** at tunnel entrance (≥ 60 s averaging to reduce multipath error)
2. **Two surveyed entrance marks** to determine bearing ψ (clockwise from true north)

Parameters: `lat0_deg`, `lon0_deg`, `h0_m`, `psi_deg`

## Forward Transform: local → GPS

```python
import math

R = 6_378_137.0 # WGS-84 semi-major axis, m

def local_to_gps(x, y, z, lat0_deg, lon0_deg, h0, psi_deg):
 """Convert local (x,y,z) metres to WGS-84 (lat_deg, lon_deg, alt_m)."""
 psi = math.radians(psi_deg)
 E = x * math.sin(psi) - y * math.cos(psi)
 N = x * math.cos(psi) + y * math.sin(psi)
 lat0 = math.radians(lat0_deg)
 lat = lat0_deg + (N / R) * (180.0 / math.pi)
 lon = lon0_deg + (E / (R * math.cos(lat0))) * (180.0 / math.pi)
 alt = h0 + z
 return lat, lon, alt
```

## Inverse Transform: GPS → local

```python
def gps_to_local(lat_deg, lon_deg, alt_m, lat0_deg, lon0_deg, h0, psi_deg):
 """Convert WGS-84 (lat,lon,alt) to local (x,y,z) metres."""
 psi = math.radians(psi_deg)
 lat0 = math.radians(lat0_deg)
 dN = (lat_deg - lat0_deg) * (math.pi / 180.0) * R
 dE = (lon_deg - lon0_deg) * (math.pi / 180.0) * R * math.cos(lat0)
 x = dN * math.cos(psi) + dE * math.sin(psi)
 y = -dN * math.sin(psi) + dE * math.cos(psi)
 z = alt_m - h0
 return x, y, z
```

## Uncertainty Propagation

σ(s) = 0.3 + 0.02 · s metres, where s = accumulated path length from ONA anchor.

Propagated to GPS: displayed as a circle of radius σ(s) on the Command Post live map.

## Worked Example

**Anchor**: lat0 = 36.8065°N, lon0 = 10.1815°E, h0 = 120 m, ψ = 30°

**Beacon local position**: (x, y, z) = (42.0, −1.5, 0.0) m

```
E = 42·sin(30°) − (−1.5)·cos(30°) = 21.000 + 1.299 = 22.299 m
N = 42·cos(30°) + (−1.5)·sin(30°) = 36.373 − 0.750 = 35.623 m

lat = 36.8065 + (35.623 / 6378137) · (180/π) = 36.80682°N
lon = 10.1815 + (22.299 / (6378137 · cos(36.8065°·π/180))) · (180/π) = 10.18175°E
alt = 120.0 m
```

**Result**: 36.80682°N, 10.18175°E, 120.0 m
