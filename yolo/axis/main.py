import threading
import torch
from dotenv import load_dotenv
import os
from pyaxis import AxisCam

from message_generator import MessageGenerator

load_dotenv()
username = os.getenv('USER')
password = os.getenv('PASSWORD')
ip_address = os.getenv('IP_ADDRESS')
port = os.getenv('PORT')

print(f"CUDA enabled: {torch.cuda.is_available()}")
print(torch.zeros(1).cuda())

message_generator = MessageGenerator()
threading.Thread(target=message_generator.run).start()

cam = AxisCam(username, password, ip_address, port)
# cam.get_live_feed()
cam.get_yolo_detections(message_generator)
