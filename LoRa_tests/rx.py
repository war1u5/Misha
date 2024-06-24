import os
import serial
import time
import sys

VALID_PACKET_IDENTIFIER = b'\x01'


def receive_packets_via_serial(com_port='COM7', baudrate=115200, output_folder='received_packets'):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    ser = serial.Serial(com_port, baudrate, timeout=10)
    time.sleep(5)
    received_packets = {}
    hex_output_file = os.path.join(output_folder, 'received_packets_hex.txt')

    try:
        with open(hex_output_file, 'w') as hex_file:
            while True:
                if ser.in_waiting > 0:
                    packet = ser.read(131)
                    hx = packet.hex()
                    print(f"Packet received: {hx}")
                    if packet.startswith(VALID_PACKET_IDENTIFIER):
                        packet_number = int.from_bytes(packet[1:3], 'big')
                        data_without_identifier = packet[3:]
                        received_packets[packet_number] = data_without_identifier
                        sys.stdout.write(f"\rReceived valid packets: {len(received_packets)}")
                        sys.stdout.flush()
                        packet_hex = packet.hex()
                        hex_file.write(f"Received packet {packet_number} (hex): {packet_hex}\n")
                        packet_file_path = os.path.join(output_folder, f'packet_{packet_number}.bin')
                        with open(packet_file_path, 'wb') as packet_file:
                            packet_file.write(data_without_identifier)
                        print(f"Received packet {packet_number}: {data_without_identifier}")
    except KeyboardInterrupt:
        pass
    finally:
        ser.close()
    print("\nAll valid packets received.")
    expected_packets = max(received_packets.keys()) + 1
    if len(received_packets) == expected_packets:
        print("All packets received successfully.")
    else:
        missing_packets = set(range(expected_packets)) - set(received_packets.keys())
        print(f"Missing packets: {sorted(missing_packets)}")


if __name__ == "__main__":
    receive_packets_via_serial()
