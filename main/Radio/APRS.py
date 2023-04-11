import subprocess
import time

def begin_APRS_recieve(path):
    with open(path, "w") as file:
        process1 = subprocess.Popen(["rtl_fm", "-f", "144.390M", "-s", "22050"], 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE)
        process2 = subprocess.Popen(["multimon-ng", "-t", "raw", "-a", "AFSK1200", "-f", "alpha", "/dev/stdin"], 
                         stdin=process1.stdout, 
                         stdout=file, 
                         stderr=subprocess.PIPE)
    return process1, process2


if __name__ == "__main__":
    output_file_path = "decoded_APRS_data.txt"
    process = begin_APRS_recieve(output_file_path)

    try:
        print(f"APRS reception started. Decoded data will be written to: {output_file_path}")
        while True:
            time.sleep(1)  # Keep the script running and check for termination every second
    except KeyboardInterrupt:
        print("Terminating the APRS reception process...")
        process.terminate()  # Terminate the rtl_fm process when the user interrupts the script (e.g., with Ctrl+C)
        process.wait()  # Wait for the process to actually terminate
        print("APRS reception process terminated.")