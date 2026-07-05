import rclpy
# pyrefly: ignore [missing-import]
from rclpy.action import ActionClient
from rclpy.node import Node
# pyrefly: ignore [missing-import]
from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration

UR_JOINTS=[
    "shoulder_pan_joint","shoulder_lift_joint","elbow_joint",
    "wrist_1_joint","wrist_2_joint","wrist_3_joint",
]

class TrajectoryClient(Node):
    def __init__(self):
            super().__init__("send_trajectory")
            self._client = ActionClient(
                self, FollowJointTrajectory,
                "/scaled_joint_trajectory_controller/follow_joint_trajectory"
            )


    def send(self):
        traj = JointTrajectory()
        traj.joint_names =UR_JOINTS
        p1=JointTrajectoryPoint()
        p1.positions= [0.0,-1.57,0.0,-1.57,0.0,0.0]# home ish
        p1.time_from_start=Duration(sec=4)
        p2=JointTrajectoryPoint()
        p2.positions= [1.6, -0.5, 1.8, -2.5, -1.2, 0.9]# dramatic sweep - unmissable, all joints legal
        p2.time_from_start=Duration(sec=8)
        traj.points=[p1,p2]

        goal = FollowJointTrajectory.Goal()
        goal.trajectory = traj
        self._client.wait_for_server()
        self.get_logger().info("sending 2-point trajectory...")
        future = self._client.send_goal_async(goal)
        rclpy.spin_until_future_complete(self, future)
        result_future = future.result().get_result_async()
        rclpy.spin_until_future_complete(self, result_future)
        self.get_logger().info(f"done: error_code={result_future.result().result.error_code}")

def main():
    rclpy.init()
    node = TrajectoryClient()
    node.send()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
