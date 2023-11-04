import serial

# Define the COM port and baud rate
COM_PORT = 'COM8'
BAUD_RATE = 115200

try:
    # Open the serial port
    ser = serial.Serial(COM_PORT, BAUD_RATE)
    print(f"Connected to {COM_PORT} at {BAUD_RATE} baud")

    # Read and display data from the serial port
    while True:
        data = ser.readline().decode().strip()
        print("Received data:", data)

except serial.SerialException as e:
    print(f"Error: {e}")
finally:
    # Close the serial port when done
    if ser.is_open:
        ser.close()
        print("Serial port closed")
