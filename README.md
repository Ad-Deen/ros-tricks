# ros-tricks

A simple trick to bypass the ROS2 architecture and the ROS-Gazebo Ignition bridge to control the Gazebo environment directly from Bash using Python scripts.

In this package, we demonstrate an alternative method to control Gazebo simulations with or without ROS. The `test` folder contains three files:
1. `pose_publisher.sdf`
2. `demo.py`
3. `PPO_env_reset.py`

### File Descriptions:

- **`pose_publisher.sdf`**: A Gazebo world file demonstrating the pose publisher plugin.
  
- **`demo.py`**: A Python script that uses the `subprocess` module to execute Bash commands and interact with Ignition Gazebo. This script launches the world, resumes the paused simulation, and retrieves pose messages in string format. It can be used to parse specific message data from echoing Ignition topics, making it suitable for integrating feedback logic into your robotics projects or execution pipeline.

- **`PPO_env_reset.py`**: A script used in a reinforcement learning environment to reset the Gazebo world. While we can't show the full RL setup right now, the script illustrates how Ignition services can be called directly in ROS nodes. This approach is useful because ROS services are currently underdeveloped and often limited to pausing and unpausing the simulation. In contrast, Ignition services offer more control and flexibility.

### Instructions:

Go to the `test` folder and execute the following command to test the raw Python functionality:
```bash
python3 demo.py
```
There is also the PPO_env_reset.py script, which I used in my reinforcement learning setup to reset the Gazebo world. Even though the full RL environment package isn't provided, you can still learn how to use Ignition services in ROS nodes without relying on the ROS service interface. The ROS service interface is limited and can only pause/unpause the simulation, while Ignition services offer a broader range of functionality.
