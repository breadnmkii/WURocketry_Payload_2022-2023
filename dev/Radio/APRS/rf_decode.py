import subprocess
import time

# Launch the subprocess
with open("data", "w") as file:
    process = subprocess.Popen(["rtl_fm", "-f", "144.390M", "-s", "22050"], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE)
    subprocess.Popen(["multimon-ng", "-t", "raw", "-a", "AFSK1200", "-f", "alpha", "/dev/stdin"], 
                     stdin=process.stdout, 
                     stdout=file, 
                     stderr=subprocess.PIPE)

# Read the data in the main Python code
while True:
    with open("data") as file:
        data = file.readlines()
    print(data)
    time.sleep(1)
