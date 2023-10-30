import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import folium
import io
import base64


class MapWidget(QWidget):
    def __init__(self, positions):
        super().__init__()
        self.webEngineView = None
        self.initUI(positions)

    def initUI(self, positions):
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Map')

        # Create folium map
        m = folium.Map(location=[positions[0][0], positions[0][1]], zoom_start=15)

        # Add a marker for each position
        for position in positions:
            folium.Marker([position[0], position[1]]).add_to(m)

        # Save it to tmp file and re-open file as base64
        data = io.BytesIO()
        m.save(data, close_file=False)
        data.seek(0)
        html = data.read()

        # Set Map to QWebEngineView
        self.webEngineView = QWebEngineView(self)
        self.webEngineView.setHtml(html.decode())
        self.webEngineView.setGeometry(50, 50, 700, 500)
        self.show()


def main():
    app = QApplication(sys.argv)

    # Set your GPS coordinates here
    positions = [[44.4268, 26.1025], [44.4278, 26.1035], [44.4288, 26.1045]]

    ex = MapWidget(positions)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

