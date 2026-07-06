# P1 — Experiment Design (frozen 2026-07-07, Fable pass; execute, don't relitigate)

**Working title:** *PanelBench: Do vision-language-action models transfer to planetary
panel servicing?* — a procedurally-randomized Isaac Sim benchmark + evaluation of the
policy ladder against a scripted expert. Target: submit ~15 Dec 2026, arXiv same day.
Venue: RA-L (rolling) primary; Space Robotics Workshop @ ICRA 2027 fallback.

## The claim structure (what the paper must be able to say)
1. We release a reproducible panel-servicing benchmark (standard UR5e, procedural IRC-style
   panel, ground-truth scoring from the panel's own joint states) — the *artifact* claim.
2. On it, we measure where the current policy ladder (BC→ACT→Diffusion→VLA fine-tunes→**VLA+RL
   post-training**) sits relative to a scripted expert under distribution shift — the *finding*
   claim. Honest negative results are a valid finding.
3. Positioning vs the evaluation crisis (RoboArena/RobotArena∞ critique of sim benchmarks):
   scoring by world-state predicates (objective, contamination-resistant), held-out procedural
   seeds published, and a declared real-arm twin (P2) as the real-world leg. We're not another
   sim benchmark; we're the effect-grounded one with a field roadmap.

## Why we win this niche (from PLAN §8, restated for the intro)
VLAs are trained/evaluated on tabletop lab manipulation; panel servicing for planetary rovers
is unstudied, safety-relevant, and we own the full apparatus: sim twin, procedural panel,
deterministic expert, effect-based grader — all already built as competition infrastructure.

## Benchmark spec
- **Robot:** UR5e (ur_description), fixed base — anyone can load it; reproducibility beats
  realism for P1 (the real arm is P2's story).
- **Environment:** procedural panel (build_panel LAYOUT dict): elements {button, switch;
  v1 adds knob, drawer} with randomized (a) element positions on the board (±10 cm grid),
  (b) board pose (±5 cm, ±10° yaw), (c) visuals via Replicator (lighting, textures, colors).
  Three difficulty tiers: T0 fixed layout / T1 position shift / T2 position+visual shift.
- **Tasks (v1):** press-button, flip-switch(direction). Task success = panel joint state
  predicate (button ≥6 mm during episode; switch sign matches command) — **the grader is the
  world's own state; no human, no video judging.**
- **Observations:** wrist RGB (Isaac camera), joint states; **actions:** joint targets @10 Hz
  (matches teleop recorder). Episode ≤30 s.

## The expert & the data engine (the design's core trick)
Our deterministic skill (taught-config replay) IS the scripted expert: for any randomized
layout, re-derive its taught configs by solving IK once offline per layout (allowed for the
EXPERT — it sees sim state; policies see only obs). Expert success rate ~100% on T0/T1 →
**demo generation at scale is a for-loop, not a teleop marathon**: N layouts × M noise-injected
replays (config-space jitter, MimicGen-lite). Teleop episodes (S4) supplement for
human-style variation. Budget: 2k generated + ≥100 teleop episodes per task.

## The ladder (all LeRobot-native; train on BITS HPC or laptop per size)
| Rung | Why it's there |
|---|---|
| Scripted expert (privileged) | ceiling / sanity |
| BC-MLP (obs→action) | floor |
| ACT | small-data champion |
| Diffusion Policy | strongest classical learner |
| SmolVLA fine-tune | the accessible VLA |
| **SmolVLA + RL post-training** (SimpleVLA-RL recipe) | **the 2026 wave; our grader IS the reward — zero reward engineering** |
| GR00T N1.5 fine-tune | the flagship VLA (HPC) |

## Protocol
Train on T0+T1 data; evaluate all rungs on T0/T1/T2 × 100 held-out layouts × 3 seeds.
Report: success rate (with Wilson CIs), time-to-success, panel-collision rate (any non-target
contact force event), **and press-force profiles from PhysX — force-aware metrics even for
vision-only policies (the ForceVLA-wave gap our benchmark fills; see RESEARCH-RADAR §2)**. Ablations (pick ≤2 by time): generated-vs-teleop data mix; episodes-count
scaling curve. Everything logged to W&B project `vanguard-p1`; eval harness = one script that
prints the paper's main table.

## Paper skeleton (write sections in this order)
1. Benchmark + grader (§3) — written from code, can start Nov 1.
2. Expert + data engine (§4).
3. Results + honest analysis (§5) — needs eval runs done by Dec 1.
4. Intro/related work last (related-work seeds: OpenVLA, π0/π0.5, SmolVLA, GR00T N1.5,
   MimicGen, LIBERO/RoboCasa/ManiSkill3 as benchmark kin, vla-eval; check for a 2026
   panel-manipulation paper we might have missed — one WebSearch sweep in Nov).

## Timeline back-cast (slack included; the S-numbers are TASKS.md stages)
- **by Oct 1:** S4 recorder live (hard gate).
- **Oct:** S3 panel v1 + LAYOUT randomizer + Replicator pass; expert-on-random-layouts
  (IK re-derivation) working; first 500 generated episodes.
- **Nov 1–20:** train the ladder (small rungs laptop, GR00T on HPC); eval harness; main table.
- **Nov 20–Dec 10:** write; figures via `dataviz` skill; internal red-team pass with
  `honest-advisor` framing ("what would a reviewer kill this for").
- **Dec 10–15:** advisor pass, polish, submit + arXiv.
- **Cut lines if late (in order):** RL rung → GR00T rung → T2 tier → 2nd ablation. The benchmark +
  expert + ≥3 rungs is still a paper; a late everything is not.
