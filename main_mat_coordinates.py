from codrone_edu.drone import *
import time
import json
from datetime import datetime

def log_position(drone, label, log):
    pos = drone.get_position_data()
    print(f"{label} position: {pos}")
    log.append({"label": label, "position": pos, "time": datetime.now().isoformat()})
    return pos

def main():
    drone = Drone()
    drone.pair()
    drone_active = True
    log = []
    filename = f"flight_log_mat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    try:
        drone.set_drone_LED(0, 0, 255, 100)  # Blue LED for mat mode
        drone.takeoff()
        print("Takeoff command sent.")
        time.sleep(1)
        # drone.set_throttle(2)
        time.sleep(.5)
        print("Ascended to target height.")
        time.sleep(.5)
        start_pos = log_position(drone, "start", log)
        # drone.triangle(speed=10, seconds=10, direction=-.25)



        # # Move right 50cm (x+)  
        drone.move_backward(75,"cm",.5)
        # print("Move right 0.5m command sent.")
        time.sleep(1)
        pos1 = log_position(drone, "(50,0)", log)

        # Move forward 50cm (y+)
        drone.turn_right(90)
        # print("Move forward 0.5m command sent.")
        time.sleep(1)
        # pos2 = log_position(drone, "(50,50)", log)

        # # Move left 50cm (x-)
        drone.square(speed=50, seconds=2, direction=1)
        # print("Move left 0.5m command sent.")
        time.sleep(2)
        # pos3 = log_position(drone, "(0,50)", log)

        # drone.turn_left(90)
        # drone.move_forward(25,"cm",.5)


        # Move backward 50cm (y-)
        # drone.move_backward(0.5)
        # print("Move backward 0.5m command sent.")
        # time.sleep(2)
        # pos4 = log_position(drone, "(0,0) (end)", log)

        drone.land()
        print("Land command sent.")
        drone.close()
        drone_active = False
        print("Drone closed.")

        with open(filename, 'w') as f:
            json.dump(log, f, indent=2)
        print(f"Flight log saved to: {filename}")
    except KeyboardInterrupt:
        print("\nCTRL+C detected. Landing drone.")
        if drone_active:
            drone.land()
            drone.close()
        with open(filename, 'w') as f:
            json.dump(log, f, indent=2)
        print(f"Partial log saved to: {filename}")
    except Exception as e:
        print(f"\nERROR: {e}\nAttempting emergency landing...")
        if drone_active:
            try:
                drone.land()
                drone.close()
            except:
                print("Manual intervention may be needed.")
        with open(filename, 'w') as f:
            json.dump(log, f, indent=2)
        print(f"Partial log saved to: {filename}")

if __name__ == "__main__":
    main()
