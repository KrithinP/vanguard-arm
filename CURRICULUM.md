# Vanguard Arm — Study Curriculum (Jul 2026 → IRC, Jan 2027)

Companion to `PLAN.md`. **For the intensive study sprint + oral-exam mastery standard, use
`STUDY-GUIDE.md` (2026-07-07) — it sequences and prioritizes; this file holds the full source
URLs, search keywords, and phase gates.** Rule R2 (theory-before-phase) runs on this document: each block gates a
build phase, and the "you're ready when" checks are the gate. Budget **6–8 h/week** alongside the
build — theory studied the same week you build the thing sticks 10× better than front-loading.

You already know well (skipping): Python/C++, deep learning (backbones, DETR, LoRA, TensorRT,
W&B), ROS2 basics, Linux, git. This curriculum covers what the arm needs that APEX didn't teach
you: **3D geometry & kinematics, manipulation control, calibration, planning stacks, and robot
learning for manipulation.**

**How to use the keywords:** they're search seeds — paste into Google Scholar/YouTube/arXiv after
you finish my sources, to go deeper than I took you. If a keyword returns something that
contradicts this plan, bring it back and we argue about it.

---

## The four spine resources (start all four now, pace them across the blocks)

1. **Modern Robotics — Lynch & Park** (free PDF + video course):
   https://hades.mech.northwestern.edu/index.php/Modern_Robotics — THE kinematics/dynamics text.
   Chapters 2–6 are Block A; 8–11 feed Block C.
2. **Robotic Manipulation — Russ Tedrake** (free web book + MIT lecture videos):
   https://manipulation.csail.mit.edu — THE manipulation course; geometric perception, grasping,
   force control, and learning chapters map 1:1 onto our stack.
3. **Articulated Robotics — Josh Newans** (YouTube + blog):
   https://articulatedrobotics.xyz — the best practical ROS2/URDF/ros2_control series that
   exists. Watch the whole "Making a Mobile Robot" + ros2_control series; translate to arm.
4. **LeRobot course & docs — Hugging Face**: https://huggingface.co/docs/lerobot +
   https://huggingface.co/learn/robotics-course — imitation learning → ACT → diffusion → VLA
   fine-tuning, all runnable. This is P1's toolchain; being fluent in it IS the paper.

---

## Block A — Foundations (Jul–Aug · gates Phase 0: sim-first)

### A1. Spatial math & kinematics (the non-negotiable math)
The arm is a chain of SE(3) transforms; everything — URDF, TF, IK, servoing, calibration — is
this math wearing different hats.
- **Sources:** Modern Robotics ch. 2–4 (config space, rigid-body motions, product of
  exponentials FK) + ch. 5–6 (Jacobians, IK); MR video lectures (Northwestern, YouTube). Gentler
  ramp: QUT Robot Academy "Robotic arms & kinematics" (Peter Corke, free videos:
  https://robotacademy.net.au). 3Blue1Brown "Essence of Linear Algebra" if any of it feels shaky.
  For the Lie-group view you'll want for papers later: Solà et al., *"A micro Lie theory for
  state estimation in robotics"* (arXiv:1812.01537) — read after MR ch. 3, not before.
- **Math to be able to DO on paper:** compose homogeneous transforms; convert
  rotation-matrix ↔ quaternion ↔ axis-angle; write the FK of a 3-link planar arm via PoE;
  compute a geometric Jacobian column; explain why J becomes singular at a straight-elbow pose.
- **Keywords:** `product of exponentials forward kinematics` · `geometric vs analytic jacobian` ·
  `damped least squares inverse kinematics` · `manipulability ellipsoid Yoshikawa` ·
  `SE(3) twist screw axis` · `micro lie theory robotics`
- ✅ **Ready when:** you can hand-derive the Jacobian of a 2-DoF arm and explain to a teammate
  what happens to IK solutions near a singularity and why we damp them.

### A2. ROS2 beyond the basics
- **Sources:** Articulated Robotics ROS2 series; official docs deep-dives: executors & callback
  groups, QoS (why camera topics drop and joint commands must not), lifecycle nodes, composition
  (https://docs.ros.org/en/humble/). Skim REP-105 (coordinate frames) and REP-103 (units) — we
  will enforce both.
- **Keywords:** `ROS2 executor callback group deadlock` · `QoS reliability durability sensor
  data` · `lifecycle node managed states` · `REP-105 frames base_link odom map` ·
  `tf2 time travel lookup transform`
- ✅ **Ready when:** you can explain why a subscriber with default QoS silently drops best-effort
  camera frames, and diagram our node graph with frame tree.

### A3. URDF/xacro, ros2_control, MoveIt2 (the stack's plumbing)
- **Sources:** Articulated Robotics URDF + ros2_control series (best available anywhere);
  control.ros.org docs (hardware_interface lifecycle, controller manager);
  MoveIt2 tutorials end-to-end (https://moveit.picknik.ai): Getting Started → Planning Around
  Objects → MoveIt Servo → Pilz Industrial Motion Planner → moveit_task_constructor.
- **Keywords:** `ros2_control hardware_interface write read loop` · `joint_trajectory_controller
  tolerances` · `MoveIt servo twist jogging` · `Pilz LIN PTP CIRC planner` · `SRDF planning group
  end effector` · `OMPL RRTConnect vs Pilz deterministic` · `moveit task constructor stages`
- ✅ **Ready when:** you can trace a joint command from "operator moves stick" → servo →
  controller_manager → hardware_interface → motor driver, naming every process boundary; and you
  know when to reach for Pilz vs OMPL and why competition moves prefer deterministic planners.

### A4. Isaac Sim / Omniverse / USD (your stated learning goal)
- **Sources:** Isaac Sim docs "Core Tutorials" + "ROS2 Bridge" series
  (https://docs.isaacsim.omniverse.nvidia.com); NVIDIA DLI free courses: *Getting Started with
  Isaac Sim*, *Synthetic Data with Replicator*; OpenUSD basics: NVIDIA's "Learn OpenUSD" free
  path (stages, prims, layers, references, variants). Then Isaac Lab docs intro (concept only —
  RL usage is Phase 5).
- **Keywords:** `OpenUSD stage layer composition arcs` · `Isaac Sim articulation root joint
  drive stiffness damping` · `Isaac Sim ROS2 bridge action graph` · `Replicator domain
  randomization writer` · `Isaac Sim URDF importer fixed base` · `PhysX solver iteration
  articulation`
- ✅ **Ready when:** you can import our URDF, wire joint states/commands over the ROS2 bridge,
  and render a randomized panel dataset with Replicator — this *is* Phase 0's deliverable, so
  the study and the build are the same hours.

---

## Block B — Perception & calibration (Sep–Oct · gates Phase 1: hardware bring-up)

### B1. Camera geometry & calibration
- **Sources:** *First Principles of Computer Vision* (Shree Nayar, Columbia — YouTube series:
  image formation, pinhole model, calibration, stereo) — the clearest treatment on the internet;
  Cyrill Stachniss photogrammetry lectures for bundle-adjustment depth; OpenCV calibration docs
  (ChArUco). Hand-eye: the classic AX=XB problem — read the `easy_handeye2` README + Tsai-Lenz
  paper summary.
- **Math:** pinhole projection matrix K[R|t]; reprojection error; what solvePnP solves; AX=XB
  structure of hand-eye.
- **Keywords:** `pinhole intrinsics extrinsics reprojection error` · `charuco calibration
  opencv` · `hand-eye calibration AX=XB Tsai Lenz Daniilidis` · `eye-in-hand vs eye-to-hand` ·
  `solvePnP IPPE_SQUARE aruco pose ambiguity`
- ✅ **Ready when:** you can explain why a 2 mm extrinsic error at the wrist becomes a task
  failure at the fingertips, and run our full calibration procedure from a written runbook you
  authored.

### B2. RGB-D, stereo, point clouds
- **Sources:** RealSense/OAK-D docs (depth modes, filters, failure cases — sunlight!); Tedrake
  ch. on geometric perception (point clouds, ICP); NVIDIA **FoundationStereo** (zero-shot stereo
  depth, 2025) — relevant because IR-pattern depth cameras degrade outdoors, which is exactly
  where we live.
- **Keywords:** `realsense outdoor sunlight depth failure` · `FoundationStereo zero shot depth` ·
  `ICP point to plane registration` · `depth camera error model quadratic range`
- ✅ **Ready when:** you've characterised our actual camera's depth error vs distance/lighting on
  a table you measured, and it's a figure in the textbook (rule R3).

### B3. Fiducials, 6-DoF object pose, detection
- **Sources:** ArUco/AprilTag original papers (skim) + pose-ambiguity issue (IPPE); NVIDIA
  **FoundationPose** (CVPR 2024 — model-based novel-object pose+tracking; our panel elements
  have CAD, which is exactly its use case); MegaPose as the render-and-compare alternative;
  YOLO fine-tuning you already know; SAM2 docs for promptable segmentation.
- **Keywords:** `FoundationPose model based pose tracking CAD` · `MegaPose render and compare` ·
  `apriltag vs aruco accuracy` · `planar tag pose ambiguity IPPE` · `synthetic to real detector
  fine tuning`
- ✅ **Ready when:** given the panel CAD + one wrist image, you can produce a 6-DoF panel pose
  and defend its error bars.

---

## Block C — Manipulation & control (Oct–Nov · gates Phase 2 skills work)

### C1. Velocity control & visual servoing
- **Sources:** resolved-rate control (MR ch. 6.3 / QUT videos); **Chaumette & Hutchinson,
  "Visual Servo Control Part I & II"** (IEEE RAM tutorials — the canonical IBVS/PBVS papers,
  very readable); MoveIt Servo source walkthrough (it's short — read the code).
- **Math:** interaction matrix L for a point feature; the IBVS control law v = -λ L⁺ e; why
  IBVS is robust to calibration error and PBVS isn't (and vice versa for trajectory shape).
- **Keywords:** `image based visual servoing interaction matrix` · `position based visual
  servoing comparison` · `resolved rate motion control singularity robust` · `visual servoing
  eye in hand camera velocity twist`
- ✅ **Ready when:** you can write the IBVS loop for centering an ArUco tag in the wrist camera
  on a whiteboard, then (rule R1) type it into the stack and watch it converge in sim.

### C2. Contact, compliance, insertion (the plug/RJ-45/hose skill)
- **Sources:** Tedrake force-control chapter; impedance vs admittance: Hogan's idea explained —
  find a modern survey (`impedance admittance control comparison survey`); peg-in-hole
  literature: classic remote-center-of-compliance + spiral search strategies; current-based
  contact detection (motor current ∝ torque — you'll build this from our drivers' telemetry).
- **Math:** mass-spring-damper target dynamics F = K·Δx + B·Δẋ; why admittance control on a
  stiff position-controlled arm is the practical choice for us; wrench transforms between frames.
- **Keywords:** `impedance vs admittance control stiff robot` · `peg in hole spiral search
  compliance` · `remote center of compliance insertion` · `current based joint torque estimation
  contact detection` · `operational space control Khatib`
- ✅ **Ready when:** you can explain the full insertion strategy — approach → contact detect →
  spiral search → compliant seat — and state what each stage senses and what it commands.

### C3. Grasping & behavior trees
- **Sources:** Tedrake grasping chapters (antipodal grasps, friction cones — enough theory to
  design the gripper fingers rationally); **Colledanchise & Ögren, "Behavior Trees in Robotics
  and AI"** (free on arXiv: 1709.00084) — read ch. 1–3 + reactive patterns;
  BehaviorTree.CPP v4 docs + Groot2.
- **Keywords:** `antipodal grasp friction cone force closure` · `behavior tree reactive fallback
  robotics` · `BT vs finite state machine robustness` · `BehaviorTree.CPP reactive sequence
  halting`
- ✅ **Ready when:** you can sketch the IDMO mission as a BT with recovery branches and defend
  every fallback node choice.

### C4. Teleop that wins competitions
- **Sources:** **GELLO** paper + site (arXiv:2309.13037, https://wuphilipp.github.io/gello_site/,
  code: github.com/wuphilipp/gello_software) — kinematically-matched leader arm, <$300 BOM; ALOHA
  paper (action chunking context + teleop rig design); predictive display / latency-compensation
  literature (skim — becomes P5 material).
- **Keywords:** `GELLO leader follower teleoperation` · `ALOHA low cost bimanual teleop` ·
  `teleoperation latency predictive display` · `shared autonomy assisted teleoperation`
- ✅ **Ready when:** you've decided gamepad vs GELLO vs both for IRC, from actual side-by-side
  task-time trials, logged as a decision.

---

## Block D — Robot learning for P1 (Nov–Dec · gates the P1 paper sprint)

You know deep learning; this block is *robot* learning — policies, not perception.
- **Sequence & sources:**
  1. Imitation learning fundamentals: behavior cloning, distribution shift, DAgger (Tedrake
     learning chapter; Levine CS285 lecture 2 only).
  2. **ACT** — action chunking transformers (ALOHA paper §method) — why chunking beats
     single-step BC.
  3. **Diffusion Policy** (Chi et al.) — the strongest small-data baseline; understand
     denoising as trajectory sampling.
  4. **VLAs**: OpenVLA paper (arXiv:2406.09246) → π0 & π0.5 (Physical Intelligence posts/papers,
     open-sourced via OpenPI) → **SmolVLA** (small, LeRobot-native — our primary fine-tune
     target) → **GR00T N1.5** (open weights, LeRobot-supported, trained heavily on synthetic
     Omniverse data — the NVIDIA-ecosystem tie-in for our story).
  5. **MimicGen** (arXiv:2310.17596) — demo multiplication: ~200 teleop seeds → 50k synthetic
     episodes via SE(3) warping of object-centric segments. This is how a student team gets
     big-data results from small-data effort; core P1 technique.
  6. LeRobot hands-on throughout: dataset format, training ACT/diffusion/SmolVLA, eval harness.
- **Keywords:** `behavior cloning distribution shift DAgger` · `action chunking transformer
  temporal ensemble` · `diffusion policy visuomotor` · `OpenVLA LoRA fine tune 7B` · `pi0 flow
  matching action expert` · `SmolVLA asynchronous inference` · `GR00T N1.5 FLARE DreamGen` ·
  `MimicGen data generation SE(3)` · `LeRobot dataset v2 format` · `vision language action model
  evaluation benchmark`
- **P6-candidate side-thread** (reading only until the Oct hardware gate — PLAN §8):
  `IKFlow generative inverse kinematics` · `residual learning robot kinematics calibration` ·
  `learned forward kinematics flexible manipulator` · `robot calibration neural network backlash`
- ✅ **Ready when:** you can defend P1's experiment table to a reviewer: which baselines
  (classical / ACT / Diffusion Policy / SmolVLA / GR00T-N1.5-finetune), what metrics, how many
  seeds/episodes, and what claim the evidence supports.

---

## Standing math thread (all blocks, low dose)

- Probability for robotics: Barfoot, *State Estimation for Robotics* (free PDF) ch. 1–4 — read
  slowly; feeds calibration and any future estimation work.
- Optimization: nonlinear least squares, Gauss-Newton/LM (Stachniss lectures) — under
  calibration, PnP, and cuRobo alike.
- **Keywords:** `gauss newton vs levenberg marquardt` · `nonlinear least squares robotics` ·
  `barfoot state estimation pdf`

## Watchlist (know these exist; adopt when the plan says)

- **cuRobo / Isaac ROS cuMotion** — GPU motion planning as a MoveIt2 plugin; Phase 3 upgrade
  (keywords: `cuRobo GPU motion generation` · `cuMotion MoveIt2 plugin`).
- **Gemini Robotics / Gemini Robotics On-Device** — closed, but the capability bar to cite in
  papers (keyword: `Gemini Robotics on-device VLA`).
- **vla-eval** — unified VLA evaluation harness; check before building P1's eval from scratch.
- Genesis / ManiSkill3 / RoboCasa — other sims/benchmarks; we stay on Isaac, but P1's related-
  work section needs them (keyword: `manipulation benchmark simulation 2026`).
