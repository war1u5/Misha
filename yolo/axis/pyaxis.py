import cv2
from ultralytics import YOLO
from dotenv import load_dotenv
import os


class AxisCam:
    def __init__(self, username, password, ip, port):
        self.base_url = f'http://{username}:{password}@{ip}:{port}'
        print(f"Initialized with the following creds: "
              f"\nUsername: {username}"
              f"\nPassword: {password}"
              f"\nIP: {ip}"
              f"\nPORT: {port}")

    def get_live_feed(self):
        url = self.base_url + '/axis-cgi/mjpg/video.cgi'

        cap = cv2.VideoCapture(url)

        if not cap.isOpened():
            print("Error: Could not open camera stream.")
            exit()

        cv2.namedWindow('Axis Camera Stream', cv2.WINDOW_NORMAL)
        while True:
            # Read a frame from the camera stream
            ret, frame = cap.read()

            if not ret:
                print("Error: Could not read frame.")
                break

            cv2.imshow('Axis Camera Stream', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def get_yolo_detections(self, message_generator):
        load_dotenv()
        model_path = os.getenv('MODEL_PATH')
        model = YOLO(model_path)

        cap = cv2.VideoCapture(self.base_url + '/axis-cgi/mjpg/video.cgi')

        while True:
            ret, frame = cap.read()

            if not ret:
                print("Error: Could not read frame.")
                break

            results = model.predict(frame, show=True, conf=0.5, device=0)
            # to do: based on the results, send a message via LoRa
            message_generator.message_queue.put(results)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
