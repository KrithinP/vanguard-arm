# vanguard_hw — the real arm's ros2_control hardware interface (Fable design, 2026-07-07)
*Phase 1, the third bottom. C++ (the RT loop demands it — the one place Python loses).
Krithin types from this; theory gate = Block A3 re-read + control.ros.org hardware docs.*

## Shape: `VanguardArmSystem : hardware_interface::SystemInterface`
- **on_init**: parse URDF params (per-joint CAN ids, gear ratios, encoder counts/rev, limits —
  ALL from the ros2_control xacro block, so tuning never means recompiling).
- **on_configure**: open SocketCAN (`can0`), verify EVERY joint answers a ping; refuse activation
  on any silent joint (fail loud at config, not mid-motion).
- **read()**: drain CAN RX ring buffer → positions (encoder→rad via ratio), velocities, CURRENTS
  (export current as the effort state interface — P3/P6's force proxy lands here for free).
- **write()**: position targets → CAN frames. **ENFORCE LIMITS HERE** (ch.3's impossible-motion
  lesson: this layer is the last line — clamp position to URDF limits, rate-limit Δposition to
  velocity*dt, and a per-joint current ceiling that triggers controlled stop). The mock and
  Isaac never protected us; this MUST.
- **Watchdog**: no valid write() for 100ms → firmware holds position (firmware-side requirement:
  give mech/electronics this spec NOW, it's a firmware feature). E-stop chain independent.

## The three invariants (test each before first full-speed motion)
1. read() after write() reflects commanded motion direction for EVERY joint (sign errors are
   day-one certainties — the URDF axis vs motor polarity table gets filled joint by joint).
2. Kill the CAN bus mid-motion → arm holds, controller aborts on tolerance, node survives.
3. Grab a link mid-slow-motion → current ceiling triggers stop <100ms (the contact-safety test;
   also your first current-sensing datapoint for P6's October gate).

## The payoff line (already true by construction)
controllers.yaml, MoveIt, every skill, the teleop, the recorder — UNCHANGED. Swap the plugin
line in the xacro from TopicBasedSystem to vanguard_hw/VanguardArmSystem. Third bottom, same
interface. The September integration is a config edit plus three invariant tests — because the
week of 2026-07-02 made it so.
