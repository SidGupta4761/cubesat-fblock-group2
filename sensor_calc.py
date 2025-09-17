#sensor_calc.py
import time
import numpy as np
import adafruit_bno055
import time
import os
import board
import busio

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)

#Activity 1: RPY based on accelerometer and magnetometer
def roll_am(accelX,accelY,accelZ):
    roll = np.arctan2(accelY, accelZ)
    return ((180/np.pi) * roll + 265) * 2 - 183

def pitch_am(accelX,accelY,accelZ):
    pitch = np.arctan2(-accelX, np.sqrt(accelY**2 + accelZ**2))
    return ((180/np.pi)* pitch)*2 

def yaw_am(accelX,accelY,accelZ,magX,magY,magZ):
    roll = np.radians(roll_am(accelX, accelY, accelZ))
    pitch = np.radians(pitch_am(accelX, accelY, accelZ))
    mag_x = magX * np.cos(pitch) + magZ * np.sin(pitch)
    mag_y = magX * np.sin(roll) * np.sin(pitch) + magY * np.cos(roll) - magZ * np.sin(roll) * np.cos(pitch)
    return ((180/np.pi)*np.arctan2(-mag_y, mag_x) + 27.5) * 142.5/90 + 77

#Activity 2: RPY based on gyroscope
def roll_gy(prev_angle, delT, gyro):
    roll = prev_angle + gyro * delT
    return roll
def pitch_gy(prev_angle, delT, gyro):
    pitch = prev_angle + gyro * delT
    return pitch
def yaw_gy(prev_angle, delT, gyro):
    yaw = prev_angle + gyro * delT
    return yaw

def set_initial(mag_offset = [175,0,-175]):
    #Sets the initial position for plotting and gyro calculations.
    print("Preparing to set initial angle. Please hold the IMU still.")
    time.sleep(3)
    print("Setting angle...")
    accelX, accelY, accelZ = sensor.acceleration #m/s^2
    magX, magY, magZ = sensor.magnetic #gauss
    #Calibrate magnetometer readings. Defaults to zero until you
    #write the code
    magX = magX - mag_offset[0]
    magY = magY - mag_offset[1]
    magZ = magZ - mag_offset[2]
    roll = roll_am(accelX, accelY,accelZ)
    pitch = pitch_am(accelX,accelY,accelZ)
    yaw = yaw_am(accelX,accelY,accelZ,magX,magY,magZ)
    print("Initial angle set.")
    return [roll,pitch,yaw]

def calibrate_mag():
    # Placeholder: returns zero offsets
    return [0, 0, 0]

def calibrate_gyro():
    # Placeholder: returns zero offsets
    return [0, 0, 0]

def compute_angle(accelX, accelY, accelZ, magX, magY, magZ, axis='roll'):
    if axis == 'roll':
        return roll_am(accelX, accelY, accelZ)
    elif axis == 'pitch':
        return pitch_am(accelX, accelY, accelZ)
    elif axis == 'yaw':
        return yaw_am(accelX, accelY, accelZ, magX, magY, magZ)
    else:
        raise ValueError("Axis must be 'roll', 'pitch', or 'yaw'")