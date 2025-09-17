from time import sleep
import subprocess

print("start")
for i in range(12):
    filename = f"picture{i}.jpg"
    subprocess.run([
        "libcamera-still",
        "--width", "640",            # Lower resolution
        "--height", "480",
        "--timeout", "1",            # 1ms delay
        "--immediate",               # No delay waiting for AE
        "-n",                        # No preview
        "-o", filename
    ])
    print(f"Captured {filename}")
print("finish")

