from codrone_edu.drone import *
import time

drone = Drone()
drone.pair()

# WITHOUT MAT - Uses internal sensors and timing
drone.set_drone_LED(255, 0, 0, 100)  # Red LED to indicate no mat mode

drone.takeoff()

# Set basic flight parameters
speed = 30  # Lower speed for more control
duration = 1.5  # Time-based movement

# Move in a square pattern using throttle/pitch controls
for i in range(4):
    print(f"Side {i+1} of square")
    
    # Move forward using pitch control
    drone.set_pitch(speed)
    drone.move(duration)
    drone.set_pitch(0)  # Stop forward movement
    
    # Brief pause for stability
    time.sleep(0.5)
    
    # Turn right using yaw control
    drone.set_yaw(speed)
    drone.move(0.8)  # Turn duration
    drone.set_yaw(0)  # Stop turning
    
    time.sleep(0.5)

# Try to return to starting position (less precise without mat)
drone.set_pitch(-speed)  # Move backward
drone.move(duration)
drone.set_pitch(0)

drone.set_roll(-speed)  # Move left
drone.move(duration)
drone.set_roll(0)

# Hover before landing
time.sleep(2)

drone.land()
drone.close()
