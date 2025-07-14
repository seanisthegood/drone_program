# Additional sensor functions you can use for more metrics:

# Motion sensors
gyro_data = drone.get_gyro()              # Gyroscope readings
accel_data = drone.get_accelerometer()    # Acceleration data
velocity = drone.get_optical_flow_velocity()  # Movement velocity

# Environmental sensors  
pressure = drone.get_barometer()          # Air pressure
temperature = drone.get_temperature()     # Temperature

# Flight state
trim_data = drone.get_trim()              # Trim settings
state = drone.get_state()                 # Flight state info

# Example of adding these to your flight log:
sensor_reading = {
    "timestamp": time.time(),
    "gyro": gyro_data,
    "accelerometer": accel_data,
    "velocity": velocity,
    "pressure": pressure,
    "temperature": temperature,
    "trim": trim_data,
    "state": state
}
flight_data["sensor_readings"].append(sensor_reading)
