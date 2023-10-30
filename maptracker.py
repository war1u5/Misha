import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import folium
import io
import base64


class MapWidget(QWidget):
    def __init__(self, latitude, longitude):
        super().__init__()
        self.webEngineView = None
        self.initUI(latitude, longitude)

    def initUI(self, latitude, longitude):
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Map')

        # Create folium map
        m = folium.Map(location=[latitude, longitude], zoom_start=15)
        folium.Marker([latitude, longitude]).add_to(m)

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
    latitude = 44.4268
    longitude = 26.1025

    ex = MapWidget(latitude, longitude)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
