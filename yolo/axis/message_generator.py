import queue
import serial


class MessageGenerator:
    def __init__(self, port, baud_rate):
        self.message_queue = queue.Queue()
        self.serial_port = serial.Serial(port, baud_rate)
        self.detection_count = 0
        print("Message generator initialized successfully on separate thread!")

    def generate_message(self, results):
        # print(f"[debug] - message: {results}")
        count = 0
        if results.numel() > 0:
            print("Detected")
            self.detection_count += 1
            if self.detection_count > 100:
                print("Object detected over 100 times!")
                alert = "alert"
                self.serial_port.write(alert.encode())
                self.detection_count = 0
        else:
            print("Not detected")

    def run(self):
        while True:
            results = self.message_queue.get()
            self.generate_message(results)
