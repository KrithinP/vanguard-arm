#!/usr/bin/env python3
"""press_button v0: the first Vanguard skill. Scene -> plan -> approach -> retreat."""
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from pymoveit2 import MoveIt2
from threading import Thread

UR_JOINTS = ["shoulder_pan_joint", "shoulder_lift_joint", "elbow_joint",
             "wrist_1_joint", "wrist_2_joint", "wrist_3_joint"]

BOARD_POS, BOARD_SIZE = [0.55, 0.0, 0.72], [0.62, 0.03, 0.42]  # true size + 1cm skin (press config must stay outside)
HOVER = [0.43, -0.09, 0.82]        # 6 cm off the button face
PRESS = [0.43, -0.021, 0.82]       # flange 1mm past full button travel (face -0.03 + 8mm): full squeeze, block absorbs
QUAT_FACE_PANEL = [-0.7071, 0.0, 0.0, 0.7071]  # tool +Z along world +Y
STAGING = [5.637, -0.408, -1.041, 4.59, 0.646, 0.0]  # HARVESTED hover (2026-07-07): captured beats composed
PRESS_CFG = [5.7086, -0.4042, -1.0772, 4.6228, 0.5743, -0.0001]  # hover + 1.10 x (harvested 3mm-contact delta): computed full-press config

def main():
    rclpy.init()
    node = Node("press_button")
    moveit2 = MoveIt2(node=node, joint_names=UR_JOINTS,
                      base_link_name="base_link", end_effector_name="tool0",
                      group_name="ur_manipulator")
    # competition manners: 10% speed so the sim tracks within JTC path tolerance
    moveit2.max_velocity = 0.1
    moveit2.max_acceleration = 0.1
    # contact task: cartesian legs may intentionally brush the scene skin; don't truncate them
    moveit2.cartesian_avoid_collisions = False
    executor = rclpy.executors.MultiThreadedExecutor(2)
    executor.add_node(node)
    Thread(target=executor.spin, daemon=True).start()

    # the skill's own senses: the panel reports its joints; we score by effect, not by faith
    panel = {"button_joint": 0.0}
    def on_panel(msg):
        for n, p in zip(msg.name, msg.position):
            panel[n] = p
    node.create_subscription(JointState, "/panel_joint_states", on_panel, 10)

    arm = {}
    def on_arm(msg):
        for n, p in zip(msg.name, msg.position):
            arm[n] = p
    node.create_subscription(JointState, "/joint_states", on_arm, 10)

    node.get_logger().info("1/4 adding board to planning scene")
    moveit2.add_collision_box(id="panel_board", size=BOARD_SIZE,
                              position=BOARD_POS, quat_xyzw=[0, 0, 0, 1])

    node.get_logger().info("2/4 moving to hover config (joint-space: no IK lottery, collision-checked)")
    moveit2.move_to_configuration(STAGING)
    moveit2.wait_until_executed()

    node.get_logger().info("3/4 pressing (joint-space hop between proven configs)")
    moveit2.move_to_configuration(PRESS_CFG)
    moveit2.wait_until_executed()

    node.get_logger().info("   holding 2 s on the button")
    import time; time.sleep(2.0)
    depression = panel["button_joint"]
    cfg = [round(arm.get(n, float("nan")), 4) for n in UR_JOINTS]
    if depression > 0.006:
        node.get_logger().info(f"PRESS VERIFIED: button at {depression*1000:.1f} mm")
        node.get_logger().info(f"HARVEST pressed config: {cfg}")
    else:
        node.get_logger().error(f"PRESS FAILED: button at {depression*1000:.1f} mm (config: {cfg})")

    node.get_logger().info("4/4 retreating to hover (joint-space)")
    moveit2.move_to_configuration(STAGING)
    moveit2.wait_until_executed()

    node.get_logger().info("press_button: DONE")
    rclpy.shutdown()

if __name__ == "__main__":
    main()