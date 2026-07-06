# S3 REFERENCE — panel v1 element geometry + LAYOUT dict (Fable, 2026-07-07). Krithin types into build_panel.py.
# Design decisions frozen here so the build session is mechanical. All joints join the /panel_joint_states
# articulation automatically (children of the board = same articulation as v0.3).

LAYOUT = {  # element -> (x_offset_from_board_center, z_offset) on the board face; y derived from thickness
    "button":  (-0.12, +0.10),
    "switch":  (+0.12, +0.10),
    "knob":    (-0.12, -0.05),
    "latch":   (+0.12, -0.05),
    "drawer":  ( 0.00, -0.14),
    "socket":  ( 0.00, +0.02),
}
# P1 randomizer: jitter each offset ±0.05 on a seeded RNG; reject layouts with <6cm element spacing.

# --- knob: free revolute about Y (its face axis), grippable ridge ---
# body: cylinder r=0.025 depth=0.03 protruding from face + a small ridge cube on its face (so a
# flange/fingertip can torque it by friction+ridge). RevoluteJoint axis "Y", NO limits (continuous),
# angular drive stiffness 0, damping 0.8 (feels like a real detentless knob).
# success predicate (turn_knob skill): |knob_joint delta| ≥ 1.57 rad from episode start.

# --- latch: revolute about Z (lever swings sideways), limits [0, 60deg], catch via damping ---
# body: lever bar 0.10x0.015x0.02, pivot at one end (localPos anchors like the switch, ch.6 lesson).
# drive: stiffness 0, damping 3.0. success: latch_joint > 0.9 rad? no—limit 1.05 rad; use > 0.8.

# --- drawer: prismatic along -Y (pulls OUT toward the arm), travel 0..0.12 m ---
# body: open-top box 0.16x0.12x0.06 sitting in a face aperture; needs a HANDLE bar (0.06x0.015x0.015)
# on its front — the grasp target for the future grasp skill; friction material on handle.
# drive: stiffness 0, damping 8.0 (self-holding-ish). success: drawer_joint > 0.08 m (open) / < 0.02 (closed).
# NOTE: drawer body must NOT collide with board interior — model the aperture as 4 thin cubes framing
# a hole (compound board), or simpler: mount drawer PROUD of the face (protruding box, no aperture). v1 = proud.

# --- socket: NO joint. Collision-only receptacle for the future insert skill ---
# 3 cylindrical holes won't work with cube prims: build as 4 cubes forming a square pocket
# (inner clearance 0.022 for a 0.02 peg) protruding 0.02 from the face. Peg = separate free
# rigid body (0.02x0.02x0.08) spawned on a spawn-shelf cube at board's left edge.
# success (insert skill): peg pose within 8mm of pocket center AND peg -Y depth ≥ 0.015 into pocket.
# (Pose predicate, not joint — the one element scored by pose; P1 v2 task.)

# Build order per element (the v0.3 recipe): cube(s) -> RigidBodyAPI -> joint w/ EXPLICIT localPos
# anchors both sides (pre-scale units, ch.6) -> DriveAPI damping -> re-run, Play, Shift-drag test.
# After v1 builds: re-harvest press/flip configs IF layout moved those elements (it does - button/switch
# keep their v0.3 spots in LAYOUT above, so existing skills stay valid).
