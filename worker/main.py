from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from serial_parameters_app import SerialParametersApp
import sys

app = QApplication(sys.argv)
app.setStyleSheet("""
    QWidget { 
        background-color: #202020;  
        color: #ffffff; 
    } 
    QPushButton, QComboBox { 
        background-color: #0066CC; 
        font-size: 20px;
    }
    QTextEdit {
        background-color: #000000;
        color: #00FF00;
        font-size: 20px;
    }
""")
app.setWindowIcon(QIcon('../utils/images/antenna.png'))

window = SerialParametersApp()
window.show()

sys.exit(app.exec_())
