from codrone_edu.drone import *
import time
import threading

drone = Drone()
drone.pair()

# Global control variables
user_command = None
flight_active = True

def get_user_input():
    """Get real-time commands from user"""
    global user_command, flight_active
    while flight_active:
        cmd = input("Enter command (w/a/s/d/q/land): ").lower().strip()
        user_command = cmd
        if cmd == 'land':
            flight_active = False
        time.sleep(0.1)

def execute_command(drone):
    """Execute user commands"""
    global user_command
    if user_command == 'w':  # Forward
        drone.move_forward(0.2)
        print("Moving forward")
    elif user_command == 's':  # Backward
        drone.move_backward(0.2)
        print("Moving backward")
    elif user_command == 'a':  # Left
        drone.move_left(0.2)
        print("Moving left")
    elif user_command == 'd':  # Right
        drone.move_right(0.2)
        print("Moving right")
    elif user_command == 'q':  # Up
        drone.move_up(0.2)
        print("Moving up")
    elif user_command == 'e':  # Down
        drone.move_down(0.2)
        print("Moving down")
    elif user_command == 'land':
        drone.land()
        print("Landing...")
        return False
    
    user_command = None  # Clear command
    return True

# Start input thread
input_thread = threading.Thread(target=get_user_input, daemon=True)
input_thread.start()

print("🚁 INTERACTIVE DRONE CONTROL")
print("Commands: w=forward, s=back, a=left, d=right, q=up, e=down, land=land")
print("=" * 60)

drone.takeoff()

# Interactive flight loop
while flight_active:
    if user_command:
        if not execute_command(drone):
            break
    time.sleep(0.1)  # Small delay

drone.close()
print("Flight ended!")
