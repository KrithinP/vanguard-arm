# S4 REFERENCE — teleop + LeRobot recorder (Fable, 2026-07-07). Krithin types; this is the map.

## Part A: moveit_servo on the overlay stack

**servo_config.yaml** (package `vanguard_teleop/config/`):
```yaml
servo_node:
  ros__parameters:
    move_group_name: ur_manipulator
    command_in_type: "unitless"          # -1..1 from gamepad/keyboard
    scale: {linear: 0.15, rotational: 0.4, joint: 0.3}
    publish_period: 0.017                # 60 Hz, match the stack
    command_out_type: trajectory_msgs/JointTrajectory
    publish_joint_positions: true
    publish_joint_velocities: false
    command_out_topic: /scaled_joint_trajectory_controller/joint_trajectory  # TOPIC iface of our JTC
    planning_frame: base_link
    ee_frame_name: tool0
    robot_link_command_frame: tool0      # jog in TOOL frame - operator-intuitive near the panel
    incoming_command_timeout: 0.2
    smoothing_filter_plugin_name: "online_signal_smoothing::ButterworthFilterPlugin"
    lower_singularity_threshold: 17.0    # Servo throttles near singularity - ch.A3 made real
    hard_stop_singularity_threshold: 30.0
    joint_limit_margin: 0.1
    check_collisions: true               # Servo checks the planning scene - publish the board box first!
    collision_check_rate: 10.0
    self_collision_proximity_threshold: 0.01
    scene_collision_proximity_threshold: 0.02
```
Launch: servo_node (params above + robot_description + SRDF from ur_moveit_config) + a
joy/keyboard node remapping to `/servo_node/delta_twist_cmds` (TwistStamped) and
`/servo_node/delta_joint_cmds`. Start servo via its trigger service:
`ros2 service call /servo_node/start_servo std_srvs/srv/Trigger`.

**KNOWN TRIPWIRE (from TASKS.md):** Humble Servo versions vary on `command_out_topic` support.
Verify FIRST: `ros2 topic info /scaled_joint_trajectory_controller/joint_trajectory` must show
sub=1 (JTC listens on its topic interface alongside the action). If Servo can't publish there,
fallback = the cruder-but-works jogger: a 20-line node that integrates twist input into a
joint target (via current /joint_states + DLS on the Jacobian from KDL) and sends 0.2 s
single-point trajectories at 5 Hz. Ugly, deterministic, competition-viable.

**Verify A:** press the button BY HAND via teleop (gamepad), while `/panel_joint_states`
confirms ≥6 mm. That run IS Gate-G0 practice.

## Part B: the LeRobot episode recorder

One node, `episode_recorder.py`, run alongside teleop; writes LeRobotDataset v2-format episodes.
```
obs:  /joint_states (6 pos+vel), /panel_joint_states (2 pos), wrist camera image
act:  the last servo command sent (subscribe to command_out_topic), 10 Hz resample
keys: observation.state (float32[8]), observation.images.wrist (HxWx3), action (float32[6])
meta: fps=10, task string ("press the red button"), episode boundaries = operator hotkey (start/stop/save|discard)
```
Implementation route: `lerobot.common.datasets.lerobot_dataset.LeRobotDataset.create()` +
`add_frame()`/`save_episode()` — check exact API against the PINNED lerobot version in
`~/venvs/lerobot` (API churn is the #2 tripwire; pin, don't chase). Recorder runs OUTSIDE the
container (venv has lerobot; DDS crosses fine with CycloneDDS+domain 42). MCAP in parallel:
`ros2 bag record -s mcap /joint_states /panel_joint_states /wrist_cam/image_raw <cmd_topic>`.

**Wrist camera (Isaac, once):** Stage → ur5e wrist_3_link → Create → Camera (child prim), pose
it looking past tool0; Action Graph → ROS2 Camera Helper node → topic `/wrist_cam/image_raw`,
640x480 @ 15 Hz (10 Hz resample downstream). Ctrl+S.

**Verify B (S4 gate):** 5 teleop episodes recorded → `LeRobotDataset(repo_id=local_path)` loads,
`dataset[0]` returns tensors with the right shapes → one episode replayed open-loop moves the arm.
```python
# replay smoke test: feed dataset actions back as joint targets at 10 Hz
```
