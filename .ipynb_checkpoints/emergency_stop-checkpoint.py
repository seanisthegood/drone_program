from codrone_edu.drone import *

# EMERGENCY STOP SCRIPT
# Run this script in a separate terminal if you need to emergency stop the drone

print("🚨 EMERGENCY STOP SCRIPT 🚨")
print("This will attempt to connect and stop any active drone")

try:
    drone = Drone()
    drone.pair()
    
    print("Connected to drone - executing emergency stop...")
    
    # Multiple stop methods
    try:
        drone.emergency_stop()
        print("✅ Emergency stop successful")
    except:
        try:
            drone.stop()
            print("✅ Stop command successful")
        except:
            try:
                # Manual control stop
                drone.set_throttle(0)
                drone.set_pitch(0) 
                drone.set_roll(0)
                drone.set_yaw(0)
                drone.land()
                print("✅ Manual stop and land successful")
            except:
                print("❌ Unable to stop drone remotely")
    
    drone.close()
    print("✅ Drone disconnected")
    
except Exception as e:
    print(f"❌ Could not connect to drone: {e}")
    print("Manual intervention may be required")
    
print("\nEmergency stop script completed.")
input("Press Enter to exit...")
