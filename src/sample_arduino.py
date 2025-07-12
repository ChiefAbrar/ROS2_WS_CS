import time
import random
import serial

# Replace this with the 2nd port shown by socat
PORT = "/dev/pts/5"   # Example
BAUD = 115200

ser = serial.Serial(PORT, BAUD)

print(f"Running without an real-life Arduino on {PORT}")

while True:
    a = random.randint(-100, 100)
    b = random.uniform(-1.0, 1.0)
    c = random.randint(0, 1023)
    d = "Henlo"

    line = f"{a},{b:.2f},{c},{d}\n"
    ser.write(line.encode())
    print(f"Sent: {line.strip()}")

    if ser.in_waiting:
        cmd = ser.read().decode().strip()
        if cmd == '1':
            print("LED ON")
        elif cmd == '0':
            print("LED OFF")

    time.sleep(1)