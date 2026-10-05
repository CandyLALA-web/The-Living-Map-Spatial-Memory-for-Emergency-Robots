"""
Executor Robot Controller - TSYP14 Living Map Challenge
Waits for beacon data relayed from the Writer, navigates to each target,
and performs a REAL physical action in the world on arrival (valve close /
marker spawn) using Supervisor privileges.
"""

from controller import Supervisor
import math
import os

# ----- Setup (Supervisor instead of plain Robot) -----
robot = Supervisor()
timestep = int(robot.getBasicTimeStep())

left_motor = robot.getDevice('left wheel')
right_motor = robot.getDevice('right wheel')
if left_motor is None:
    left_motor = robot.getDevice('left wheel motor')
if right_motor is None:
    right_motor = robot.getDevice('right wheel motor')

left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))
left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)

MAX_SPEED = min(left_motor.getMaxVelocity(), 5.24) if left_motor else 5.24

gps = robot.getDevice('gps')
gps.enable(timestep)

compass = None
try:
    compass = robot.getDevice('compass')
    compass.enable(timestep)
except Exception:
    pass

sensor_names = ['so0', 'so1', 'so2', 'so3', 'so12', 'so13', 'so14', 'so15']
sonars = {}
for name in sensor_names:
    try:
        s = robot.getDevice(name)
        s.enable(timestep)
        sonars[name] = s
    except Exception:
        pass

# ----- Shared beacon log -----
SHARED_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'shared_data')
BEACON_LOG_PATH = os.path.join(SHARED_DIR, 'beacon_log.txt')

mission_queue = []
processed_beacon_ids = set()
current_target = None
current_label = None
mission_active = False
ARRIVAL_RADIUS = 0.4


def distance_2d(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[2] - b[2]) ** 2)


def heading_to_target(current_pos, target_pos):
    dx = target_pos[0] - current_pos[0]
    dz = target_pos[2] - current_pos[2]
    return math.atan2(dz, dx)


def get_current_heading():
    if compass:
        values = compass.getValues()
        return math.atan2(values[0], values[2])
    return 0.0


def navigate_to(target_pos, current_pos):
    base_speed = 3.0
    target_heading = heading_to_target(current_pos, target_pos)
    current_heading = get_current_heading()
    heading_error = target_heading - current_heading

    while heading_error > math.pi:
        heading_error -= 2 * math.pi
    while heading_error < -math.pi:
        heading_error += 2 * math.pi

    turn = 2.0 * heading_error
    left_speed = base_speed - turn
    right_speed = base_speed + turn

    if sonars:
        min_reading = min(s.getValue() for s in sonars.values())
        if min_reading < 0.4:
            left_speed = base_speed - 2.5
            right_speed = base_speed + 2.5

    left_speed = max(min(left_speed, MAX_SPEED), -MAX_SPEED)
    right_speed = max(min(right_speed, MAX_SPEED), -MAX_SPEED)
    left_motor.setVelocity(left_speed)
    right_motor.setVelocity(right_speed)


def stop_robot():
    left_motor.setVelocity(0.0)
    right_motor.setVelocity(0.0)


# ----- REAL physical actions using Supervisor privileges -----

def close_valve():
    """Finds the VALVE node and turns it green to show it's been closed."""
    valve_node = robot.getFromDef('VALVE')
    if valve_node is None:
        print("[WARNING] VALVE node not found - check DEF name in world file")
        return
    appearance_field = valve_node.getField('children').getMFNode(0).getField('appearance')
    appearance_node = appearance_field.getSFNode()
    color_field = appearance_node.getField('baseColor')
    color_field.setSFColor([0.1, 0.8, 0.1])  # green = closed/safe
    print("[WORLD UPDATE] Valve turned green - gas leak mitigated")


def drop_marker(position):
    """Spawns a small marker Solid at the given position to show a
    supply/marker was physically left for human responders."""
    root = robot.getRoot()
    children_field = root.getField('children')
    marker_vrml = f"""
    Solid {{
      translation {position[0]} {position[1]} {position[2]}
      children [
        Shape {{
          appearance PBRAppearance {{
            baseColor 0.1 0.3 0.9
            roughness 0.3
            metalness 0.1
          }}
          geometry Sphere {{ radius 0.1 subdivision 1 }}
        }}
      ]
      name "response_marker"
    }}
    """
    children_field.importMFNodeFromString(-1, marker_vrml)
    print(f"[WORLD UPDATE] Marker dropped at {position}")


def perform_mission_action(label, target_pos):
    t_now = int(robot.getTime())
    if "GAS" in label:
        close_valve()
        print(f"[MISSION ACTION] t={t_now}s | Valve closed - gas leak mitigated at {target_pos}")
    else:
        drop_marker(target_pos)
        print(f"[MISSION ACTION] t={t_now}s | Marker dropped at {target_pos}")
    print(f"[MISSION COMPLETE] status=confirmed | event={label} | target={target_pos}")


def poll_beacon_log():
    if not os.path.exists(BEACON_LOG_PATH):
        return
    with open(BEACON_LOG_PATH, 'r') as f:
        lines = f.readlines()
    for line in lines:
        parts = line.strip().split(',')
        if len(parts) < 10:
            continue
        beacon_id = int(parts[0])
        if beacon_id in processed_beacon_ids:
            continue
        processed_beacon_ids.add(beacon_id)
        label = parts[2]
        x, y, z = float(parts[3]), float(parts[4]), float(parts[5])
        mission_queue.append((label, (x, y, z)))
        print(f"[EXECUTOR] Received beacon #{beacon_id} ({label}) - added to mission queue")


# ----- Main loop -----
print("Executor robot standing by - waiting for beacon data...")

while robot.step(timestep) != -1:
    poll_beacon_log()
    pos = gps.getValues()

    if not mission_active and mission_queue:
        current_label, current_target = mission_queue.pop(0)
        mission_active = True
        print(f"[EXECUTOR] Mission briefed: heading to {current_label} at {current_target}")

    if mission_active:
        if distance_2d(pos, current_target) < ARRIVAL_RADIUS:
            stop_robot()
            perform_mission_action(current_label, current_target)
            mission_active = False
            current_target = None
        else:
            navigate_to(current_target, pos)
    else:
        stop_robot()
