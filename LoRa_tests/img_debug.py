from PIL import Image
import numpy as np
import os


def rebuild_image_from_packets(packets_folder, output_image_path, image_width, image_height, packet_size=70):
    """
    Rebuild the image from saved packets.
    """
    # List all packet files in the packets_folder
    packet_files = sorted([f for f in os.listdir(packets_folder) if f.startswith('packet_')], key=lambda x: int(x.split('_')[1].split('.')[0]))
    print(packet_files)
    # Initialize an empty list to store packet data
    all_packets = []

    # Read each packet file and append packet data
    for filename in packet_files:
        with open(os.path.join(packets_folder, filename), 'rb') as f:
            packet_data = f.read()
            all_packets.append(packet_data)

    # Concatenate all packets into a single byte stream
    image_bytes = b''.join(all_packets)

    # Ensure the byte stream is the correct length
    expected_length = image_width * image_height
    if len(image_bytes) != expected_length:
        print(f"Warning: Expected image bytes length is {expected_length}, but got {len(image_bytes)}")

    # Reconstruct image from byte stream
    img = Image.frombytes('L', (image_width, image_height), image_bytes[:expected_length])

    # Save the reconstructed image
    img.save(output_image_path)
    print(f"Reconstructed image saved at {output_image_path}")

    # Display the reconstructed image
    img.show()


if __name__ == "__main__":
    packets_folder = 'received_packets'  # Folder where received packets are saved
    output_image_path = 'reconstructed_image.jpg'
    image_width, image_height = 128, 128  # Known dimensions of the image

    # Rebuild the image from received packets
    rebuild_image_from_packets(packets_folder, output_image_path, image_width, image_height)
