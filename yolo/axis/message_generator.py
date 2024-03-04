# message_generator.py
import queue
import threading


class MessageGenerator:
    def __init__(self):
        self.message_queue = queue.Queue()

    def generate_message(self, results):
        # TODO: Implement message generation based on results
        print(f"message: {results}")

    def run(self):
        while True:
            results = self.message_queue.get()
            self.generate_message(results)
