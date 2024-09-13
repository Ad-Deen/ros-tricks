import subprocess
import time
import json

def launch_gazebo_in_new_bash():
    try:
        # Step 1: Launch Gazebo in a new bash instance
        gazebo_process = subprocess.Popen(
            ['bash', '-c', 'ign gazebo pose_publisher.sdf'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        print("Launching Gazebo environment in a new bash shell...")
        return gazebo_process

    except Exception as e:
        print(f"Error launching Gazebo: {e}")
        return None

def echo_ign_topic_in_new_bash():
    try:
        # Step 2: Echo the Ignition topic in another new bash instance
        topic_process = subprocess.Popen(
            ['bash', '-c', 'ign topic -e -t /model/double_pendulum_with_base/pose'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        print("Echoing topic data in another bash shell...")

        # Step 3: Continuously read the output from the topic echo
        while True:
            output = topic_process.stdout.readline()
            if output:
                # Print the raw output
                print(f"Raw Output: {output.strip()}")

                # Print the type of the data
                # print(f"Type of data received: {type(output)}")       #type of msg is in string format , so we can use indexing or string search 
                #                                                       to get the data we need

            elif topic_process.poll() is not None:
                break

        # Get any errors from the topic echo process
        stderr = topic_process.communicate()[1]
        if stderr:
            print(f"Topic Echo Error: {stderr}")

    except Exception as e:
        print(f"An error occurred while echoing topic: {e}")


def control_simulation(command):
    # Construct the Ignition command to control the simulation (pause/resume)
    control_command = (
        f'ign service -s /world/pose_publisher/control '
        '--reqtype ignition.msgs.WorldControl --reptype ignition.msgs.Boolean '
        '--timeout 300 --req '
        f'\'pause: {command == "pause"}\''
    )

    try:
        # Run the command in a separate bash shell
        control_process = subprocess.Popen(
            ['bash', '-c', control_command],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        print(f"Sending {command} command to simulation...")

        # Get the output from the command
        stdout, stderr = control_process.communicate()

        if stdout:
            print(f"Command Output:\n{stdout}")
        if stderr:
            print(f"Error Output:\n{stderr}")

    except Exception as e:
        print(f"Failed to control the simulation: {e}")

if __name__ == "__main__":
    # Launch Gazebo in one bash shell
    gazebo_process = launch_gazebo_in_new_bash()

    if gazebo_process:
        # Wait for 2 seconds to allow Gazebo to start
        time.sleep(2)

        # Send the resume command to unpause the simulation
        control_simulation("resume")

        # Launch the echo command in another bash shell
        echo_ign_topic_in_new_bash()
