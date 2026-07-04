# Project Vanguard — Arm Autonomy: 2-Year Master Plan (Jul 2026 → Jul 2028)

**Owner:** Krithin Poola, Autonomous Lead, Project Vanguard (BITS Pilani Hyderabad)
**Scope:** Everything arm — manipulation autonomy, arm perception, arm teleop, arm sim, and the
interfaces to mechanical (arm hardware) and to the nav/comms subteams.
**North star:** Win IRC 2027. Build the world's best student rover-arm autonomy stack by mid-2028,
measured by competition results and published research — not vibes.

---

## 0. Working agreement (standing rules — bind every session, every phase)

- **R1 — Krithin types everything.** Claude provides complete reference code, designs, and
  reviews; nothing enters the repo that Krithin didn't type himself. (Same agreement as APEX;
  teammates write their own subsystems under the same spirit.) Claude may be explicitly
  commanded to fix a specific bug directly; Krithin reviews the diff.
- **R2 — Theory before build.** No phase begins until its curriculum block (`CURRICULUM.md`) is
  passed: Claude delivers a theory brief + the block's "ready when" check at phase start;
  Krithin studies in parallel and clears the gate. Learning is a deliverable, not overhead.
- **R3 — The textbook grows with the build** *(amended 2026-07-02: Claude authors it)*. A LaTeX
  textbook (`docs/textbook/`, same practice as APEX/ATOM) is maintained in parallel for every
  phase — theory learned, decisions made, mistakes and their root causes, with figures/plots/
  photos. **Claude writes the textbook and all documentation directly** (R1 does not apply to
  docs — it covers implementation code only). Claude's standing duty: capture textbook-worthy
  moments (a result, a failure with a lesson, a design decision, a first success) in the same
  session they happen; Krithin reads chapters as part of each phase's R2 gate.

## 1. What "best in the world" means (measurable)

"Beat ETH Zurich" needs translation: ETH doesn't field a team at these rover comps. The teams that
actually define world-class here are **Missouri S&T MRDT** (URC 2025+2026 champion), **Monash Nova
Rover**, **EPFL Xplore**, **AGH Space Systems** (Kraków), **ITU Rover** (Istanbul), and **Team
Anveshak** (IIT Madras — the domestic benchmark). ETH's relevance is as the *research* benchmark
(RSL — legged/space robotics, sim-to-real). So the goal splits cleanly:

| Axis | World-class bar | Our 2-year target |
|---|---|---|
| Competition | URC/ERC podium | **Win IRC 2027**; ERC 2027 finals + top-3 maintenance task; URC 2028 finals |
| Autonomy | Most teams teleop the arm. Fully autonomous panel servicing is rare even at ERC | Autonomous IDMO/maintenance task by ERC 2027; every arm task has an autonomous mode by 2028 |
| Research | RA-L / ICRA / IROS papers from student teams are rare | **5 publishable units by mid-2028** (§8): P1 submitted Dec 2026, P2 by end of spring 2027 semester, 2 flagship-quality among the five |
| Funding | Top teams run 6-figure (USD) budgets on sponsor networks | Grant+sponsor flywheel running by mid-2027: RESPOND proposal in, ≥3 in-kind sponsors, cash sponsorship deck live (§11) |
| Engineering | CI, sim regression, digital twin, real telemetry review — most student teams have none of this | Full industry-grade workflow from month 1 (§9) |

The honest gap analysis: top teams win on **reliability and operator skill**, not exotic autonomy.
The stack that wins IRC 2027 is a boringly reliable teleop arm with assistive autonomy. The stack
that makes us world-best by 2028 adds genuine autonomy on top of that reliable base. Don't invert
the order.

### 1.1 Know thy enemy — the benchmark teams and their open code

| Team | Credentials | What's public / what to study |
|---|---|---|
| **Missouri S&T MRDT** | URC champion 2025 **and** 2026 (+2017) | github.com/MissouriMRDT — `Autonomy_Software` (modern C++, deliberately **non-ROS** custom architecture), `RoveComm` (custom UDP protocol), UE5-based simulator. Lesson: they win on ruthless reliability + mission ops, not framework fashion. Study their ops discipline; don't copy the no-ROS choice (our research goals need the ROS/Isaac ecosystem) |
| **EPFL Xplore** | **ERC 2025 champion** | github.com/EPFLXplore — **`ERC_HD` is their robotic-arm codebase (C++, actively developed — updated Jun 2026)**, plus `ERC_CAMERAS`, `ERC_NAV`, LIO-SAM forks. The single most relevant open repo to this plan: read their HD architecture, issues, and commit history before designing ours |
| **STAR Dresden** | ERC 2025 2nd | Watch their maintenance-task runs; ERC publishes score breakdowns |
| **AGH Space Systems** | ERC 2025 3rd, perennial podium | Longest ERC track record; their PIMA-equivalent presentations are public on YouTube |
| **Monash Nova Rover** | URC 2026 2nd, 3 podiums in 5 yrs | github.com/MonashNovaRover — ROS2 + Nav2 stack (closest architecture to ours at the top level) |
| **Team Anveshak (IIT Madras), Team Vicharaka (IISc)** | The domestic bar; Vicharaka strong at IRC 2026 (Manipal) | Their IRC runs are on YouTube; we'll meet them at Udupi |

**Actions (Phase 0):** (a) Explore-agent sweep of `ERC_HD` + `Autonomy_Software` → 1-page "how
they win" memo per team, into the textbook; (b) pull the IRC 2026 final scoreboard + award list
(SPROS posts them on Instagram/site) and score-decompose where the winners' points came from;
(c) watch 3 URC SAR videos from finalist teams — that's the bar our SDDR video must clear.

**NASA's open-source rover (reviewed):** `nasa-jpl/open-source-rover` + `osr-rover-code` — JPL's
build-it-yourself 6-wheel rocker-bogie (COTS parts, ROS2, Python; v4.1.0 released Feb 2025,
actively maintained, 530★). **Honest assessment for us:** no arm, Foxy-era Python nodes — it's a
*chassis/bringup reference for the wider Vanguard team* (rocker-bogie geometry, drive/corner
kinematics, clean bringup docs), not an arm-autonomy source. The more interesting JPL repo for
this subteam is **`nasa-jpl/rosa`** — an LLM agent that introspects and operates ROS systems in
natural language (see `TOOLING.md`).

---

## 2. Competition landscape

### 2.1 Priority three — deep-read summaries (from the rulebooks)

#### IRC — International Rover Challenge (SPROS, India) — **PRIMARY TARGET**
- **Cadence (from IRC 2026):** registration 12 Sep–20 Oct; SDDR report+video due ~20 Nov; top 26
  (incl. 3 non-Asian wildcards) advance; finals 28 Jan–2 Feb in Udupi, Karnataka. Expect IRC 2027
  on the same cadence — **SDDR ~Nov 2026, finals ~Jan/Feb 2027. That is ~7 months away.**
- **Rulebook:** https://roverchallenge.org/wp-content/uploads/2025/10/IRC-2026-Rulebook.pdf
  (local copy saved; watch https://roverchallenge.org/irc/ for the 2027 edition ~Sept 2026)
- **Constraints:** rover ≤65 kg deployed / 85 kg all fielded parts, ≤1.5×1.2 m footprint (no height
  limit), ≤500 m from base station, no line-of-sight ops, unlicensed bands only (5.8 GHz
  recommended, congested-RF resilience is explicitly a judged part of the challenge), budget cap
  ₹20L, kill switch mandatory, 30-min missions, interventions cost 20% each (max 2/mission),
  mission aborted if 0 points in first 10 min, must hit 30% of points by 20 min to use full 30.
- **Missions and what the arm owns:**
  - **ABEx (Astrobiology Expedition):** subsurface sample ≥10 g from ≥10 cm depth, sealed in a
    cache tube, onboard analysis (temp/humidity/pH/pressure + one life-detection assay), panoramas
    + documentation, 5-page report in 30 min after mission. *Arm involvement: sampling mechanism
    (scoop/auger — decide with mech whether it's arm-mounted or a dedicated module), and the cache
    must be designed for later retrieval by the arm in RADO.*
  - **RADO (Reconnaissance & Autonomous Delivery):** 10 min recon (photograph + GPS-tag scattered
    objects; may store one object in a cache — gripping-carry not allowed), then 20 min
    pick-up-and-deliver. Objects: hand tools, containers, rocks ≤5 kg, graspable diameters ≤7 cm,
    up to 40×40×40 cm. **Pickup may be teleop, but delivery must be autonomous for full points —
    teleop delivery scores 50%.** This one rule is the single biggest arm-adjacent points lever in
    the competition. Delivery mode must be declared before finals.
  - **IDMO (Instrument Deployment & Maintenance):** the pure arm mission. Published op list: pick
    up a cache (handle ≥10 cm long, ≤5 cm dia, ≤5 kg) and carry it to the panel; open/close a
    drawer and place the cache inside; push buttons; flip switches; turn knobs; operate a joystick;
    undo latches; open panels; **insert a 3-pin plug into a standard socket**. Deployment leg:
    place cache components in a designated pattern/orientation, then read a code/pattern/text off
    the panel via the video feed and submit it. Panel height ≤1.5 m. Sub-missions attemptable in
    any order, points per sub-mission.
  - **PIMA / BPP / Exhibition:** static assessments — systems-engineering presentation, business
    plan, rover showcase (50 pts). Not arm scope, but SDDR + PIMA quality is what gets us to Udupi
    at all.

#### ERC — European Rover Challenge (Poland, on-site edition)
- **Cadence:** finals early Sept (ERC 2026: 4–6 Sept, Kielce). Applications open ~Dec–Mar. **First
  realistic entry: ERC 2027** (2026 qualification already closed). Some editions also run a
  **remote edition** on a hosted Leo Rover — cheap way to compete early; check when 2027 docs drop.
- **Docs:** https://roverchallenge.eu/competitor-zone/ — 2026 on-site files:
  https://drive.google.com/drive/folders/1txkq-1_6nlA_hwPbyGS6wdTtF9tjuSCb
- **Tasks:** Science (surface+subsurface sampling, in-situ measurement, documentation),
  **Maintenance** (electrical panel: set switches, measure electrical parameters, power an
  electromagnetic lock, **insert an RJ-45 plug**, observe feedback; panel carries **ArUco markers
  explicitly so the arm can operate autonomously — autonomous execution scores higher**),
  Collection/Probing (fetch caches, place in onboard container in required orientation, deliver),
  Traverse/Navigation (staged autonomy), Presentation. ERC is the most autonomy-weighted of the
  three and the natural stage for our autonomous-manipulation ambitions.

#### ARC — Australian Rover Challenge (ARCh, Adelaide University)
- **Cadence (from ARCh 2026):** finals **26–29 March** at the EXTERRES Analogue Facility,
  Roseworthy Campus, Adelaide — a purpose-built simulated **lunar** environment. Qualification
  is staged: **CDR due ~29 Oct** of the prior year, **SAR due ~11 Feb**, Cost Report ~11 Mar.
  For ARCh 2027 that means CDR lands in the same window as the IRC SDDR — plan both documents
  together (large content overlap).
- **Docs:** https://set.adelaide.edu.au/atcsr/australian-rover-challenge/information-for-teams
  (rules + task descriptions); 2026 participant handbook saved locally. Indian teams already
  compete here (2026 field: Australia, India, Indonesia, Kazakhstan, Poland).
- **Theme:** lunar ISRU — establish an in-situ resource-utilisation outpost. Four scored field
  tasks (2026 edition):
  - **Post-Landing Task:** systems check on a lander, relay damage to judges, navigate to supply
    caches past obstacles, initiate a start-up protocol, **connect a propellant hose** — the
    arm-heavy task (inspection, cache handling, connector mating).
  - **Space Resources Task:** collect **icy regolith** samples (freezer storage provided) —
    excavation/sampling tooling + handling.
  - **Excavation & Construction Task:** regolith excavation and construction ops — primarily a
    dedicated excavation tool, but manipulation-adjacent.
  - **Mapping & Autonomous Task:** autonomous traversal + mapping (nav subteam leads; arm idle).
- **Why it fits us:** lunar ISRU tasks diversify the skill set beyond Mars-yard panel work, the
  March slot chains cleanly after IRC (rover already integrated and rehearsed), and it's the
  URC-family circuit — results there are internationally legible.

### 2.2 Other competitions (scanned; calendar options)

| Competition | Where/when | Notes |
|---|---|---|
| **URC** — University Rover Challenge | MDRS, Utah, finals ~late May–early Jun | The flagship. 116 teams → 38 finalists in 2026 via SAR (report + demo video, due ~Feb–Mar). Equipment Servicing task = joysticks, buttons, switches, knobs, screws, board swaps via connectors, hand cranks. Realistic first entry: **URC 2028** (SAR Feb 2028) — a URC-ready rover 4 weeks after IRC 2027 is a gamble. |
| **CIRC** — Canadian International Rover Challenge | Drumheller, Canada, ~early Aug | URC-family tasks. Option for 2028 if budget allows. |
| **Anatolian Rover Challenge** | Istanbul, ~July | Narrative Moon/Mars rescue missions; publishes an open rover-comms protocol (RSCP, github.com/anatolianroverchallenge/rscp). Optional July slot if ERC prep allows. |
| **ISRO IRoC-U** | India (URSC, Bengaluru), cycle Dec→Aug | 2026 theme: swarm/autonomous exploration, no GNSS. ₹27L prize pool, national visibility, near-zero travel cost. **Watch for IRoC-U 2027 announcement (~Oct–Nov 2026)** — strong fit for the nav subteam; arm involvement depends on theme. |
| **IRDC** (SPROS, online) | design-only, part of SPROS Week | Cheap entry for juniors; feeds IRC pipeline. |
| **World Rover League (WRL)** | https://roverchallenge.org/wrl/ | SPROS's cross-event league — verify how IRC results feed it. |
| **UKSEDS Olympus Rover Trials** | UK | Entry-level; useful only as a freshman training target. |

**Recommended competition sequence:**
IRC 2027 (Jan) → ARC 2027 (Adelaide, Mar — CDR Oct 2026, SAR Feb 2027) → ERC 2027 (Sept) →
IRC 2028 (Jan) → ARC 2028 (Mar) → URC 2028 (May–Jun) → ERC 2028.
IRoC-U in parallel if the 2027 theme fits. One competition per quarter max — every comp costs ~6
weeks of team focus. Note the Jan→Mar chain is tight: the ARC SAR (~11 Feb) falls two weeks
after IRC finals, so its content must be drafted in December from IRC rehearsal footage.

### 2.3 The common arm task, distilled

Across IRC/ERC/URC/ARC the arm work collapses into six reusable **skills**:

1. **Grasp & carry** — handles, tools, rocks, caches (≤5 kg, ≤7 cm grasp features).
2. **Panel operations** — buttons, toggles, knobs, joysticks, latches, drawers, hand cranks.
3. **Peg-in-hole insertion / connector mating** — 3-pin plug (IRC), RJ-45 (ERC), board
   connectors (URC), propellant hose (ARC). The hardest skill; needs compliance + visual
   servoing.
4. **Place with orientation** — caches in patterns, containers in required orientation.
5. **Sampling support** — scoop/auger interface, cache seal/handoff.
6. **Read & report** — OCR/codes off panels through the arm camera.

Build these as competition-agnostic, behavior-tree-composable skills and every new rulebook
becomes a re-orchestration, not a rebuild. This is the architectural bet of the whole plan.

---

## 3. What winning IRC 2027 actually requires

Working backwards from the rulebook:

- **Get selected:** SDDR (report + 5-min video) ~20 Nov 2026 must show an *integrated, tested*
  rover — not renders. Only top 26 go. The SDDR is a deliverable with a deadline sitting exactly
  when we'll want to be heads-down building. Assign an owner now; draft it from our real test
  footage (this is where the weekly integration videos in §9 pay off twice).
- **Survive the point-rate rules:** 0 points in 10 min = mission aborted; <30% at 20 min = mission
  ended. So the operator playbook must front-load guaranteed points (easiest sub-missions first),
  and every skill needs a fast teleop fallback. Rehearse pacing with a shot clock.
- **Exploit the autonomy differential:** RADO autonomous delivery = 100% vs 50% points. If our
  autonomous delivery is even 70% reliable, it beats perfect teleop. This is where nav + arm
  integrate: autonomous drive-to-GPS + arm place/drop. Decide the declared mode by Jan 1 based on
  rehearsal stats, not hope.
- **IDMO = deterministic teleop + assists.** At IRC level, full panel autonomy is not required to
  win — a great operator with camera-frame Cartesian jog, click-to-align on ArUco/detected
  elements, and compliant insertion will outscore a flaky autonomous attempt. Autonomy assists,
  human decides. (Full autonomy is the ERC 2027 goal, not the IRC 2027 gamble.)
- **Interventions discipline:** 20% each. Reliability engineering (watchdogs, brownout protection,
  E-stop recovery, comms failover) is worth more than any single feature.
- **Comms is a scored adversarial environment:** congested 5.8 GHz, no interference complaints
  entertained. Arm teleop dies with bad video. Coordinate with comms subteam on: H.265 hardware
  encode, adaptive bitrate, multi-camera priority switching, and a **low-bandwidth arm mode**
  (pose telemetry + wireframe render instead of video) as the degraded fallback. That fallback is
  also secretly an autonomy forcing-function.

---

## 4. The Vanguard arm stack (architecture)

Platform: **Ubuntu 22.04 + ROS 2 Humble** for the IRC 2027 season. (Humble hits EOL May 2027 —
plan the **Jazzy/Ubuntu 24.04 migration for Mar–Jun 2027**, between IRC and ERC. Pin everything
in Docker so the migration is a base-image bump, not an archaeology dig.)

```
┌─────────────────────────── Operator Station ───────────────────────────┐
│ Foxglove (telemetry/plots) + custom teleop UI (video, arm jog, skills) │
│ Gamepad + GELLO-style kinematically-matched leader arm (<$300 BOM —    │
│ intuitive teleop AND the LeRobot demo-collection rig) · SpaceMouse opt │
│ mission shot-clock · points tracker                                    │
└──────────────────────────────┬─────────────────────────────────────────┘
                        WebRTC/GStreamer video + rosbridge/zenoh telemetry
┌──────────────────────────────┴─────────────────────────────────────────┐
│ ROVER (Jetson Orin)                                                    │
│  Task layer:   BehaviorTree.CPP v4 skills (grasp, panel-op, insert,   │
│                place, sample-assist, read-code) + mission orchestrator │
│  Motion:       MoveIt 2 (OMPL + Pilz industrial planner) ·             │
│                moveit_servo for teleop/visual-servo · collision scene ·│
│                cuMotion/cuRobo GPU planning (Phase-3 upgrade, MoveIt   │
│                plugin — same interfaces)                               │
│  Perception:   ArUco/AprilTag (GPU, isaac_ros) · YOLO det + SAM2 seg · │
│                FoundationPose 6-DoF (panel elements, caches) ·         │
│                eye-in-hand (wrist) + eye-to-hand (mast) RGB-D ·        │
│                FoundationStereo fallback for outdoor depth (IR-pattern │
│                depth degrades in sunlight — our default condition)     │
│  Control:      ros2_control hardware_interface → motor drivers ·       │
│                joint_trajectory_controller + velocity ctrl for servo · │
│                current-based contact detection · soft limits, watchdog │
└─────────────────────────────────────────────────────────────────────────┘
        ▲ same interfaces, swapped bottom layer ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ Isaac Sim digital twin: arm + gripper URDF, IDMO panel replica, yard   │
│ terrain · ROS 2 bridge · Replicator synthetic data · Isaac Lab RL envs │
└─────────────────────────────────────────────────────────────────────────┘
```

Design rules:
- **Sim and real expose identical ROS 2 interfaces.** Every skill runs unmodified against Isaac
  Sim or hardware. This is what lets us build for 2 months before the arm exists, and regression-
  test forever after.
- **Every autonomous skill has a teleop twin** reachable in one button press mid-execution.
- **Perception is layered:** fiducials (ArUco — ERC gives them to you) → learned detection →
  model-based 6-DoF refinement. Each layer degrades gracefully to the one below.
- **Insertion = compliance + servoing, not precision.** Spiral-search insertion with
  current-sensed contact and compliant fingertips/wrist beats chasing sub-mm calibration on a
  student-built arm that flexes.
- **Log everything:** every run (sim or real) writes an MCAP bag; weekly review ritual (§9).

---

## 5. Arm hardware requirements → mechanical team (DELIVER THIS WEEK)

The arm is being designed *right now*. Autonomy dies at design time, not integration time. Hand
mech a one-page interface spec covering, at minimum:

**Kinematics & reach**
- **6 DoF minimum** (5 cannot do arbitrary approach orientation for plug/RJ-45 insertion) + wrist
  roll with generous (ideally continuous) range.
- Reach: panel ops up to **1.5 m above ground** (IRC) and ground-level pickup, from the rover's
  deck height — verify the workspace envelope against both extremes with margin.
- Payload: **≥5 kg at working extension** (IRC cache spec) — specify at extension, not at base.

**Sensing & drives (non-negotiables)**
- **Joint-side absolute encoders** (≥14-bit) on every axis — motor-side-only encoders + belts =
  unusable for autonomy. Homing-free startup required.
- Per-joint **current sensing** exposed to software (contact detection, grasp verification).
- Backlash budget: ≤0.5° per joint (cycloidal/harmonic or preloaded belts at distal joints).
- Position AND velocity control modes at the driver level, ≥100 Hz command rate (500 Hz+ ideal);
  drivers speak CAN (preferred) with a documented protocol — no closed vendor black boxes.

**Integration**
- Rigid **wrist camera mount** (RGB-D, USB3 — routed with strain relief and service loop) +
  **mast/chassis camera** with full arm-workspace view.
- Standard tool flange; gripper = separately swappable module. Gripper v1: parallel jaw, ≥80 mm
  stroke, compliant/high-friction fingertips, **hook feature for ≥10 cm handles**, current-based
  grip feedback.
- E-stop chain integration: arm power cut independently switchable; joints must not collapse on
  power loss where a human could be underneath (brakes or self-locking gearing on shoulder).
- Mass: fits the 65 kg deployed / 85 kg total-fielded budget with the mission modules; arm
  swappable by 2 people in <10 min (rulebook allows reconfiguration between missions).
- **CAD → URDF pipeline commitment:** mech maintains the assembly such that we can export
  link-accurate URDF with real inertials (Onshape/SolidWorks → URDF exporter). Frozen joint
  placement + frame conventions agreed before detailed design.

Also decide jointly *now*: is ABEx sampling arm-mounted (scoop/auger tool on the flange) or a
dedicated module? Recommendation: **dedicated sampling module**, arm handles only the cache
handoff — decouples the two highest-risk missions.

---

## 6. Roadmap

Every phase opens with its theory gate (rule R2 — curriculum blocks in `CURRICULUM.md`:
A→Phase 0, B→Phase 1, C→Phase 2, D→P1 paper sprint) and closes with its textbook chapter
(rule R3).

### Phase 0 — Sim-first foundation (now → arm delivery, Jul–Aug 2026)
*Goal: when the arm arrives, software is waiting for it, not the reverse.*
- Week 1: interface spec to mech (§5) · register team intent for IRC 2027 the day the portal opens
  (watch site; early-bird discount) · dev environment standard (Ubuntu 22.04 + Docker devcontainer,
  ROS 2 Humble, single `vanguard_arm` monorepo, CI skeleton).
- URDF/xacro from mech's CAD (iterate as design evolves — this feedback loop also catches mech
  design errors early, e.g. self-collisions, unreachable panel poses).
- **Isaac Sim digital twin**: arm + gripper in an IDMO-panel scene; ROS 2 bridge; teleop the sim
  arm end-to-end from the operator UI. Build the IDMO panel and RADO objects in USD from the
  rulebook dimensions.
- MoveIt 2 up on the sim arm: planning scene, Pilz Cartesian moves, moveit_servo jogging.
- Skill framework: BehaviorTree.CPP scaffolding + the six skills (§2.3) as stubs; grasp & place
  working in sim.
- Operator station v0: Foxglove + gamepad teleop of sim arm; measure operator task times from day
  one (baseline metric).
- Team: recruit + onboard the arm autonomy squad (§9); Isaac learning path (§7) starts now.
- Research P1 rides this phase for free: the sim panel scenes + LeRobot-logged teleop demos ARE
  the P1 benchmark and dataset (§8). Faculty advisor secured by end of Aug (blocker for P1
  submission + RESPOND/NVIDIA grants). MathWorks/GitHub/AWS in-kind applications out this month.
- **Gate G0 (arm hardware arrives):** sim IDMO run — teleop operator completes ≥5 of the listed
  panel ops in sim within 15 min.

### Phase 1 — Hardware bring-up (Sep–Oct 2026)
- `ros2_control` hardware interface for the real drivers; joint calibration, soft limits,
  watchdogs, E-stop verification **before anything moves fast**.
- System ID: real joint velocities/accels, backlash map → update URDF + sim to match reality
  (sim-real gap measured, not assumed).
- Camera intrinsics + **hand-eye calibration** (easy_handeye2); repeatability audit: commanded vs
  measured EE pose across workspace.
- Teleop v1 on real arm: camera-frame Cartesian jog, speed scaling, singularity/limit guarding.
- First real grasps: cache-with-handle pickup, tool pickup, place in container.
- **Gate G1 (end Oct):** real-arm pick-and-place of an IRC-spec cache, 10/10 repeatable; teleop
  IDMO panel mock ≥5 ops.

### Phase 2 — IRC 2027 campaign (Nov 2026 → finals ~Jan/Feb 2027)
- **SDDR submission ~20 Nov** — owner assigned in Phase 0; video cut from rehearsal footage.
- **ARC 2027 CDR ~29 Oct** — written alongside the SDDR (same evidence base, different template);
  ARC SAR content drafted in December so only fresh footage is needed after IRC.
- Build the physical **IDMO panel replica** (buttons/switches/knobs/joystick/latch/drawer/3-pin
  socket, at 1.5 m) and RADO object set from the 2027 rulebook the week it drops; sim versions
  updated same week.
- Weekly full-mission dress rehearsals under competition rules (30-min clock, intervention
  penalties, base-station isolation, degraded comms drills). Track a points spreadsheet per run —
  the declared RADO delivery mode (autonomous vs teleop) is decided by this data by Jan 1.
- Autonomous delivery pipeline with nav subteam: GPS-goal drive + arm place/drop + release verify.
- Assistive autonomy for IDMO teleop: ArUco/detector-based **click-to-approach** (operator clicks
  panel element, arm servos to pre-contact pose, human finishes) — the highest points-per-
  engineering-hour feature in this plan.
- Insertion skill hardening: compliant fingertips + spiral search on the 3-pin plug; target ≥80%
  success in rehearsal or it stays teleop-only at finals.
- **P1 submitted by Dec 2026** (arXiv + RA-L/workshop, §8) — sim-only by design, so the IRC
  hardware crunch can't sink it; the VLA fine-tune/eval runs on the team desktop while hardware
  rehearsals own the arm.
- Code freeze 2 weeks out; freeze = operator training time, not feature time. Ship to Udupi with
  a full spares kit and a written per-mission operator playbook (sub-mission order, abort
  criteria, pacing against the 10/20-min rules).
- **Gate G2: IRC 2027 result. Target: win; floor: top-5 + highest IDMO score.**

### Phase 3 — ARC 2027 sprint + consolidation (Feb–May 2027)
- **ARC SAR ~11 Feb** (drafted in Dec, finalized with IRC footage) → **ARC finals late Mar,
  Adelaide**: Post-Landing task skills (lander inspection, cache handling, start-up protocol,
  **propellant hose connection** — a connector-mating variant of the insertion skill) + icy-
  regolith sampling handoff with mech's excavation tooling. Travel/visas booked by Dec.
- Two-week retrospectives after each comp; archive competition branches; publish season report.
- **ROS 2 Jazzy / Ubuntu 24.04 migration** (Humble EOL May 2027) in the April–May lull.
- ERC 2027 application (watch for docs ~Dec–Mar) · decide IRoC-U 2027 entry when theme drops.
- Begin the real autonomy push for ERC: FoundationPose-based panel-element 6-DoF, full
  maintenance-task behavior tree in sim (ArUco-guided), Replicator synthetic data for panel/cache
  detectors.
- **P2 (field systems paper) drafted in Feb from IRC data, submitted ~1 Mar (IROS 2027)**; ARC
  results added at camera-ready. RESPOND proposal + sponsorship deck out in Mar on the back of
  P1 + the IRC result (§11). P3 experiments (learned insertion) begin as the ERC autonomy push —
  same work, two outputs.
- **Gate G3 (May): ARC top-5 + best Post-Landing score among first-time entrants; autonomous
  maintenance task (switches + measurement + RJ-45) ≥70% success in sim, ≥50% on the physical
  replica.**

### Phase 4 — ERC 2027 (Jun–Sep 2027)
- ERC (early Sep): **run the maintenance task autonomously** — this is the season's headline goal
  and paper #1's field validation. Fall back per-element to teleop on failure (graceful autonomy).
- Optional: Anatolian Rover Challenge (Jul) only if ERC prep is ahead of schedule — it's a
  re-orchestration of existing skills, but July focus is scarce.
- **Gate G4: ERC finals; top-3 maintenance-task score; ≥50% of maintenance ops executed
  autonomously in the actual run.**

### Phase 5 — Learned skills + IRC 2028 (Oct 2027 → Feb 2028)
- **Isaac Lab RL workstream** (now that classical stack is solid): learned insertion policy
  (RJ-45/3-pin) with domain randomization, benchmarked against the classical spiral-search
  baseline — win or lose, that ablation is paper #2.
- Whole-mission autonomy rehearsals: IDMO start-to-finish autonomous in sim nightly (CI), weekly
  on hardware.
- IRC 2028 campaign (reuse Phase 2 playbook — it should cost half the effort this time).
- **P4 (dataset paper) submitted Sep–Dec 2027** — it assembles what the logging discipline has
  been accumulating all along; P3 revisions handled; P5 experiments (edge-VLA distillation or
  the operator study) run on IRC 2028 rehearsal infrastructure.
- **Gate G5: IRC 2028 — defend/win; ≥1 mission leg run fully autonomous at finals.**

### Phase 6 — URC + full circuit (Mar–Jul 2028)
- ARC 2028 (late Mar, Adelaide): defend/improve — CDR Oct 2027 + SAR Feb 2028 reuse the Phase 5
  pipeline; target podium + a fully autonomous Post-Landing attempt.
- URC 2028: SAR due ~Feb–Mar (prepared during Phase 5), finals late May–early Jun at MDRS, Utah —
  budget/visa planning starts Oct 2027 (§10).
- ERC 2028 application; CIRC optional.
- **P5 submitted Feb–May 2028** — completing the five; handoff documentation + succession (you
  graduate eventually — the stack shouldn't).
- **Gate G6: URC finals appearance + equipment-servicing top quartile; five publishable units
  submitted (≥2 accepted); the six skills all have autonomous modes with measured success
  rates.**

---

## 7. Isaac Sim / Isaac Lab / Omniverse — learning path

Untangling the names first:
- **Omniverse** = NVIDIA's platform layer: **USD** (Universal Scene Description — the scene file
  format everything shares), the RTX renderer, PhysX, and Nucleus (asset server). You don't
  "learn Omniverse" separately; you absorb it by using Isaac Sim. Do learn **USD basics** early —
  stages, prims, references, variants — everything in Isaac is a USD stage.
- **Isaac Sim** = the robotics simulator built on Omniverse. URDF import, sensors (RGB-D, lidar,
  IMU), ROS 2 bridge, **Replicator** (synthetic data generation with domain randomization).
- **Isaac Lab** = the robot-learning framework on top of Isaac Sim (successor to Orbit/
  IsaacGymEnvs): vectorized GPU-parallel environments, RL (PPO via rsl_rl/skrl), imitation
  learning. You write manager-based envs; it handles the thousand-arms-in-parallel part.

Sequence (start now; ~6 weeks part-time to productive):
1. Install Isaac Sim on the team RTX desktop (§10) — check the version compatibility matrix
   (Isaac Sim ↔ Isaac Lab ↔ driver) before installing anything; pin versions in the README.
2. Core tutorials: UI + USD stage → URDF import (use *our* arm the moment mech shares CAD) →
   articulations + joint drives.
3. **ROS 2 bridge**: drive the sim arm from the same `ros2_control`/MoveIt stack as hardware
   (topic-based bridge first; it's the industry-standard pattern and what §4 assumes).
4. Build the IDMO panel scene in USD; wire buttons/switches as articulated joints with sensors.
5. **Replicator**: randomized lighting/pose/texture renders of panel + caches → train the YOLO
   detector on synthetic, fine-tune on ~200 real images. (First taste of the sim2real loop.)
6. **Isaac Lab** (Phase 5, not before): manager-based env for peg insertion; PPO with domain
   randomization on physics + vision; export policy → ONNX → deploy behind the same skill
   interface as the classical version.
7. NVIDIA DLI free courses ("Getting Started with Isaac Sim", Isaac Lab robot learning) as
   structured onboarding for the squad — assign as onboarding homework with a demo-day.

Hardware note: Isaac Sim wants RTX + ≥12 GB VRAM for comfortable scenes; Isaac Lab training wants
24 GB (RTX 4090/5090 class). Your 5070 Ti laptop (12 GB) is fine for scene work and small-scale
Lab experiments; the team desktop (§10) carries training.

---

## 8. Research program — 5 papers in 24 months

**Target (set 2026-07-02): ≥5 publishable units by mid-2028 — the first submitted by Dec 2026,
the second by end of the spring 2027 semester.** Research is a funding instrument as much as a
scientific one (§11): every paper is a grant application exhibit, so every paper goes on arXiv
the day it's submitted.

**Calibration, stated honestly:** five *groundbreaking* papers in 2 years from a student team is
not a plan, it's a wish. Five *real, publishable, citable* units — two flagship-quality
(conference main track / RA-L), three solid (benchmark, dataset, workshop/field-report) — is
achievable *if* the research rides the competition infrastructure instead of competing with it.
Groundbreaking-ness comes from owning a niche, and we have a genuine one:

**The niche: foundation manipulation policies in the field.** The VLA (vision-language-action)
wave — OpenVLA (7B, Open X-Embodiment), π0/OpenPI (Physical Intelligence, flow-matching,
open-sourced), NVIDIA GR00T N1 (trained heavily on Omniverse synthetic data), SmolVLA
(lightweight, LeRobot-native, trainable on a single consumer GPU) — is trained and evaluated
almost entirely on *tabletop* manipulation in labs. Nobody has serious results on **planetary/
field manipulation**: outdoor lighting, dust, unstructured terrain, a flexing student-built arm,
degraded comms, safety-critical panel ops. "Do VLAs survive the field?" is an open question we
are uniquely instrumented to answer — we own a rover, a Mars yard schedule, an Isaac Sim twin,
and a competition calendar that forces real deployments. That question is the spine of the
program; the ecosystem (LeRobot for data/training, vla-eval-style harnesses for evaluation,
Isaac Lab for RL baselines) is mature enough that a student team can execute on it.

**Enabling decision (do this from day 1, costs almost nothing):** every teleop session — sim and
real — is recorded as **LeRobot-format demonstration episodes** in addition to MCAP bags.
Rehearsals thereby produce training datasets as a by-product. Rehearsals → data → papers →
grants → better rover. That loop is the whole strategy.

### The five papers

| # | Paper (working title) | What it needs | Submit | Venue (primary / fallback) |
|---|---|---|---|---|
| P1 | **"Do VLAs transfer to planetary manipulation?"** — Isaac Sim panel-servicing benchmark (IDMO/ERC panels, procedural randomization) + LeRobot demo dataset (**MimicGen-multiplied**: ~200 GELLO/sim teleop seeds → thousands of episodes via SE(3) demo warping) + evaluation ladder: classical MoveIt pipeline vs ACT vs Diffusion Policy vs SmolVLA fine-tune vs GR00T-N1.5 fine-tune (all LeRobot-native) | **Sim only — no hardware dependency.** Phase 0 scenes + teleop demos | **Dec 2026** (arXiv immediately) | RA-L (rolling) / Space Robotics Workshop @ ICRA 2027; stretch: ICRA 2027 (ddl ~15 Sep — only if Phase 0 lands early) |
| P2 | **Field systems paper** — the full open-source arm autonomy stack + IRC 2027 field results (skill success tables, failure taxonomy), ARC 2027 added at camera-ready | IRC 2027 deployment data | **Mar 2027** (spring semester) | IROS 2027 (ddl ~1 Mar) / i-SAIRAS-iSpaRo 2027 (ddl ~Jun, based on 2026 pattern) |
| P3 | **Sim-to-real learned insertion** — Isaac Lab RL policy + VLA fine-tune vs classical spiral-search compliance, on the real arm, across misalignment/lighting/latency. Honest negative results welcome; the ablation is the contribution | Real arm + Phase 3 autonomy stack | **Jun–Sep 2027** | CoRL 2027 (ddl ~Jun) / RA-L |
| P4 | **Dataset/benchmark release** — multi-competition field manipulation dataset: LeRobot teleop episodes (sim+real), MCAP logs, Replicator synthetic + real annotated panel/cache detection & 6-DoF pose | Accumulates automatically if the day-1 logging decision holds | **Sep–Dec 2027** | ICRA 2028 (ddl ~Sep 2027) / RA-L / NeurIPS D&B track |
| P5 | **Edge VLA or shared autonomy** — either "VLA at the edge": distill/quantize a fine-tuned policy to Jetson Orin for field manipulation with latency/success benchmarks, or an operator study on assisted teleop under degraded comms (we'll have unmatched operator-hours data) | Full 2027 season infrastructure | **Feb–May 2028** | IROS 2028 / RA-L / iSpaRo 2028 |

P1 is deliberately the sim-only paper so the end-of-2026 deadline cannot be hostaged by hardware
slips — and its artifacts (panel scenes, demo pipeline, evaluation harness) are exactly the
Phase 0/2 engineering we need anyway. P2's deadline (~1 Mar) sits between IRC and ARC; the paper
is drafted in Feb from IRC data.

### Rules of the program

- **Faculty advisor is a blocker — resolve by Aug 2026.** Needed for arXiv endorsement,
  co-authorship credibility, lab access, and as PI for RESPOND / NVIDIA academic grants (§11).
  Shortlist BITS Hyderabad robotics/CV faculty now.
- Every paper's experiments must double as competition hardening. No research that doesn't make
  the rover better.
- W&B for all training runs; MCAP + LeRobot logging from day one; a `research/` dir in the
  monorepo with one reproducible pipeline per paper.
- Authorship policy written down before P1 (contribution-based; advisor + core contributors) —
  cheap now, expensive later.
- Each submission triggers: arXiv upload + project-page update + a sponsor-facing one-pager
  (§11). Publications are fundraising ammunition; treat the pipeline that way.

---

## 9. Team, process, infrastructure

**Squad (arm autonomy), target 8–10 people:**
- Manipulation & controls (2): ros2_control, MoveIt, insertion, compliance.
- Perception (2): detectors, pose estimation, calibration, Replicator.
- Teleop & operator experience (1–2): UI, video pipeline, input devices, operator training
  program. (Deliberately a first-class role — operators win IRC.)
- Sim & infra (2): Isaac Sim scenes, digital twin parity, CI, logging, tooling.
- You: architecture, integration, gates, research direction.
Recruit 2–3 juniors per role area for succession; every senior has an apprentice by 2027.

**Process (the actual industry-standard part):**
- Monorepo, PR-only main, code review required, `main` always runs the sim mission.
- CI (GitHub Actions for build+unit tests on every PR; GPU jobs on Krithin's laptop via a
  nightly cron while docked — no self-hosted cloud runner): **nightly headless Isaac Sim mission
  regression** — sim IDMO run scored automatically, trend tracked. A regression in nightly score
  blocks merges. This single practice is rarer than any algorithm among student teams and
  compounds for two years. Heavy training jobs go to the BITS HPC as containerized batch jobs.
- Every hardware session produces an MCAP bag + a one-line log entry; weekly 30-min bag-review
  ritual (watch the worst failure of the week together).
- Every teleop session (sim and real) is additionally recorded as LeRobot-format demonstration
  episodes — the raw material for the VLA research program (§8) at near-zero marginal cost.
- Docs-as-you-go: `docs/` textbook chapters per subsystem (the APEX habit — it works), onboarding
  runbook, per-mission operator playbooks under version control.
- Definition of done for a skill = success-rate measured over ≥20 trials in sim AND ≥10 on
  hardware, logged in the skill scoreboard.
- **AI leverage everywhere it compounds:** Claude for rulebook diffing each edition (feed old+new
  PDF, get the delta), SDDR/report drafting from logs, code review, test generation, W&B run
  analysis. Time-sucks named this quarter — reports and debugging — are exactly what gets
  automated first.

**Cross-team interfaces:** written interface contracts with mech (§5), nav (autonomous-delivery
handoff: goal pose in map frame + arrival tolerance), comms (bandwidth budget per camera, arm
telemetry priority, degraded-mode spec). Review monthly.

**The recruitment engine (explicit goal: this team gets hired at top companies):**
What gets a student hired at NVIDIA/Physical Intelligence/Google DeepMind Robotics/Skild — or
ISRO, Skyroot, ideaForge at home — is *visible, verifiable artifacts in the exact stack industry
uses*, and this plan manufactures them deliberately:
- **Ecosystem fluency that reads on a resume:** Isaac Sim/Lab + cuMotion + GR00T fine-tuning
  (NVIDIA's entire robotics stack — they hire people who showcase it), LeRobot contributions
  (Hugging Face's robotics community is a hiring watering hole; upstream our dataset + a tutorial
  there), MoveIt2/ros2_control (every robotics company's baseline).
- **Public proof:** the open-source stack repo, the P1 benchmark site, arXiv papers with their
  names on them, competition results, and a per-member "what I built" page. GitHub stars and a
  dataset on the HF hub outperform GPA in robotics screening — everyone gets one flagship
  artifact they own end-to-end.
- **Legibility:** every member can rehearse a 5-minute deep-dive on their subsystem (the PIMA
  presentations double as interview prep). Post-competition blog posts per season.
- Track it: a `TEAM.md` ledger of member → artifacts → papers → placements. The placement list
  becomes the recruitment pitch for the next generation.

---

## 10. Budget & procurement (arm-autonomy scope, fits inside IRC ₹20L team cap)

| Item | Est. cost (₹) | When | Notes |
|---|---|---|---|
| RGB-D cameras ×2 (RealSense D435i/D455 or OAK-D Pro) | 60–120k | Now | Wrist + mast; buy same model ×2 for spares/parity |
| Jetson Orin NX 16GB carrier/devkit | 90–120k | Now | You know this platform cold from APEX — reuse everything |
| ~~Team RTX desktop~~ → **laptop + college HPC** (decided 2026-07-02) | 0 | — | Krithin's RTX 5070 Ti laptop (12 GB) runs Isaac Sim scenes, sim teleop, SmolVLA-class fine-tunes; heavy training (GR00T N1.5 fine-tune, MimicGen at scale, Isaac Lab RL) goes to the BITS HPC as batch jobs. Consequences: (1) nightly sim-regression CI runs on the laptop via cron/systemd-timer while it's docked, not a self-hosted runner; (2) HPC jobs need containerized (Apptainer/Singularity likely — verify what BITS HPC supports) training images from day 1; (3) revisit a team desktop only if HPC queue times start gating P1 |
| Gripper actuation + compliant fingertips (v1+v2) | 30–60k | Aug 2026 | With mech |
| IDMO panel replica + RADO object set | 15–25k | Nov 2026 | Rebuild per rulebook each season |
| Gamepads, SpaceMouse, operator peripherals | 15–25k | Aug 2026 | |
| GELLO-style leader arm (Dynamixel XL330s + 3D-printed links, matched to our arm's kinematics) | 25–35k | Sep 2026 (once arm kinematics freeze) | Doubles as teleop input AND LeRobot demo-collection rig; open design (github.com/wuphilipp/gello_software) |
| Wrist 6-axis F/T sensor | 150–400k | **Deferred to 2027, only if current-sensing proves insufficient** | Decide after Phase 2 data |
| Travel: Udupi (IRC) | team budget | Jan 2027 | Book early — peak season, rulebook explicitly warns |
| Travel: Adelaide (ARC) + Australian visas | team budget + sponsors | book Dec 2026 | Two international trips 8 weeks apart (IRC→ARC) — freight/carnet plan for the rover needed |
| Travel: Poland (ERC) | team budget + sponsors | 2027 | Sponsorship pipeline is a BPP/PIMA asset too |
| Travel: Utah (URC 2028) + US visas | large; start Oct 2027 | 2028 | Visa lead time from India is the real deadline |

---

## 11. Funding & sponsorship engine

Money follows evidence. The order of operations: cheap in-kind wins now → publications + IRC
result as proof → grants and cash sponsorships on the back of them. Assign a business/outreach
lead (non-engineer is fine — this is also exactly what IRC's BPP assessment scores, so the work
double-counts as competition points).

**Government / space-agency grants (the big, slow money):**
- **ISRO RESPOND** (isro.gov.in/SponsoredResearch.html) — ISRO's sponsored-research programme
  for academia: funds fellowships, materials, testing, minor equipment. **Requires a faculty
  PI** — the same advisor P1 needs (§8); frame the proposal around autonomous planetary
  manipulation / VLA field evaluation. Route through the BITS sponsored-research office.
- **IN-SPACe** student programmes + **Space Technology Incubation Centres (STICs)** — mentorship
  + facilities; watch their calls.
- **IRoC-U prize money** — ₹27L pool in the 2026 cycle; entering (if the 2027 theme fits) is
  simultaneously a funding play.
- BITS internal: institute/department student-project funds, and the Practice School network as
  an industry-contact channel.

**Corporate — in-kind first (apply this month, all are low-effort):**
- **MathWorks student competition programme** — sponsors rover competitions (ERC is on their
  list: mathworks.com/academia/student-competitions): software licenses, training, mentors.
  Submit the request form now.
- **NVIDIA**: Academic Grant Program (compute/hardware — faculty PI required, pairs with the
  RESPOND advisor); education discounts on Jetson; DLI credits. Our Isaac-Sim-heavy,
  GR00T-adjacent research story is exactly what their robotics education outreach wants to
  showcase — pitch it that way.
- Software/cloud in-kind: GitHub Education, AWS/GCP academic credits (train detectors/VLAs when
  the desktop is saturated), Foxglove (free team licenses for students), Altium/SolidWorks/Ansys
  education sponsorships (mech team shares the ask).
- **Intel RealSense / stereo-camera vendors** — student team hardware sponsorships in exchange
  for footage/logos.

**Corporate — cash (post-IRC 2027, with evidence in hand):**
- **Indian space & robotics startups**: Skyroot, Agnikul, Dhruva Space, Pixxel, Bellatrix,
  ideaForge — young companies with hiring needs and marketing budgets; a winning student team is
  cheap, targeted branding + a recruiting pipeline. Apollyon Dynamics is a natural first
  conversation (declare the conflict of interest openly and keep IP boundaries written).
- **CSR (Companies Act §135)**: large Indian firms must spend 2% of profits on CSR; education +
  technology-incubation qualify. Approach via the university (CSR money flows institution-to-
  institution far more easily than to a student club).
- Sponsorship deck with tiers (rover livery, base-station branding, jersey logos, recruiting
  access, demo days) — build it from IRC footage in Feb 2027; refresh per season.

**Community & alumni:**
- **BITSAA** (the BITS alumni association) — alumni grants and crowdfunding campaigns have funded
  BITS student teams before; a Mars-rover team with papers is an easy sell. Also Ketto/Milaap
  campaigns timed to competition news cycles (post-win > pre-season).
- **Travel grants**: IEEE RAS student travel awards (ICRA/IROS/iSpaRo), IAC student
  programmes — apply per accepted paper; this is how conference travel gets paid without eating
  the hardware budget.

**The flywheel, explicitly:** P1 on arXiv (Dec 2026) + IRC 2027 result (Feb) → sponsorship deck
+ RESPOND proposal (Mar 2027) → funded 2027-28 season → P2–P5 + ERC/URC results → larger grants.
Publications are not a side quest; they are the fundraising engine.

## 12. Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Arm hardware late or spec'd without autonomy needs | **High** — the default failure of student teams | §5 spec this week; sim-first Phase 0 means software doesn't idle; escalate to team lead if encoders/current-sensing get value-engineered out |
| IRC 2027 rulebook changes tasks vs 2026 | Medium | Skills (§2.3) are task-agnostic; rebuild panel replica the week the rulebook drops; AI rulebook diff |
| SDDR non-selection (top 26 only) | Low-Med | Treat SDDR as a first-class deliverable with an owner and two internal review passes; wildcard route doesn't apply to us (Asia) |
| Comms failure kills arm teleop at finals | Medium | Low-bandwidth arm mode; assists that need only telemetry; rehearse with throttled links |
| Autonomy gamble fails on the day | Medium | Declared-mode decision from rehearsal stats; per-element teleop fallback in every BT |
| Key-person risk (you, seniors graduating) | Certain, eventually | Apprentice model, textbook docs, recorded onboarding; succession is a Phase 6 gate |
| Isaac version churn breaks the twin | Medium | Pin versions; upgrade only in Phase 3/off-season windows |
| Burnout — 5 competitions + 5 papers in 24 months | **High** | One comp per quarter max; papers ride competition work (P1 sim-only, P4 auto-accumulating) rather than adding parallel workstreams; mandatory 2-week post-comp cooldowns; cut CIRC/Anatolian and P5 before cutting sleep |
| Paper rejections stall the count | Medium | arXiv on submission day (funders see output immediately); RA-L rolling resubmission; workshop fallbacks per paper; "5 submitted" is the controllable metric, acceptances follow quality |
| No faculty advisor by Sept | Medium | Blocks P1 endorsement + RESPOND + NVIDIA grants. Shortlist 3 BITS-H candidates in July; the pitch: a running rover, a data pipeline, and co-authorship on 5 papers costs them near-zero effort |
| VLA niche gets crowded | Medium | Field/planetary angle + competition deployments is the moat — labs can fine-tune models but can't easily field them; speed matters, hence P1 in 2026 |

---

## 13. This week

1. **Write and deliver the arm interface spec to mechanical** (§5). Book a 1-hour review with
   their lead. This is the highest-leverage hour of the entire plan.
2. Stand up the `vanguard_arm` repo: devcontainer (22.04/Humble), CI skeleton, README with the
   §4 architecture.
3. Order/requisition: RTX desktop, 2× RGB-D cameras, Orin devkit (§10).
4. Set a calendar watch: IRC 2027 registration (roverchallenge.org, ~Sept), **ARC 2027
   registration + CDR (set.adelaide.edu.au/atcsr — CDR ~late Oct 2026, registration opens
   earlier)**, ERC 2027 docs (roverchallenge.eu), IRoC-U 2027 (ursc.gov.in, ~Oct–Nov).
5. Install Isaac Sim on your laptop; do tutorials 1–3 of §7 with any 6-DoF URDF until mech's CAD
   lands.
6. Recruit: post the squad roles (§9) + a business/outreach lead (§11); **shortlist 3 faculty
   advisor candidates and send the first email** — advisor is the blocker for P1, RESPOND, and
   NVIDIA grants.
7. Kick off the sim IDMO panel scene from the IRC 2026 dimensions (they won't change much) —
   this is simultaneously the P1 benchmark environment.
8. Fire off the zero-cost funding applications: MathWorks student competition form, GitHub
   Education, AWS/GCP academic credits (§11).
9. P1 technical spike: install LeRobot, run SmolVLA fine-tuning end-to-end on any public
   dataset on your laptop — confirm the training loop works before betting a December deadline
   on it.
10. Start `CURRICULUM.md` Block A (rule R2): Modern Robotics ch. 2–3 + Articulated Robotics
    ros2_control series + Isaac Sim core tutorials — this week's study hours.
11. Scaffold `docs/textbook/` (rule R3): main.tex + chapter 1 ("Why this stack") from this
    plan's §3–§4 reasoning, before any code exists to document.

---

*Sources: [IRC 2026 Rulebook (PDF)](https://roverchallenge.org/wp-content/uploads/2025/10/IRC-2026-Rulebook.pdf) · [OpenVLA](https://openvla.github.io/) · [VLA models comparison 2026](https://www.roboticscenter.ai/tools/vla-models-comparison) · [VLA — Wikipedia](https://en.wikipedia.org/wiki/Vision-language-action_model) · [i-SAIRAS & iSpaRo 2026](https://www.isparo.space/) · [Space Robotics Workshop series](https://space-robots.org/) · [ISRO RESPOND](https://www.isro.gov.in/SponsoredResearch.html) · [IRoC-U prize details](https://makersmuse.in/news/isros-2026-robotics-challenge/) · [NVIDIA Academic Grant Program](https://www.nvidia.com/en-us/industries/higher-education-research/academic-grant-program/) · [MathWorks ERC sponsorship](https://www.mathworks.com/academia/student-competitions/european-rover.html) · [IRC](https://roverchallenge.org/irc/) · [ERC tasks](https://roverchallenge.eu/european-rover-challenge-a-list-of-tasks/) · [ERC competitor zone](https://roverchallenge.eu/competitor-zone/) · [ERC 2026 on-site files](https://drive.google.com/drive/folders/1txkq-1_6nlA_hwPbyGS6wdTtF9tjuSCb) · [ARC — about](https://set.adelaide.edu.au/atcsr/australian-rover-challenge/about-the-competition) · [ARC — team info/rules](https://set.adelaide.edu.au/atcsr/australian-rover-challenge/information-for-teams) · [ARCh 2026 handbook (PDF)](https://adelaide.edu.au/content/dam/adelaideuniversity/documents/about/news-and-events/events/2026/australian-rover-challenge/arch-2026-participant-handbook.pdf.coredownload.pdf) · [ARCh 2026 result](https://adelaide.edu.au/about/news/2026/uq-space-takes-out-australian-rover-challenge-2026/) · [Anatolian RC](https://www.anatolianrover.space/missions) · [Anatolian RSCP](https://github.com/anatolianroverchallenge/rscp) · [URC](https://urc.marssociety.org/) · [URC 2026 finalists](https://www.marssociety.org/news/2026/03/18/38-teams-advance-to-2026-university-rover-challenge-finals/) · [URC — Wikipedia](https://en.wikipedia.org/wiki/University_Rover_Challenge) · [IRoC-U 2026](https://www.ursc.gov.in/IRoC-U2026/challenge.jsp)*
