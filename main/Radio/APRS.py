import subprocess
import time

def begin_APRS_recieve(path):
    with open(path, "w") as file:
        process = subprocess.Popen(["rtl_fm", "-f", "144.390M", "-s", "22050"], 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE)
        subprocess.Popen(["multimon-ng", "-t", "raw", "-a", "AFSK1200", "-f", "alpha", "/dev/stdin"], 
                         stdin=process.stdout, 
                         stdout=file, 
                         stderr=subprocess.PIPE)
    return process