from codrone_edu.drone import *
drone = Drone()
drone.pair()

speed = 40
duration = 1

drone.takeoff()

drone.set_pitch(speed)

drone.set_throttle(speed)

drone.move(duration)

drone.set_throttle(-speed)

drone.move(duration)

drone.set_throttle(speed)

drone.move(duration)

drone.set_throttle(-speed)

drone.move(duration)

drone.land()

drone.close()