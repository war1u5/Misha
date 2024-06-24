from PIL import Image
import numpy as np
import serial
import time
import os

VALID_PACKET_IDENTIFIER = b'\x01'


def compress_image(input_image_path, output_image_path, max_width, max_height, quality=20):
    with Image.open(input_image_path) as img:
        img = img.convert("RGB")
        img.thumbnail((max_width, max_height))
        img.save(output_image_path, format='JPEG', quality=quality)
        print(f"Image saved at {output_image_path} with size {img.size}")


def image_to_packets(image_path):
    with Image.open(image_path) as img:
        img = img.convert('L')
        image_data = np.array(img).flatten()
    image_bytes = image_data.tobytes()
    total_length = len(image_bytes)
    packets = [image_bytes[i:i + 128] for i in range(0, total_length, 128)]
    return packets


def save_packets(packets, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for i, packet in enumerate(packets):
        with open(f"{output_folder}/packet_{i}.bin", "wb") as f:
            f.write(packet)
        print(f"Saved packet {i} with size {len(packet)} bytes")


def send_packets_via_serial(packets, com_port='COM5', baudrate=9600, output_file='sent_packets_hex.txt'):
    ser = serial.Serial(com_port, baudrate)
    time.sleep(5)
    print("Init Done")
    with open(output_file, 'w') as hex_file:
        for i, packet in enumerate(packets):
            packet_number = i.to_bytes(2, 'big')  # Use 2 bytes for packet number
            packet_with_identifier = VALID_PACKET_IDENTIFIER + packet_number + packet
            print(packet_with_identifier)
            ser.write(packet_with_identifier)
            packet_hex = packet_with_identifier.hex()
            hex_file.write(f"Sent packet {i} (hex): {packet_hex} with size {len(packet_with_identifier)} bytes\n")
            print(f"Sent packet {i} (hex): {packet_hex} with size {len(packet_with_identifier)} bytes")
            time.sleep(6)
    ser.close()
    print("All packets sent.")
    print(f"Hex data saved to: {output_file}")


if __name__ == "__main__":
    input_image_path = 'meme.png'
    compressed_image_path = 'sent_compressed.jpg'
    output_folder = 'sent_packets'
    hex_output_file = 'sent_packets_hex.txt'
    max_width, max_height = 128, 128
    compress_image(input_image_path, compressed_image_path, max_width, max_height)
    packets = image_to_packets(compressed_image_path)
    save_packets(packets, output_folder)
    send_packets_via_serial(packets, com_port='COM5', baudrate=9600, output_file=hex_output_file)
    print(f"Total packets created: {len(packets)}")
