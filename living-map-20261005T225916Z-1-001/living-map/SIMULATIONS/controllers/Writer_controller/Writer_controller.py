"""
Writer Robot Controller - TSYP14 Living Map Challenge
Explores the tunnel using a systematic waypoint sweep, avoids walls,
detects events (gas leak, collapse risk), and drops binary beacons.
"""

from controller import Robot
import struct
import math
import sys

# Unbuffer stdout so prints appear in real-time in Webots console
sys.stdout.reconfigure(line_buffering=True)

# ----- Setup -----
robot = Robot()
timestep = int(robot.getBasicTimeStep())

# Tunnel search grid waypoints (x, y)
# Adjust max X (e.g., 12.0m) and Y bounds to fit your world's exact dimensions
SWEEP_WAYPOINTS = [
    # Row 1: Right down the middle
    (1.0, 0.0),
    (12.0, 0.0),
    
    # Row 2: Right side sweep returning
    (12.0, 0.8),
    (1.0, 0.8),
    
    # Row 3: Left side sweep going forward
    (1.0, -0.8),
    (12.0, -0.8),
]

# ----- Motors -----
left_motor = robot.getDevice('left wheel')
right_motor = robot.getDevice('right wheel')

if left_motor is None:
    left_motor = robot.getDevice('left wheel motor')
if right_motor is None:
    right_motor = robot.getDevice('right wheel motor')

if left_motor and right_motor:
    left_motor.setPosition(float('inf'))
    right_motor.setPosition(float('inf'))
    left_motor.setVelocity(0.0)
    right_motor.setVelocity(0.0)
else:
    print("[ERROR] Motors could not be initialized! Check device names in Webots.")

MAX_SPEED = min(left_motor.getMaxVelocity(), 5.24) if left_motor else 5.24

# ----- GPS -----
gps = robot.getDevice('gps')
gps.enable(timestep)

# ----- Sonars -----
sensor_names = ['so0', 'so1', 'so2', 'so3', 'so12', 'so13', 'so14', 'so15']
sonars = {}
for name in sensor_names:
    try:
        s = robot.getDevice(name)
        s.enable(timestep)
        sonars[name] = s
    except Exception:
        pass

# ----- Event Targets -----
GAS_LEAK_POS = (2.0, 0.6, -0.65)
COLLAPSE_POS = (5.0, 1.0, 0.6)
DETECTION_RADIUS = 1.0  # meters

# ----- State Variables -----
mission_id = 1
beacon_counter = 0
events_triggered = {'gas': False, 'collapse': False}

EVENT_GAS = 2
EVENT_COLLAPSE = 3

prev_pos = None


def get_robot_yaw(current_pos, fallback_yaw):
    """Computes yaw heading in radians using position delta from GPS."""
    global prev_pos
    if prev_pos is None:
        prev_pos = current_pos
        return fallback_yaw

    dx = current_pos[0] - prev_pos[0]
    dy = current_pos[1] - prev_pos[1]
    
    # Update heading only if robot has moved > 1 cm
    if math.sqrt(dx**2 + dy**2) > 0.01:
        yaw = math.atan2(dy, dx)
        prev_pos = current_pos
        return yaw
        
    return fallback_yaw


def navigate_to_waypoint(robot_pos, yaw, target_pos):
    """Calculates wheel speeds to steer towards target waypoint."""
    dx = target_pos[0] - robot_pos[0]
    dy = target_pos[1] - robot_pos[1]
    
    distance_to_target = math.sqrt(dx**2 + dy**2)
    
    if distance_to_target < 0.3:
        return 0.0, 0.0, True

    target_yaw = math.atan2(dy, dx)
    angle_error = target_yaw - yaw
    
    # Normalize angle error between -pi and +pi
    while angle_error > math.pi: angle_error -= 2 * math.pi
    while angle_error < -math.pi: angle_error += 2 * math.pi

    base_speed = 2.5
    kp = 2.0  # Proportional turning gain
    
    turn_bias = kp * angle_error
    
    left_speed = base_speed - turn_bias
    right_speed = base_speed + turn_bias
    
    return left_speed, right_speed, False


def distance_3d(a, b):
    return math.sqrt(sum((a[i] - b[i]) ** 2 for i in range(3)))


def pack_beacon(beacon_id, event_type, severity, confidence, value,
                beacon_pos, event_offset, t_written):
    """Pack beacon payload per competition spec."""
    severity_confidence = ((severity & 0x0F) << 4) | (confidence & 0x0F)
    
    bx = max(-32768, min(32767, int(beacon_pos[0] * 10)))
    by = max(-32768, min(32767, int(beacon_pos[1] * 10)))
    bz = max(-32768, min(32767, int(beacon_pos[2] * 10)))
    
    dx = max(-128, min(127, int(event_offset[0] * 2)))
    dy = max(-128, min(127, int(event_offset[1] * 2)))
    dz = max(-128, min(127, int(event_offset[2] * 2)))

    data = struct.pack(
        '<BBBB BBh hhh bbb HH',
        1, 0, mission_id & 0xFF, beacon_id & 0xFF, event_type & 0xFF,
        severity_confidence, int(value) & 0xFFFF, bx, by, bz,
        dx, dy, dz, int(t_written) & 0xFFFF, 0
    )
    return data


def drop_beacon(event_type, label, robot_pos, severity, confidence, value):
    global beacon_counter
    beacon_counter += 1
    t_now = int(robot.getTime())
    msg = pack_beacon(
        beacon_id=beacon_counter,
        event_type=event_type,
        severity=severity,
        confidence=confidence,
        value=value,
        beacon_pos=robot_pos,
        event_offset=(0, 0, 0),
        t_written=t_now
    )
    print(f"[BEACON DROPPED] #{beacon_counter} | {label} | "
          f"pos=({robot_pos[0]:.2f}, {robot_pos[1]:.2f}, {robot_pos[2]:.2f}) | "
          f"t={t_now}s | hex={msg.hex()}", flush=True)


def check_events(robot_pos):
    if not events_triggered['gas']:
        if distance_3d(robot_pos, GAS_LEAK_POS) < DETECTION_RADIUS:
            drop_beacon(EVENT_GAS, "GAS LEAK", robot_pos,
                        severity=3, confidence=12, value=3200)
            events_triggered['gas'] = True

    if not events_triggered['collapse']:
        if distance_3d(robot_pos, COLLAPSE_POS) < DETECTION_RADIUS:
            drop_beacon(EVENT_COLLAPSE, "COLLAPSE RISK", robot_pos,
                        severity=4, confidence=10, value=0)
            events_triggered['collapse'] = True


def is_obstacle_ahead():
    if not sonars:
        return False
    front_sensors = ['so0', 'so1', 'so2', 'so3', 'so12', 'so13', 'so14', 'so15']
    readings = [sonars[s].getValue() for s in front_sensors if s in sonars]
    valid_readings = [r for r in readings if r > 0.05]
    if not valid_readings:
        return False
    return min(valid_readings) < 0.5


def avoid_obstacles():
    base_speed = 2.0
    left_sensors = ['so0', 'so1', 'so2', 'so3']
    right_sensors = ['so12', 'so13', 'so14', 'so15']

    left_dist = min([sonars[s].getValue() for s in left_sensors if s in sonars], default=10.0)
    right_dist = min([sonars[s].getValue() for s in right_sensors if s in sonars], default=10.0)

    if left_dist < right_dist:
        left_motor.setVelocity(base_speed)
        right_motor.setVelocity(-base_speed * 0.5)
    else:
        left_motor.setVelocity(-base_speed * 0.5)
        right_motor.setVelocity(base_speed)


# ----- Main Execution Loop -----
print("Writer robot started - systematic tunnel sweep...", flush=True)

current_waypoint_idx = 0
current_yaw = 0.0

while robot.step(timestep) != -1:
    pos = gps.getValues()
    
    if math.isnan(pos[0]) or math.isnan(pos[1]) or math.isnan(pos[2]):
        continue

    # Update current orientation heading
    current_yaw = get_robot_yaw(pos, current_yaw)

    # Detect gas leak / collapse risk
    check_events(pos)

    # Waypoint path execution
    if current_waypoint_idx < len(SWEEP_WAYPOINTS):
        target = SWEEP_WAYPOINTS[current_waypoint_idx]
        
        left_sp, right_sp, arrived = navigate_to_waypoint(pos, current_yaw, target)
        
        if arrived:
            print(f"[PATH PLAN] Reached waypoint {current_waypoint_idx + 1}/{len(SWEEP_WAYPOINTS)}: {target}", flush=True)
            current_waypoint_idx += 1
        else:
            if is_obstacle_ahead():
                avoid_obstacles()
            else:
                left_motor.setVelocity(max(-MAX_SPEED, min(MAX_SPEED, left_sp)))
                right_motor.setVelocity(max(-MAX_SPEED, min(MAX_SPEED, right_sp)))
    else:
        left_motor.setVelocity(0.0)
        right_motor.setVelocity(0.0)
        print("[PATH PLAN] Area sweep complete!", flush=True)
        break