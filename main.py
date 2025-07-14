from codrone_edu.drone import *
import time
import json
from datetime import datetime

# Emergency stop flag
emergency_stop = False

def emergency_stop_drone(drone):
    """Emergency stop function - stops all motors immediately"""
    print("\n🚨 EMERGENCY STOP ACTIVATED! 🚨")
    try:
        drone.emergency_stop()  # Immediate motor cutoff
        # Alternative methods if emergency_stop() doesn't exist:
        # drone.stop()  # or
        # drone.land()  # or 
        # drone.set_throttle(0)
        # drone.set_pitch(0)
        # drone.set_roll(0)
        # drone.set_yaw(0)
    except:
        # Fallback - cut all movement
        drone.set_throttle(0)
        drone.set_pitch(0)
        drone.set_roll(0)
        drone.set_yaw(0)
    
    drone.close()
    print("Drone stopped and disconnected.")
    exit()

drone = Drone()
drone.pair()
drone_active = True  # Track if drone is still active

print("🚨 EMERGENCY STOP OPTIONS:")
print("1. Press Ctrl+C in terminal to LAND and STOP immediately")
print("2. Close this program window")
print("3. Turn off drone manually if needed")
print("4. Run 'python emergency_stop.py' in another terminal")
print("=" * 60)

try:
    # Flight metrics storage
    flight_data = {
        "flight_start": datetime.now().isoformat(),
        "movements": [],
        "sensor_readings": [],
        "flight_summary": {}
    }

    # Create filename once for consistent logging
    filename = f"flight_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    # Enable optical flow for position control on the mat
    drone.set_drone_LED(0, 255, 0, 100)  # Green LED to indicate ready

    drone.takeoff()
    print("Takeoff command sent.")
    flight_start_time = time.time()

    # Gently ascend to about 1 meter (adjust duration as needed)
    drone.set_throttle(5)  # Set a moderate upward speed
    time.sleep(1.2)         # Adjust this value for your drone/model
    drone.set_throttle(0)   # Stop ascending
    print("Ascended to target height.")
    time.sleep(1)           # Brief hover to stabilize

    # Record initial position
    initial_pos = drone.get_position_data()
    initial_battery = drone.get_battery()

    # Get drone system info (if available)
    try:
        drone_info = {
            "firmware_version": drone.get_version(),
            "serial_number": drone.get_serial_number(),
            "hardware_info": drone.get_hardware_info()
        }
        print(f"Drone Info: {drone_info}")
        flight_data["flight_summary"]["drone_info"] = drone_info
    except:
        print("Drone system info not available")

    flight_data["flight_summary"]["initial_position"] = initial_pos
    flight_data["flight_summary"]["initial_battery"] = initial_battery

    # Move in a square pattern using sensor feedback
    print("\n--- Starting Square Pattern ---")
    for i in range(4):
        print(f"\n--- Side {i+1} ---")
        start_pos = drone.get_position_data()
        start_time = time.time()
        print(f"Starting position: {start_pos}")
        drone.move_forward(0.5)  # Move forward 50cm
        print("Move forward command sent.")
        end_pos = drone.get_position_data()
        end_time = time.time()
        battery = drone.get_battery()
        print(f"End position: {end_pos}")
        print(f"Battery: {battery}%")
        movement_data = {
            "segment": i + 1,
            "start_position": start_pos,
            "end_position": end_pos,
            "start_time": start_time,
            "end_time": end_time,
            "duration": end_time - start_time,
            "battery_level": battery
        }
        flight_data["movements"].append(movement_data)
        try:
            with open(filename, 'w') as f:
                json.dump(flight_data, f, indent=2)
        except:
            pass
        time.sleep(1)
        drone.turn_right(90)
        print("Turn right command sent.")
        time.sleep(1)
    print("\n--- Square Pattern Complete ---\n")

    # Return to starting position using optical flow
    return_start_time = time.time()
    drone.move_backward(0.5)
    print("Move backward command sent.")
    drone.move_left(0.5)
    print("Move left command sent.")
    return_end_time = time.time()

    # Final position and metrics
    final_pos = drone.get_position_data()
    final_battery = drone.get_battery()
    total_flight_time = time.time() - flight_start_time

    # Check color sensor (if available on your mat)
    color = drone.get_color_data()
    if color:
        print(f"Detected color: {color}")
        # Convert color to string for JSON serialization
        color_str = str(color)
    else:
        color_str = None

    # Store final flight summary
    flight_data["flight_summary"].update({
        "final_position": final_pos,
        "final_battery": final_battery,
        "total_flight_time": total_flight_time,
        "return_to_home_duration": return_end_time - return_start_time,
        "detected_color": color_str,
        "flight_end": datetime.now().isoformat()
    })

    drone.land()
    print("Land command sent.")
    drone.close()
    drone_active = False  # Mark drone as closed
    print("Drone closed.")

    # Save flight data to file
    with open(filename, 'w') as f:
        json.dump(flight_data, f, indent=2)

    print(f"\n=== FLIGHT METRICS ===")
    print(f"Total Flight Time: {total_flight_time:.2f} seconds")
    print(f"Battery Used: {flight_data['flight_summary']['initial_position']} -> {final_battery}%")
    print(f"Distance Traveled: Check {filename} for detailed path")
    print(f"Flight log saved to: {filename}")

    # Print square path summary
    print("\n=== SQUARE FLIGHT SUMMARY ===")
    for move in flight_data["movements"]:
        print(f"Side {move['segment']}: Start {move['start_position']} -> End {move['end_position']} | Duration: {move['duration']:.2f}s | Battery: {move['battery_level']}%")
    print("============================\n")

    # Calculate total distance traveled
    total_distance = 0
    for movement in flight_data["movements"]:
        if movement["start_position"] and movement["end_position"]:
            # Simple distance calculation (you might want to make this more sophisticated)
            print(f"Segment {movement['segment']}: {movement['duration']:.2f}s")
    print(f"Flight data saved to: {filename}")
    print("\nScript completed successfully!")

except KeyboardInterrupt:
    print("\n🚨 CTRL+C DETECTED - LANDING DRONE SAFELY! 🚨")
    try:
        if drone_active:
            drone.land()
            print("✅ Drone landed safely")
            drone.close()
            drone_active = False
        # Save partial flight data
        with open(filename, 'w') as f:
            json.dump(flight_data, f, indent=2)
        print(f"✅ Partial flight data saved to: {filename}")
    except Exception:
        print("❌ Unable to land automatically - use emergency_stop.py")
    print("🚁 Flight ended by user")

except Exception as e:
    print(f"\n🚨 ERROR OCCURRED! 🚨")
    print(f"Error: {e}")
    try:
        if drone_active:
            print("Attempting emergency landing...")
            drone.land()
            print("✅ Emergency landing successful")
            drone.close()
            drone_active = False
        else:
            print("Drone already landed and closed. No emergency landing needed.")
    except Exception:
        print("❌ Emergency landing failed - drone may need manual intervention")
    # Optionally, save partial data or log error here