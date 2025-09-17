import adafruit_fxos8700
import adafruit_fxas21002c
import time
import os
import board
import busio
from picamera2 import Picamera2
import numpy as np
import sys
from sensor_calc import set_initial, compute_angle, calibrate_mag, calibrate_gyro

# Set up I2C and sensors
i2c = busio.I2C(board.SCL, board.SDA)
sensor1 = adafruit_fxos8700.FXOS8700(i2c)  # Accelerometer + Magnetometer
sensor2 = adafruit_fxas21002c.FXAS21002C(i2c)  # Gyroscope
camera = Picamera2()

# Code to take a picture at a given offset angle
def capture(dir='roll', target_angle=30):
    dir = dir.lower()  # Ensure consistency
    if dir not in ['roll', 'pitch', 'yaw']:
        print("Invalid direction. Must be one of: roll, pitch, yaw")
        return

    # Uncomment if you implement calibration
    offset_mag = calibrate_mag()  # Default is [0, 0, 0]
    # offset_gyro = calibrate_gyro()  # Optional if using gyro logic

    # Get initial sensor readings
    accelX, accelY, accelZ = sensor1.accelerometer
    magX, magY, magZ = sensor1.magnetometer
    initial_rpy = set_initial(accelX, accelY, accelZ, magX, magY, magZ, offset_mag)

    print("Begin moving camera...")
    time.sleep(1)

    while True:
        # Read IMU
        accelX, accelY, accelZ = sensor1.accelerometer
        magX, magY, magZ = sensor1.magnetometer

        # Apply magnetometer offset
        magX -= offset_mag[0]
        magY -= offset_mag[1]
        magZ -= offset_mag[2]

        # Compute the current angle
        angle = compute_angle(accelX, accelY, accelZ, magX, magY, magZ, axis=dir)

        print(f"{dir.capitalize()} = {angle:.2f}°, Target = {target_angle}°")

        # Margin for error: ±3°
        if abs(angle - float(target_angle)) < 3:
            print("Target angle reached! Capturing image...")

            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f"image_{dir}_{target_angle}_{timestamp}.jpg"

            camera.start()
            time.sleep(0.5)  # Let camera warm up
            camera.capture_file(filename)
            camera.stop()

            print(f"Image saved as {filename}")
            break

        time.sleep(0.1)


if __name__ == '__main__':
    # Example: python3 auto_camera.py yaw 45
    args = sys.argv[1:]
    if len(args) != 2:
        print("Usage: python3 auto_camera.py <axis> <target_angle>")
    else:
        capture(args[0], float(args[1]))
