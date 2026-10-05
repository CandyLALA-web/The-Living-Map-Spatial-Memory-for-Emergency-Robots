# Beacon Drop Mechanism

Servo-driven rotary magazine for deploying beacon nodes.

> **PENDING** — Mechanical design files to be produced during Sprint S4 (17–23 Nov 2026).

## Concept

A **rotary magazine** mounted at the rear of the Writer Robot chassis holds up to **8 beacon nodes** in radially-arranged slots. When the controller issues a DROP command, the MG995 servo rotates the magazine by **45°** (360° / 8 slots), releasing one beacon into a gravity-feed channel that guides it to the tunnel floor directly behind the robot.

## Mechanism Description

1. **Magazine drum**: 3D-printed ABS cylinder, 120 mm diameter, 8 pockets at 45° intervals. Each pocket friction-holds one IP54 enclosure (90 × 36 × 25 mm).
2. **Release gate**: A spring-loaded trapdoor at the bottom of the drum; servo rotation swings the gate open for the pocket aligned to the bottom.
3. **Gravity channel**: 35° inclined ramp guides the beacon from the gate to the floor, ensuring it lands upright with the RF antenna facing up.
4. **Servo**: MG995 metal-gear servo (11 kg·cm). One 45° rotation per drop command; position-controlled via PWM from RPi GPIO 18.
5. **Beacon count sensor**: IR break-beam in each pocket to count remaining beacons; signals low-beacon warning at ≤ 2 remaining.

## Expected Design Files

| File | Format | Contents |
|------|--------|---------|
| `magazine_assembly.step` | STEP | Full assembly CAD (drum + gate + ramp + motor mount) |
| `magazine_assembly.stl` | STL | 3D-printable drum body (split for FDM printing) |
| `mechanism_diagram.pdf` | PDF | Exploded view with part labels and dimensions |

## Print Settings (Preliminary)

- Material: PETG (heat-resistant, tunnel humidity tolerance)
- Layer height: 0.2 mm
- Infill: 30% gyroid
- Perimeters: 3
- Estimated print time: ~4 hours (drum body only)
