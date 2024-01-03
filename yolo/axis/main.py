from dotenv import load_dotenv
import os
from pyaxis import AxisCam

load_dotenv()
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
ip_address = os.getenv('IP_ADDRESS')
port = os.getenv('PORT')

cam = AxisCam(username, password, ip_address, port)
cam.get_yolo_detections()
