# P1 data engine REFERENCE — scripted expert on randomized layouts (Fable, 2026-07-07)

The design's core trick made concrete: the taught-config skill becomes a layout-general expert
because *teaching can be automated when you own sim state*. Pipeline per layout seed:

## 1. generate_layout(seed) -> LAYOUT dict + build panel headlessly
Isaac headless (`isaac-sim.headless` / SimulationApp): run build_panel with jittered LAYOUT,
Replicator visual randomization pass (T2 only). One process per batch of layouts.

## 2. re-teach the expert per layout (the automated "harvest")
For each element+task, compute the config pair the human harvested manually in ch.9 — but via
IK, which the EXPERT is allowed (it reads sim ground truth; policies never do):
- hover pose = element world pose + face-normal offset (6cm), tool axis = -face normal.
- contact pose = hover advanced along normal to (travel + 1mm) — same overshoot trick.
- Solve IK for BOTH with the SAME seed config (bias toward a canonical elbow-up branch:
  seed the solver at the ch.9 STAGING config; reject solutions >1.5 rad joint-distance from
  seed — this kills the 8-branch lottery *inside* the generator).
- Validate: FK(sol) matches pose <2mm; collision-check hover against board box. Reject & resample.
- IK tool: `moveit2.compute_ik` (pymoveit2 exposes it) or KDL directly — offline, so slow is fine.

## 3. roll out expert episodes with injected noise (MimicGen-lite)
For m in M (e.g. 8 rollouts/layout): perturb hover+contact configs with joint noise σ=0.02 rad
(clip to keep FK within 1cm of target), execute hover->contact->retreat at 10 Hz, record
obs/actions in LeRobot format (SAME recorder as S4 — one writer, two sources: human + expert).
Label success from panel predicates AS RECORDED (keep failures! ~5-10% failed episodes are
valuable — filter at training time per recipe, and they're the RL rung's negatives).

## 4. dataset assembly
2k expert + ≥100 teleop episodes/task; metadata per episode: {seed, tier, source: expert|human,
success, panel joint traces}. Dataset card documents the generator — reviewers must be able to
regenerate from seeds. THE SEEDS ARE THE BENCHMARK: publish train seeds, hold out eval seeds.

## Compute budget sanity
Episode ≈ 15s sim time; headless RTX laptop ≈ 2-4x realtime single-env → 2k episodes ≈ 3-6
laptop-hours. Fine. (Isaac Lab vectorization exists if this ever needs 50k — P5/P6 territory.)

## Failure modes to expect (tripwires)
- IK branch flips between hover and contact (different branches = wild swing): reject pair if
  joint-distance(hover,contact) > 0.8 rad; resample with tighter seed bias.
- Replicator randomization leaking into physics (material friction changes press force): lock
  physics materials; randomize VISUAL materials only for T2.
- Camera pose drift after layout jitter: wrist cam is arm-mounted (moves with arm — fine);
  keep any static cam FIXED across layouts or policies cheat off panel position via background.
