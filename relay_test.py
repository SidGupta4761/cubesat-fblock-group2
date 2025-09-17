import subprocess
import os

# === CONFIG ===
mac_ip = "192.168.201.119"
mac_user = "siddharthagupta"  # <-- your Mac username
mac_dest_dir = "~/Downloads/cubesat_fly_data"
file_to_send = "picture0.jpg"
# ==============

# --- Check if the file exists before trying to send ---
if not os.path.exists(file_to_send):
    print(f"[ERROR] File '{file_to_send}' does not exist. Please capture it first.")
    exit(1)

# --- Relay the file ---
print(f"[INFO] Sending {file_to_send} to {mac_user}@{mac_ip}:{mac_dest_dir}...")
result = subprocess.run([
    "scp", file_to_send, f"{mac_user}@{mac_ip}:{mac_dest_dir}/"
])

# --- Confirm result ---
if result.returncode == 0:
    print("[SUCCESS] File successfully relayed to Mac.")
else:
    print("[ERROR] File relay failed. Check SSH and file permissions.")
