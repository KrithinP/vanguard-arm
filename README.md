# Vanguard Arm

Manipulation autonomy for Project Vanguard — BITS Pilani Hyderabad Mars Rover team.
Goal: win **IRC 2027**, then ARC → ERC → URC; 5 papers by mid-2028.

Master plan, curriculum, and tooling live in this directory:
`PLAN.md` · `CURRICULUM.md` · `TOOLING.md`. Decisions: `../../decisions/log.md` (AIOS root).

## Architecture (see PLAN.md §4 for the full diagram)

```
Operator station (Foxglove + teleop UI + GELLO leader arm)
        │  WebRTC video · zenoh/rosbridge telemetry
Rover (Jetson Orin, ROS 2 Humble)
  Task layer:   BehaviorTree.CPP skills — grasp · panel-op · insert · place · sample · read
  Motion:       MoveIt 2 (OMPL + Pilz) · moveit_servo · (cuMotion, Phase 3)
  Perception:   ArUco/AprilTag → YOLO+SAM2 → FoundationPose · wrist + mast RGB-D
  Control:      ros2_control → CAN drivers · current-based contact detection
        ║ identical ROS 2 interfaces
Isaac Sim digital twin (URDF + IDMO panel scene + Replicator)
```

## Quickstart

```bash
# VS Code → "Reopen in Container" (.devcontainer/), then:
ros2 doctor
colcon build --symlink-install   # ros2_ws/
```

Textbook: `docs/textbook/` (`tectonic main.tex`). Research pipelines: `research/`.

## Pinned versions (do not drift without a decision-log entry)

| Component | Version | Why |
|---|---|---|
| Ubuntu / ROS 2 | 22.04 / Humble | Season platform; Jazzy migration scheduled post-IRC (PLAN §6 Phase 3) |
| Isaac Sim | **5.1.0** (standalone zip, `~/isaacsim`) | Current stable; official UR5e asset |
| Isaac Lab | **2.3.2** | Last stable release paired with Isaac Sim 5.1 (Lab 3.0 is beta, needs Isaac Sim 6.0 — revisit at Phase 3) |
| RMW | CycloneDDS, `ROS_DOMAIN_ID=42` | Team-wide DDS decision (textbook §1.3) |

## Working agreement

Krithin types all implementation code (Claude provides reference + review). Theory gates per
phase (`CURRICULUM.md`). Claude authors textbook + docs in-session. Details: PLAN.md §0.
