#!/usr/bin/env python3
"""S1 REFERENCE (Claude, 2026-07-07) — Krithin types the real switch_flip.py from this (R1).

switch_flip: second skill, proving the ch.9 pattern generalizes.
Pattern identical to press_button: joint-space hops between HARVESTED configs, verify by effect.

HARVEST PROCEDURE (do once, before typing the skill):
 1. Bring-up order: Isaac(Play) -> control stack -> MoveIt+RViz.
 2. In RViz, jog/plan the arm to hover in front of the SWITCH (it's at world (0.67,-0.03,0.82),
    i.e. 12cm RIGHT of board center, 10cm up). Execute. Read /joint_states -> that's HOVER_SW.
 3. Nudge tool to push the switch paddle's TOP toward the board (flips it one way). Execute,
    read /joint_states -> PUSH_A. Retreat, approach the paddle's BOTTOM, push -> PUSH_B.
 4. Bake the three configs below. If a push only half-flips, extend that config's delta by
    1.10x from hover, exactly like PRESS_CFG in press_button (captured beats composed).

PANEL PREREQ (Script Editor, once): give the switch a detent so it holds sides crisply.
    from pxr import UsdPhysics
    import omni.usd
    sj = omni.usd.get_context().get_stage().GetPrimAtPath("/World/IDMOPanel/switch_joint")
    drv = UsdPhysics.DriveAPI(sj, "angular")
    drv.GetStiffnessAttr().Set(0.0); drv.GetDampingAttr().Set(5.0)   # heavier damping = holds side, no gravity creep
    Then Ctrl+S. (Also add this to build_panel.py's switch section for future rebuilds.)
"""
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from pymoveit2 import MoveIt2
from threading import Thread
import sys

UR_JOINTS = ["shoulder_pan_joint", "shoulder_lift_joint", "elbow_joint",
             "wrist_1_joint", "wrist_2_joint", "wrist_3_joint"]
BOARD_POS, BOARD_SIZE = [0.55, 0.0, 0.72], [0.62, 0.03, 0.42]

# --- HARVEST THESE (placeholders will fail planning on purpose) ---
HOVER_SW = None   # e.g. [5.9, -0.45, -0.98, 4.55, 0.40, 0.0]
PUSH_A   = None   # flips switch to side A (positive angle)
PUSH_B   = None   # flips switch to side B (negative angle)
FLIP_THRESHOLD = 0.30  # rad; |switch_joint| beyond this = committed to a side (limit is 0.436)

def main():
    side = (sys.argv[1] if len(sys.argv) > 1 else "A").upper()
    assert side in ("A", "B"), "usage: switch_flip.py [A|B]"
    push_cfg, want_sign = (PUSH_A, +1) if side == "A" else (PUSH_B, -1)
    assert HOVER_SW and push_cfg, "HARVEST the configs first (see module docstring)"

    rclpy.init()
    node = Node("switch_flip")
    moveit2 = MoveIt2(node=node, joint_names=UR_JOINTS, base_link_name="base_link",
                      end_effector_name="tool0", group_name="ur_manipulator")
    moveit2.max_velocity = 0.1
    moveit2.max_acceleration = 0.1
    executor = rclpy.executors.MultiThreadedExecutor(2)
    executor.add_node(node)
    Thread(target=executor.spin, daemon=True).start()

    panel = {"switch_joint": 0.0}
    def on_panel(msg):
        for n, p in zip(msg.name, msg.position):
            panel[n] = p
    node.create_subscription(JointState, "/panel_joint_states", on_panel, 10)

    def leg(desc, cfg):
        node.get_logger().info(desc)
        moveit2.move_to_configuration(cfg)
        if not moveit2.wait_until_executed():
            node.get_logger().error(f"LEG FAILED: {desc} - aborting")
            rclpy.shutdown(); raise SystemExit(2)

    node.get_logger().info("1/4 adding board to planning scene")
    moveit2.add_collision_box(id="panel_board", size=BOARD_SIZE,
                              position=BOARD_POS, quat_xyzw=[0, 0, 0, 1])
    leg("2/4 hover at switch (joint-space)", HOVER_SW)
    leg(f"3/4 pushing switch to side {side}", push_cfg)
    import time; time.sleep(1.0)
    leg("4/4 retreat to hover", HOVER_SW)

    time.sleep(0.5)  # let the switch settle on its detent
    angle = panel["switch_joint"]
    if angle * want_sign > FLIP_THRESHOLD:
        node.get_logger().info(f"FLIP VERIFIED ({side}): switch at {angle:+.3f} rad")
    else:
        node.get_logger().error(f"FLIP FAILED ({side}): switch at {angle:+.3f} rad")
        raise SystemExit(1)
    node.get_logger().info("switch_flip: DONE")
    rclpy.shutdown()

if __name__ == "__main__":
    main()
