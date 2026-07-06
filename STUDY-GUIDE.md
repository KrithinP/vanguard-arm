# The Vanguard Study Guide — project start → IRC 2027
*Vetted 2026-07-07 (Fable pass). Companion to CURRICULUM.md (which has the full source URLs +
search keywords — this guide sequences and prioritizes; that file expands). The standard
throughout: the **oral-exam test** — could you explain this to a PIMA judge, a recruiter, your
advisor, and a first-year, each at their level? If not, it isn't learned yet.*

---

## 0. How to study this (read first, it changes everything after)

- **Method: recall, not re-reading.** For every section: read once → close everything → write/
  say the explanation from memory → check → fix gaps. Re-reading feels like learning; recall IS
  learning. The ✅ checks and the Question Bank (§6) are your recall prompts.
- **The sprint (your 2–3 days):** Day 1 = §2 (math spine) + §3.1–3.3 (the stack). Day 2 = §3.4–
  3.5 + §4 (papers, first pass). Day 3 = §5 (competition layer) + full Question Bank, closed-book.
- **Then maintenance till IRC (§7):** ~2 h/week. Mastery is built in the sprint, *kept* weekly.
- **Paper-reading method (use for every paper in §4):** three passes — (1) abstract + figures +
  conclusion, 10 min: what's the claim? (2) method section, 20 min: how, exactly? (3) experiments,
  10 min: does the evidence support the claim? Write THREE sentences per paper: claim, mechanism,
  what-we-steal. Papers you can't summarize in three sentences aren't read yet.
- **Your unfair advantage:** `docs/textbook/main.pdf` — Part I is the story of everything you
  built with every mistake root-caused. Read chapters *before* their theory sections below; the
  war stories are the memory hooks the theory hangs on.

---

## 1. The story you must be able to tell (learn this FIRST — it's the answer to "what do you do")

Three lengths, memorized cold:

**10 seconds (anyone):** "I lead arm autonomy for our Mars-rover team — I build the software
that lets a robot arm operate control panels, first driven by a human, eventually by itself.
We're building it to win India's international rover championship."

**60 seconds (engineer/recruiter):** add — "The stack is ROS 2 + MoveIt on a digital twin in
NVIDIA Isaac Sim; we proved the sim and the real arm expose identical interfaces, so everything
we build this summer runs unmodified on hardware in September. Skills are deterministic
demonstration-replay with verification from the world's own state — and that same
infrastructure doubles as a research benchmark: we're evaluating whether vision-language-action
models transfer to planetary panel servicing, submitting in December."

**5 minutes (judge/advisor):** the full arc — competition tasks → six-skill architecture →
sim-first rationale → the determinism doctrine (ch.9) → research program (P1 benchmark, the
RL-reward-for-free insight, the field/force niche) → roadmap to IRC. Practice this OUT LOUD
twice during the sprint. It is the PIMA presentation, the advisor pitch, and the interview
answer, and they are the same speech at three zoom levels.

---

## 2. Day 1 morning — the math spine (own it on paper)

**Read: your textbook Part II (A1→A3), working every problem closed-book.** Then patch gaps with
Modern Robotics (MR) ch. 2–6 (free PDF + videos — CURRICULUM A1 has links).

The five objects you must manipulate fluently, each with its one-line essence:
1. **Rotations/SO(3)** — orthogonal, det+1; compose right-to-left; quaternions are the wire
   format (x,y,z,w in ROS — the ordering trap is A1's Problem 4).
2. **Transforms/SE(3)** — pose = R + p; subscript cancellation IS TF2; inverse transposes only R.
3. **PoE forward kinematics** — `T(θ) = e^[S1]θ1 ··· e^[Sn]θn · M`; the URDF is this, serialized.
4. **The Jacobian** — columns = "tool velocity if only joint i moves"; lever-arm physics;
   `det J → 0` = singularity = the straight-elbow experiment you ran on day 2.
5. **Damped least squares** — `Δθ = Jᵀ(JJᵀ+λ²I)⁻¹e`; why we damp instead of pretending precision.

✅ *Gate:* A2.1 and A3.1 solved cold on paper; explain to an imaginary first-year why 6 DoF is
the floor for plug insertion, and what physically happens at a singularity.

## 3. Day 1 afternoon → Day 2 — the stack (your build, systematized)

Read the matching textbook chapter FIRST (hooks), then the concept doc (structure):

- **3.1 ROS 2 model** *(ch.3 + ch.5)*: nodes/topics/services/actions; QoS (why sensor data is
  best-effort and commands are reliable); executors. The FollowJointTrajectory action anatomy —
  you've lived it; now be able to draw it.
- **3.2 ros2_control** *(ch.5)*: the read→update→write loop; hardware_interface as the ONLY
  swap point (mock → topic_based/Isaac → CAN drivers = one interface, three bottoms — say this
  sentence in every interview); controllers vs broadcasters; why tolerances define what
  "success" even means (ch.5's correction lesson). Source: control.ros.org concepts pages.
- **3.3 MoveIt 2** *(ch.7)*: planning scene (the world model YOU populate), SRDF/groups, OMPL
  sampling vs Pilz determinism, IK plugins, why pose goals are an 8-branch lottery on a UR
  (ch.9) and when configurations beat poses. Source: moveit.picknik.ai concepts.
- **3.4 Isaac Sim / USD** *(ch.4 + ch.6)*: stages/prims/references; articulations, joints,
  drives (stiffness/damping — recite the undamped-UR5e story), the ROS 2 bridge action graph;
  Replicator's role in P1. Source: Isaac Sim docs core concepts + CURRICULUM A4.
- **3.5 The determinism doctrine** *(ch.8–9 — read twice, this is YOUR contribution)*:
  travel-safely-touch-intentionally; captured-beats-composed; verify-by-effect; the escalation
  from GUI → script → skill. This doctrine is what you'll defend in every design review.

✅ *Gate:* whiteboard the full data path (operator/skill → action → JTC → hardware interface →
Isaac/motors → joint states → back) with every process boundary named; explain each of the
textbook's ~24 lessons in one sentence each (skim the mistake logs as a checklist).

## 4. Day 2–3 — the research canon (the papers, vetted, in reading order)

*Three-pass method + three sentences each. Full citations/links: CURRICULUM Block D +
research/RESEARCH-RADAR.md. Two sittings of ~4 papers beat one death-march.*

**Sitting 1 — how robots learn from demonstrations (P1's spine):**
1. **ALOHA/ACT** — action chunking; why predicting sequences beats single steps.
2. **Diffusion Policy** — denoising as trajectory sampling; the strongest small-data baseline.
3. **OpenVLA** — the open 7B VLA; what "fine-tune a VLA" concretely means.
4. **SmolVLA** — why small+open matters; OUR primary fine-tune target; async inference idea.
5. **MimicGen** — demo multiplication via SE(3) warps; connect to our config-replay data engine
   (ch.9's convergence insight — be able to tell that story: our skill IS a scripted expert).

**Sitting 2 — the 2026 frontier (what makes P1 current, from the RADAR):**
6. **GR00T N1.5** (blog+paper skim) — synthetic-data-heavy flagship; our HPC rung.
7. **SimpleVLA-RL** — RL post-training; OUR grader-as-reward insight — one paragraph, memorized.
8. **ForceVLA** (abstract+figures) — the contact blind spot; why P1 reports force metrics and
   P3 uses current sensing (the lab-F/T-vs-field-current asymmetry — your line to own).
9. **RoboArena / RobotArena∞** (abstracts) — the evaluation crisis; recite P1's three answers
   (predicate scoring, held-out seeds, real-arm leg).
10. **DreamGen** (abstract+figures) — neural trajectories; know it as the industry data engine
    P4 might ablate against.

**Then re-read `research/p1/DESIGN.md` start to finish.** ✅ *Gate:* defend the ladder to a
hostile reviewer — why each rung exists, what result would mean what, and answer "isn't this
just another sim benchmark?" without notes.

## 5. Day 3 — the competition layer

- **Rulebooks**: query the graph, don't re-read PDFs (`graphify query "..."`). Must know cold:
  IRC mission structure (ABEx/RADO/IDMO/PIMA), the 10-min/20-min point gates, intervention
  costs, the RADO autonomous-delivery 100%-vs-50% rule, comms constraints, 65 kg/1.5 m limits.
  ARC: the four tasks + hose connector. ERC: maintenance panel + ArUco autonomy bonus.
- **Know thy enemy** (PLAN §1.1): skim EPFL Xplore's `ERC_HD` README/architecture and MRDT's
  `Autonomy_Software` docs — 30 min each, enough to compare-and-contrast with our stack when a
  judge asks "what do other teams do?"
- **Watch**: 2–3 URC/ERC finalist run videos + one SAR video (the bar for our SDDR) — active
  watching: score along, note operator pacing.
- ✅ *Gate:* Question Bank section F, closed book.

## 6. The Question Bank (the oral exam — answer ALL closed-book by sprint end)

**A. Math/kinematics:** Why can't 5 DoF do arbitrary insertion? · What happens to IK at a
straight elbow, mathematically and physically? · Derive the 2R Jacobian determinant; what does
its zero mean? · Why damp IK, and what does λ trade? · Quaternion vs RPY — when and why?
**B. Stack:** Trace a button press from Python to PhysX, every hop. · What exactly swaps
between mock, Isaac, and real hardware? · What does error_code=0 certify, and under what
config? · Why did the arm "randomly wander" that Sunday? (two controller managers) · Why
providers-before-consumers in bring-up?
**C. Sim:** What is a USD reference vs a copy? · Where does an Articulation Root live on a
fixed-base robot and why? · What do drive stiffness/damping do, and what did the UR5e asset
ship with? · Why is the panel procedural?
**D. Skills doctrine:** Why joint configs over poses? (the 8-branch answer) · Why did the
cartesian service betray us — and what does its silent fallback teach about APIs? · What makes
a skill a skill vs a script? (verify-by-effect + abort-on-failed-leg) · Recite
travel-safely-touch-intentionally with its origin story.
**E. Research:** The 3-sentence version of each of the 10 papers. · Why is our grader an RL
reward? · The evaluation-crisis answer. · Why field manipulation is a moat frontier labs can't
cheaply cross. · What would make P1 fail, and its cut lines?
**F. Competition:** Where do IDMO points actually come from? · The RADO autonomy math — when
does a 70%-reliable autonomous delivery beat perfect teleop? · What does an intervention cost
and when do you take one anyway? · Our declared-mode decision process?
**G. The mirror (hardest):** What are the three biggest weaknesses of our current stack?
(Fair answers: baked configs brittle to panel pose — perception isn't in the loop yet; single
taught element set; no force control — contact is open-loop position. Knowing your weaknesses
IS the expert signal.)

## 7. Maintenance till IRC (after the sprint, ~2 h/week)

- **Weekly:** 3 random Question-Bank items closed-book · 1 paper (new from the radar or a
  re-pass) · re-read the newest textbook chapter (they keep appearing — that's R3 working).
- **Phase-gated:** Block B (calibration/camera geometry) the week hardware arrives — not
  before; Block C1–C2 (servoing/compliance) when perception enters the skills; Block D
  hands-on deepens during the P1 sprint itself.
- **Monthly:** give the 5-minute story out loud to someone new; update it with the month's work.
- **October radar re-sweep** feeds one new paper into the rotation.

## 8. What else you'll need (your ask — the honest list)

1. **Spaced repetition (Anki or plain flashcards)** — 30–40 cards from the Question Bank +
   paper three-sentences. 10 min/day beats everything else on retention; make the cards during
   the sprint (making them is half the learning).
2. **Teach it — you have ~50 recruits.** Run a 1-hour "how our arm works" session for the
   inductees in August. Nothing exposes fog like a first-year's "but why?" This is the single
   highest-leverage suggestion in this file.
3. **A gap log** — a running note of every question you couldn't answer cleanly (from study,
   judges, advisor, recruits). It becomes each week's study agenda and my session openers.
4. **The advisor conversations are oral exams** — treat the first faculty meeting as a dry run
   of the 5-minute story + P1 defense. Ask them to poke holes.
5. **Print the textbook** (or tablet+pen) — annotate margins during the sprint; your
   annotations become v2 of the book.
6. **Watch selectively, not completely:** Tedrake's lecture *chapters* on force control and
   grasping when Block C opens; 3Blue1Brown linear algebra ONLY if A1 felt shaky (2 h, once).
7. **Sleep the sprint properly** — recall-based study is brutal; 3 focused 90-min blocks/day
   with real breaks outperform 10-hour grinds. The material is deep, not wide; depth needs rest.
8. **What you do NOT need yet:** RL theory courses, advanced control theory (operational-space,
   MPC), SLAM — all deliberately post-IRC or gated to phases. Depth on the canon above beats
   breadth every time someone asks you what you do.
