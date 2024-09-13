#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32, Bool
import subprocess


class PoseResetNode(Node):

    def __init__(self):
        super().__init__('pose_reset_node')
        self.reset_count = 0
        self.collision_occurred = False  # Flag to track collision state
        self.is_resetting = False  # To prevent multiple resets on the same collision
        self.update_received = False  # Flag to track if update flag is received

        # Timer to run at 30Hz (0.033 seconds)
        self.timer = self.create_timer(1 / 30, self.timer_callback)

        # Publisher for system_feedback topic
        self.feedback_publisher = self.create_publisher(Int32, 'system_feedback', 10)

        # Publisher for episode_end topic
        self.episode_end_publisher = self.create_publisher(Bool, '/episode_end', 10)

        # Subscriber to collision topic
        self.collision_subscription = self.create_subscription(
            Bool,
            '/collisions',
            self.collision_callback,
            10
        )

        # Subscriber to update_sync topic
        self.update_sync_subscription = self.create_subscription(
            Bool,
            '/value_update_sync',
            self.update_sync_callback,
            10
        )

    def collision_callback(self, msg):
        # If collision is detected (True) and we are not already resetting
        if msg.data and not self.is_resetting:
            self.collision_occurred = True
            self.is_resetting = True  # Mark that a reset is in progress
            self.reset_robot_pose()

        # If no collision (False), we are ready for the next collision
        elif not msg.data:
            self.is_resetting = False  # Reset flag to allow future resets

    def update_sync_callback(self, msg):
        # If update flag is True, set update_received to True
        if msg.data:
            self.update_received = True
            # Resume the simulation if reset is complete
            self.control_simulation('play')

    def timer_callback(self):
        # This timer callback runs at 30Hz but doesn't need to handle resets anymore
        pass

    def reset_robot_pose(self):
        # Pause the simulation
        self.control_simulation('pause')

        # Publish the episode end signal
        self.publish_episode_end(True)

        # Construct the Ignition command to reset pose
        command = (
            'ign service -s /world/empty_world/set_pose '
            '--reqtype ignition.msgs.Pose --reptype ignition.msgs.Boolean '
            '--timeout 300 --req '
            '\'name: "PPO_agent", position: {x: 0.0, y: 0.0, z: 1.0}, '
            'orientation: {x: 0.0, y: 0.0, z: 0.707, w: 0.707}\''
        )

        try:
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.stderr:
                self.get_logger().error(f'Error:\n{result.stderr.decode()}')
        except subprocess.CalledProcessError as e:
            self.get_logger().error(f'Command failed with exit code {e.returncode}')
            self.get_logger().error(f'Error output: {e.stderr.decode()}')

        # Increment reset counter
        self.reset_count += 1

        # Publish feedback immediately after pose reset
        self.publish_feedback()

        # Clear the collision flag after reset
        self.collision_occurred = False

    def control_simulation(self, command):
        # Construct the Ignition command to control simulation
        control_command = (
            f'ign service -s /world/empty_world/control '
            '--reqtype ignition.msgs.WorldControl --reptype ignition.msgs.Boolean '
            '--timeout 300 --req '
            f'\'pause: {command == "pause"}\''
        )

        try:
            result = subprocess.run(control_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.stderr:
                self.get_logger().error(f'Error:\n{result.stderr.decode()}')
        except subprocess.CalledProcessError as e:
            self.get_logger().error(f'Command failed with exit code {e.returncode}')
            self.get_logger().error(f'Error output: {e.stderr.decode()}')

    def publish_episode_end(self, status):
        # Create a Bool message with the episode end status
        msg = Bool()
        msg.data = status
        # Publish the episode end status
        self.episode_end_publisher.publish(msg)

    def publish_feedback(self):
        # Create an Int32 message with the reset count
        msg = Int32()
        msg.data = self.reset_count
        # Publish the reset count data
        self.feedback_publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = PoseResetNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
