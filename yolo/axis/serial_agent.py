from dotenv import load_dotenv


class SerialAgent:
    def __init__(self, port, baudrate):
        print(f"Serial Agent initialized with the following specs: "
              f"\nCom port: {port}"
              f"\nBaudrate: {baudrate}")

