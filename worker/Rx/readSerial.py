import serial
import serial.serialutil

COM_PORT = 'COM8'
BAUD_RATE = 115200

try:
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)  # Set a timeout value in seconds
    print(f"Connected to {COM_PORT} at {BAUD_RATE} baud")

    while True:
        data = ser.readline().decode().strip()
        print(data)

except serial.serialutil.SerialTimeoutException:
    print("Serial communication timed out.")
except serial.SerialException as e:
    print(f"Error: {e}")
finally:
    if ser.is_open:
        ser.close()
        print("Serial port closed")
