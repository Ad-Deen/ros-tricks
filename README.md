# ros-tricks
A small trick to bypass any ros2 architecture and ros gazebo ignition bridge to control gazebo environment directly from bash using python scripts.

In this package we are trying to an alternative to controlling gazebo simulations with or without ROS. In the test folder we have 3 files.
1. pose_publisher.sdf
2. demo.py
3. PPO_env_reset.py

In the pose_publisher.sdf file we have a gazebo world demonstrating pose_publisher plugin. In the demp.py we are using the subprocess function to access the linux bash and interacting the Ignition gazebo from bash. As you can observe from the script, we are starting the world, resuming the paused environment and getting the pose messages in a string format. We can parse the messages we want

