from codrone_edu.drone import *
import time

drone = Drone()
drone.pair()

# WITH MAT - Uses optical flow and visual tracking
drone.set_drone_LED(0, 255, 0, 100)  # Green LED

drone.takeoff()

# Precise movement using mat's visual reference points
drone.go_to_height(1)  # Set height to 1 meter
time.sleep(2)

# Move in a square pattern using optical flow sensor + mat
for i in range(4):
    # Get precise position from optical flow
    start_pos = drone.get_position_data()
    print(f"Starting position: {start_pos}")
    
    # Move forward 50cm - very accurate with mat
    drone.move_forward(0.5)
    
    # Verify actual movement
    end_pos = drone.get_position_data()
    print(f"End position: {end_pos}")
    
    time.sleep(1)
    drone.turn_right(90)  # Precise 90-degree turn
    time.sleep(1)

# Return to exact starting position
drone.move_backward(0.5)
drone.move_left(0.5)

# Use color detection on mat
color = drone.get_color_data()
if color:
    print(f"Detected color on mat: {color}")

drone.land()
drone.close()
