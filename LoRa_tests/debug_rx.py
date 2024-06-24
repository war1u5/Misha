import serial
import time
import os


def receive_packets_via_serial(com_port='COM7', baudrate=115200):
    ser = serial.Serial(com_port, baudrate, timeout=10)
    time.sleep(2)  # Wait for serial connection to stabilize

    received_packets = []

    try:
        while True:
            if ser.in_waiting > 0:
                packet = ser.read(71)  # Adjust packet size based on sender's packet_size

                # Convert packet to hexadecimal format
                hex_data = ' '.join([f'{byte:02X}' for byte in packet])
                print(f"Received packet (hex): {hex_data}")

    except KeyboardInterrupt:
        pass
    finally:
        ser.close()


if __name__ == "__main__":
    receive_packets_via_serial()
