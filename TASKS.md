# Vanguard Arm — Execution Plan: Phase 0c → Gate G0 (+P1 runway)

## HANDOFF BLOCK (paste-first for any fresh session, any model)
Vanguard arm autonomy, BITS-H Mars Rover team; goal = win IRC 2027. Stack: Ubuntu 22.04/ROS2
Humble in container `vanguard-arm-dev`, Isaac Sim 5.1 on host (`~/launch_isaac.sh`, stage
`ros2_ws/isaac/VanguardArm.usd`), `topic_based_ros2_control` overlay
(`vanguard_isaac_control`), MoveIt via `ur_moveit_config`. **Bring-up order: Isaac(Play) →
control stack → MoveIt.** Done so far: digital twin proven (unmodified client code drives
PhysX), IDMO panel v0.3 (articulation; button+switch publish `/panel_joint_states`),
`press_button.py` = first skill, deterministic (joint-space between HARVESTED configs) and
self-scoring (verify by panel joint state). Working agreement PLAN.md §0: Krithin types
implementation code (R1); theory gate per phase (R2, CURRICULUM.md); Claude authors textbook
same-session (R3). Debug ladder + standing truths: `.claude/skills/bug-hunter/SKILL.md` annex.
Approach chosen & why: demonstration-and-replay (captured configs) over pose/IK planning —
poses are an 8-branch IK lottery and the cartesian service degrades silently (textbook ch.9);
poses return only when perception drives them. When judgment calls exceed the plan: route to
the smartest available model (CLAUDE.md model-routing table).

## Org calendar (interleave; none of these move)
| When | What |
|---|---|
| ~Aug 2026 | Faculty advisor CLOSED (gates P1 endorsement, RESPOND, NVIDIA) — in progress |
| ~Sept 2026 | IRC 2027 registration opens (roverchallenge.org — watch weekly, /schedule agent) |
| ~Sept 2026 | Mech arm arrives → Phase 1 hardware bring-up begins |
| ~1 Oct 2026 | LeRobot recording pipeline MUST be live (S4) — P1 data clock starts |
| ~29 Oct 2026 | ARC (Australian) 2027 CDR due — draft alongside IRC SDDR |
| ~20 Nov 2026 | IRC SDDR (report + 5-min video; cut from rehearsal footage) |
| ~15 Dec 2026 | P1 submitted (arXiv same day) |

## S1 — `switch_flip`: prove the pattern generalizes (1 session)
- **Goal:** second skill: flip the yellow switch to a commanded side, verify via
  `/panel_joint_states` (`switch_joint` < −0.3 rad or > +0.3 rad per side).
- **Where:** `ros2_ws/src/scripts/switch_flip.py` (copy press_button skeleton).
- **How:** harvest 3 configs (hover-at-switch, push-left-contact, push-right-contact) by
  jogging in RViz/running partial motions and reading `/joint_states` (the ch.9 harvest move).
  Also: give the switch a detent so it stops gravity-creeping — in `build_panel.py` set switch
  drive stiffness ~2.0 with targetPosition at ±25° after flip, or accept creep and verify sign only.
- **Verify:** 3 consecutive runs each direction, `FLIP VERIFIED (left/right)` printed; switch
  visibly rests on the commanded side.
- **Fence:** no perception, no BT yet, no new panel elements. One skill, one session.

## S2 — skill library: extract the pattern (1–2 sessions)
- **Goal:** `vanguard_skills` ROS package: `PanelSkill` base class (scene box, leg() guard,
  panel-state subscription, verify-by-effect, harvested-config registry in a YAML —
  `configs/taught_poses.yaml`), with press_button + switch_flip as 20-line subclasses.
- **Where:** `ros2_ws/src/vanguard_skills/` (proper package: setup.py, entry points).
- **Verify:** `ros2 run vanguard_skills press_button` and `... switch_flip` both VERIFIED;
  scripts/ versions deleted; colcon test passes a smoke test that imports both skills.
- **Fence:** do NOT add BT here; do NOT touch the Isaac stage. Refactor only — behavior
  byte-identical to S1.

## S3 — panel v1: the full IRC element set (1–2 sessions + Isaac GUI)
- **Goal:** add knob (revolute, free), latch (revolute with catch), drawer (prismatic, long
  travel), 3-pin socket (collision geometry only) to `build_panel.py`; all joints in
  `/panel_joint_states`; positions parameterized by a `LAYOUT` dict (randomization-ready = P1).
- **Verify:** rebuild → Play → every element manipulable by Shift-drag or DriveAPI; topic
  carries all joints; board doesn't move; Ctrl+S survives reopen.
- **Fence:** dimensions from IRC-2026 rulebook (graph-query it, don't re-read the PDF);
  arm-reach-checked at z≈0.72–0.85; no skill code in this task.

## S4 — teleop + LeRobot recording (the P1-critical path; 2–3 sessions, DONE BEFORE OCT 1)
- **Goal:** (a) keyboard/gamepad jog teleop via `moveit_servo` (config from Block C1 —
  Claude provides servo YAML+launch reference, Krithin types); (b) every teleop session
  recorded as LeRobot-format episodes: obs = `/joint_states` + `/panel_joint_states` (+ a
  wrist-camera image topic once an Isaac camera is added to the stage), action = servo twists
  or joint targets. `ros2 bag record -s mcap` in parallel (both formats, per PLAN §8).
- **Where:** `ros2_ws/src/vanguard_teleop/`; recorder bridges via `~/venvs/lerobot`.
- **Verify:** drive the arm to press the button BY HAND via teleop; a LeRobot dataset with ≥5
  episodes loads in `lerobot` python and replays; MCAP bag plays back in Foxglove.
- **Fence:** no policy training yet; no GELLO hardware (that's a Phase-1 build); wrist camera
  = one Isaac Camera prim + ROS2 CameraHelper node, not a full sensor suite.

## S5 — BT wrapper + the six stubs (1 session)
- **Goal:** BehaviorTree.CPP (or py_trees if C++ drags — decide by build friction, log the
  decision) mission tree: `IDMO_demo` = press_button → flip_switch, with per-skill fallback
  to "report failure, hold position". Stubs registered for the remaining 4 skills (grasp,
  insert, place, read-code) that log NOT_IMPLEMENTED.
- **Verify:** one command runs the 2-skill mission end to end, both VERIFIED; injected failure
  (unplug panel topic) routes to the fallback branch, mission reports partial.
- **Fence:** no new skill implementations here; tree + wiring only.

## S6 — GATE G0: the Phase-0 exit exam (half session, repeat weekly after)
- **Goal:** PLAN §6 gate: teleop operator (Krithin) completes ≥5 panel operations in ≤15 min
  in sim, from cold start, logged.
- **Verify:** MCAP bag + a one-page scorecard (ops attempted/completed/times) in
  `docs/rehearsals/`; textbook chapter on the first rehearsal.
- **Fence:** no autonomy in the loop — this gate measures the OPERATOR + stack reliability.

## S7 — CI: the nightly regression (1 session, laptop-docked cron)
- **Goal:** script `ci/nightly.sh`: colcon build + unit tests + (when laptop docked with Isaac
  running) headless skill regression — press_button + switch_flip once each, exit code from
  VERIFIED lines; cron/systemd-timer wiring; log to `ci/log/`.
- **Verify:** intentionally break a config → nightly run FAILS loudly; fix → green.
- **Fence:** GitHub Actions gets build+lint only (no GPU/Isaac in cloud); don't gold-plate.

## Standing review cadence (use the installed skills)
- `/code-review` on every nontrivial diff before commit (bug-hunter for anything broken —
  its ROS annex has the ladder).
- `security-sweep` before the repo goes public (pre-P1 release, ~Nov) — check git history
  for anything personal, since day-1 history was cleaned but new history accumulates.
- `honest-advisor` on any new research/feature idea before it enters the plan (the P6/MPC
  triage pattern: reshape onto our moat or reject).
- `/checkpoint` every session, no exceptions — it's why cold starts cost minutes not hours.

## Risks with tripwires
- **Isaac camera/rendering in headless CI is flaky** → tripwire: S7 first headless run; fallback: CI regression runs state-only (no camera), camera episodes recorded only in interactive sessions.
- **LeRobot format churn** (v2→v3) → tripwire: S4 first dataset load; fallback: pin lerobot version in the venv, note in pinned-versions table.
- **moveit_servo config fights the overlay stack** → tripwire: S4 day 1 (servo publishes to a controller we don't run); fallback: jog via joint_trajectory goals at 5 Hz (cruder, works).
- **Mech arm slips past Sept** → no tripwire needed: everything above is sim-only by design; Phase 1 slides without touching P1.
