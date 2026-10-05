"""Living Map - frame translation.

Writer frame: origin = anchor beacon, +x = robot heading at start, +y = left (REP-103).
psi = compass bearing of the +x axis, degrees clockwise from true north.
"""
import math
from dataclasses import dataclass

R_EARTH = 6378137.0  # m, local flat-earth approximation (error < 1 cm at 100 m)


@dataclass
class Anchor:
    lat: float      # deg, from the Outside Network GPS
    lon: float      # deg
    psi_deg: float  # compass bearing of Writer +x axis


def local_to_enu(x: float, y: float, psi_deg: float) -> tuple[float, float]:
    p = math.radians(psi_deg)
    east = x * math.sin(p) - y * math.cos(p)
    north = x * math.cos(p) + y * math.sin(p)
    return east, north


def enu_to_local(east: float, north: float, psi_deg: float) -> tuple[float, float]:
    p = math.radians(psi_deg)
    x = east * math.sin(p) + north * math.cos(p)
    y = -east * math.cos(p) + north * math.sin(p)
    return x, y


def local_to_gps(x_m: float, y_m: float, a: Anchor) -> tuple[float, float]:
    e, n = local_to_enu(x_m, y_m, a.psi_deg)
    lat = a.lat + math.degrees(n / R_EARTH)
    lon = a.lon + math.degrees(e / (R_EARTH * math.cos(math.radians(a.lat))))
    return lat, lon


def gps_to_local(lat: float, lon: float, a: Anchor) -> tuple[float, float]:
    n = math.radians(lat - a.lat) * R_EARTH
    e = math.radians(lon - a.lon) * R_EARTH * math.cos(math.radians(a.lat))
    return enu_to_local(e, n, a.psi_deg)


def sigma_m(path_len_m: float, dist_from_anchor_m: float,
            k_odom: float = 0.05, sigma_psi_deg: float = 5.0,
            sigma_gps_m: float = 3.0) -> float:
    """1-sigma position error: odometry drift + compass error + GPS fix."""
    drift = k_odom * path_len_m
    compass = dist_from_anchor_m * math.radians(sigma_psi_deg)
    return math.sqrt(drift**2 + compass**2 + sigma_gps_m**2)


if __name__ == "__main__":
    a = Anchor(lat=36.8430, lon=10.1950, psi_deg=30.0)
    x_cm, y_cm = 420, 150                     # values stored in the beacon
    x, y = x_cm / 100, y_cm / 100
    e, n = local_to_enu(x, y, a.psi_deg)
    lat, lon = local_to_gps(x, y, a)
    print(f"local ({x:.2f}, {y:.2f}) m -> ENU E={e:.3f} N={n:.3f} m")
    print(f"GPS   {lat:.7f}, {lon:.7f}")
    bx, by = gps_to_local(lat, lon, a)
    print(f"round trip -> ({bx:.3f}, {by:.3f}) m")
    d = math.hypot(x, y)
    print(f"sigma at {d:.1f} m from anchor, path 8 m: {sigma_m(8, d):.2f} m")
    print(f"sigma at 30 m from anchor, path 60 m: {sigma_m(60, 30):.2f} m")
    assert abs(bx - x) < 1e-3 and abs(by - y) < 1e-3