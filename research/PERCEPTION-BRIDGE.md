# The Perception Bridge — taught skills on a movable panel (Fable design, 2026-07-07)
*Phase 0d/2 design. Solves the ch.9 caveat ("baked configs are brittle to the panel moving")
without abandoning the determinism doctrine. Read after STUDY-GUIDE §2 (you need frames cold).*

## The problem, precisely
Taught configs are joint-space snapshots that encode the panel's pose IMPLICITLY. Competition
panel pose is unknown until the rover parks. Naive answer — "use pose goals + IK online" —
reintroduces the 8-branch lottery ch.9 killed. We need: panel-relative teaching + lottery-free
online re-derivation.

## The design (three pieces, all machinery we already have)

### 1. Teach in the PANEL frame, not the world frame
At teach time, record for each taught config: `X_panel_tool = X_world_panel⁻¹ · FK(θ_taught)`
(a tool pose in the panel's frame — the A1 triple-product, reversed). The YAML stores BOTH the
joint config (for fixed-panel/sim use) and `X_panel_tool` (for the field). One extra line in
the teach harvester.

### 2. Estimate X_world_panel online (the ONLY perception in the loop)
ArUco board (4 markers, panel corners — ERC literally provides this; for IRC we detect the
panel face) → solvePnP → `X_cam_panel` → chain through calibrated `X_tool_cam` (hand-eye,
Block B1) and `FK`: `X_world_panel = FK(θ_now) · X_tool_cam · X_cam_panel`. Median over 30
frames, reject outliers >2cm. Panel is static per attempt → estimate ONCE after parking,
freeze it. No tracking, no servoing loop, no drift: one number, measured carefully.

### 3. Re-derive joint configs offline-onboard (the data-engine trick, reused on the rover)
For each skill: `X_world_tool_target = X_world_panel · X_panel_tool` → solve IK **seeded at
the canonical STAGING config, rejecting solutions >1.5 rad joint-distance from seed** (the
branch-pinning rule from data_engine.REFERENCE §2 — the lottery killed the same way twice).
Validate FK<2mm + collision-check vs the board box (also re-posed from X_world_panel). Output:
a fresh taught_poses.yaml for THIS panel pose. Then the skills run EXACTLY as today —
deterministic joint hops. Perception runs once per parking, never per motion.

## Why this is right (the defensible argument)
- Preserves ch.9's doctrine: perception FINDS the panel; replay PRESSES the button.
- Degrades gracefully: ArUco fails → operator clicks 4 panel corners in the camera view →
  same PnP → same pipeline (the teleop-assist from PLAN §3, unified with autonomy).
- It's the SAME code path as P1's expert generator — field system and benchmark share the
  re-teach machinery. One implementation, two papers, one competition.
- Error budget: PnP ~5mm + hand-eye ~3mm + FK ~2mm ≈ 1cm at the tool. Button is 4cm wide;
  press tolerance eats it. RJ-45/3-pin insertion does NOT (needs <2mm) → insertion keeps its
  compliance/spiral-search layer on top (C2) — perception gets you to pre-insert, compliance
  finishes. This split IS the P3 paper's framing.

## Build order (Phase 0d, post-S6): ArUco board on the sim panel → sim hand-eye (trivial:
known transforms — validates pipeline) → re-derivation node → THE TEST: move the panel 20cm +
15° in sim, re-estimate, re-derive, run press_button UNMODIFIED → VERIFIED. That demo (skills
survive panel relocation) is the SDDR video's autonomy money-shot.
