# Research Radar — field state mid-2026 → program implications
*Swept 2026-07-07 (Fable pass). Re-sweep quarterly; next due ~Oct 2026 (pre-P1 writing).*

## Six findings, six implications

### 1. RL post-training of VLAs is THE 2026 wave — SFT-only ladders are already dated
SimpleVLA-RL (ICLR'26), π_RL (online RL for flow VLAs), FORCE, FlowPRO, STARE-VLA — an entire
subfield emerged in ~12 months: SFT policies can't recover from OOD errors; outcome-driven RL
post-training fixes it. **Implication (P1, adopted):** add ONE RL-post-trained rung
(SimpleVLA-RL recipe, open code, on the SmolVLA rung). Our killer synergy: **the verify-by-
effect grader IS a reward function** — panel joint-state predicates give sparse-but-honest
rewards with zero reward engineering. Sellable line: *"PanelBench ships an RL-ready reward
signal for free."* No SFT-only benchmark paper can say that.

### 2. Force/contact is the acknowledged VLA blind spot
ForceVLA (force-aware MoE, +23% on contact tasks), FAVLA (fast-slow), ForceFlow, FAWAM —
consensus: vision-only VLAs fail contact-rich work. Panel servicing IS contact-rich.
**Implications:** (P1, adopted) report contact/force metrics from PhysX (press force profile,
non-target contact events) even for vision-only policies — positions the benchmark as the
force-aware evaluation the wave needs. (P3/P6, sharpened) our real arm specs **per-joint
current sensing** → current-as-force-proxy makes P3's insertion ablation a *field* entry in
the ForceVLA conversation, which is all lab arms with real F/T sensors. Cheap arm, honest
force signal = the twist nobody has.

### 3. The evaluation crisis is real and named
RoboArena (distributed real-world eval), RobotArena∞ (real-to-sim translation), open LIBERO
saturation/contamination criticism; sim benchmarks accused of not capturing calibration drift,
contact, timing. **Implication (P1, adopted):** position AGAINST "another sim benchmark":
(a) scoring = world-state predicates, not video/human judgment (objective, contamination-
resistant); (b) held-out procedural seeds published, train/eval leakage impossible by
construction; (c) the real-arm twin (Phase 1) is the declared real-world leg — P2 field
results close the sim-real loop the critics demand. Cite the crisis in the intro; be the
remedy in our niche.

### 4. World-model data engines are industry's answer to data scarcity
DreamGen "neural trajectories" (22 new behaviors from ONE teleop task), Cosmos-Predict 2.5,
NVIDIA R²D² workflows. **Implication (P4, stretch option):** the dataset paper gains a timely
ablation — *scripted-expert replay vs neural trajectories vs human teleop: which data engine
works for contact tasks?* Only if bandwidth allows; the cheap version (cite + position our
expert-replay engine as the deterministic baseline world models should beat) costs one
paragraph. Do not let this inflate P1.

### 5. Shared autonomy is warm but our corner is empty
PATO (policy-assisted teleop), real-to-sim-to-real shared autonomy (2026), Stiffness Copilot
(impedance copilot for contact teleop — closest neighbor). Nobody: assisted teleop for
**field panel servicing under degraded comms**. We will own: competition RF environments,
operator-hours logs, latency injection infrastructure. **Implication (P5, sharpened):** P5 is
no longer "edge VLA OR operator study" — it is **"residual copilot for panel servicing under
communication degradation"**: train assistance from our teleop corpus, evaluate operator+
copilot vs operator-alone across injected latency/dropout. Unique data, timely method,
competition-useful (it's literally our IRC degraded-comms fallback, §3 PLAN).

### 6. Industry: manipulation foundation models are field-deploying NOW
Figure: 350+ Figure-03s, 1 robot/hour production, Helix in logistics; BMW pilot retired after
90k parts. Atlas ships with Gemini Robotics (multi-embodiment, zero-shot motion transfer).
JAL humanoids at Haneda on 3-year commitment. **Implications:** (a) intro framing — deployment
is outrunning field-domain evaluation; that gap is our thesis; (b) recruitment section of
PLAN §9 strengthens: the skills this program builds (VLA fine-tuning, RL post-training,
force-aware eval, Isaac/GR00T pipeline) are precisely what these companies are hiring for
RIGHT NOW; (c) NVIDIA grant narrative (GR00T rung + Cosmos-adjacent data engine) got stronger.

## What we deliberately did NOT chase
Humanoid whole-body control (crowded, no moat), pure world-model research (capital-intensive),
new VLA architectures (frontier-lab territory), LIBERO-style tabletop suites (saturated).
The moat remains: **field/planetary manipulation + a rover + competition deployments.**

## Sources (primary)
SimpleVLA-RL github.com/PRIME-RL/SimpleVLA-RL · π_RL arXiv:2510.25889 · ForceVLA
(OpenReview 2845H8Ua5D) · FAVLA arXiv:2602.23648 · RoboArena arXiv:2506.18123 · RobotArena∞
arXiv:2510.23571 · UMI-Bench arXiv:2606.10382 · DreamGen arXiv:2505.12705 · Cosmos/R²D²
developer.nvidia.com blogs · PATO (RSS'19 p013) · Real-to-Sim-to-Real Shared Autonomy
arXiv:2603.17016 · Stiffness Copilot arXiv:2603.14068 · figure.ai/news (Helix, 03 production).
