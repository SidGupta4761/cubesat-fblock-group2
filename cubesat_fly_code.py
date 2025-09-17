import subprocess
import time
from datetime import datetime
import board
import busio
import adafruit_bno055
import os

# ==== CONFIG ====
mac_ip = "192.168.201.119"
mac_user = "siddharthagupta"  # <-- your Mac username
mac_dest_dir = "~/Downloads/cubesat_fly_data"
log_filename = "imu_log.txt"
image_prefix = "fly_image_"
num_images = 10
interval = 0.5  # seconds
data_folder = "fly_output"
# ================

# Ensure clean output folder
os.makedirs(data_folder, exist_ok=True)

# Setup IMU
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)

# Initialize motion state
velocity = 0.0  # m/s
position = 0.0  # m
last_time = time.time()

# Prepare log file
log_path = os.path.join(data_folder, log_filename)
with open(log_path, "w") as log:
    log.write("timestamp, image_file, accel_x, velocity, position, mag_x, mag_y, mag_z\n")

# Start capture loop
print("Starting capture sequence...")
for i in range(num_images):
    current_time = time.time()
    dt = current_time - last_time
    last_time = current_time

    timestamp = datetime.utcnow().isoformat()
    image_file = f"{image_prefix}{i}.jpg"
    image_path = os.path.join(data_folder, image_file)

    # Capture image
    subprocess.run([
        "libcamera-still",
        "--width", "640", "--height", "480",
        "--timeout", "1",
        "--immediate",
        "-n",
        "-o", image_path
    ])

    # Read IMU data
    try:
        accel = sensor.acceleration  # (x, y, z) in m/s^2
        mag = sensor.magnetic        # (x, y, z) in microteslas
        ax = accel[0] if accel and accel[0] is not None else 0.0
    except Exception as e:
        print(f"[WARN] IMU read failed: {e}")
        ax = 0.0
        mag = (None, None, None)

    # Integrate to get velocity and position (simple Euler method)
    velocity += ax * dt
    position += velocity * dt

    # Log data
    with open(log_path, "a") as log:
        log.write(f"{timestamp}, {image_file}, {ax:.4f}, {velocity:.4f}, {position:.4f}, "
                  f"{mag[0]}, {mag[1]}, {mag[2]}\n")

    print(f"[{i+1}/{num_images}] {image_file} | a={ax:.2f} m/s² | v={velocity:.2f} m/s | x={position:.2f} m")
    time.sleep(interval)

print("Capture complete. Transferring files to Mac...")

# --- Single scp transfer (one password prompt) ---
subprocess.run([
    "scp", "-r", data_folder, f"{mac_user}@{mac_ip}:{mac_dest_dir}/"
])

print("✅ Transfer complete.")
