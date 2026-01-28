---
term: IMU (Inertial Measurement Unit)
created: 2026-01-27
---

# IMU (Inertial Measurement Unit)

> **See also:** [[quick-context/silicon-die]] | [[quick-context/semiconductor-fabrication]]

**Definition:** A sensor package combining accelerometer (linear acceleration), gyroscope (angular velocity), and often magnetometer (compass heading) to track orientation and motion. The BNO086 in your Pupper is a 9-axis IMU with built-in sensor fusion that outputs quaternions—essential for knowing which way the robot is tilting.

```
IMU SENSOR AXES:

         +Z (yaw)
          │
          │  ╱ +Y (pitch)
          │ ╱
          │╱
   ───────┼──────► +X (roll)
         ╱│
        ╱ │

  ACCELEROMETER: measures g-force on each axis
  GYROSCOPE: measures rotation rate (°/sec)
  MAGNETOMETER: measures magnetic field direction

  SENSOR FUSION (what BNO086 does internally):
  ┌─────────┐
  │  Accel  ├──┐
  └─────────┘  │    ┌──────────┐    ┌────────────┐
  ┌─────────┐  ├───►│  Fusion  ├───►│ Quaternion │
  │  Gyro   ├──┤    │Algorithm │    │ (x,y,z,w)  │
  └─────────┘  │    └──────────┘    └────────────┘
  ┌─────────┐  │
  │   Mag   ├──┘    Corrects drift, outputs stable orientation
  └─────────┘
```

**Key insight:** Raw gyro data drifts over time (accumulating error), raw accelerometer is noisy—sensor fusion combines them so gyro handles fast motion while accelerometer corrects long-term drift.
