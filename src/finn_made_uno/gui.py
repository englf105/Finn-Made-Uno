import sys
from PyQt6.QtGui import QFont, QFontDatabase, QIcon

from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QFormLayout,
    QLabel,
    QDoubleSpinBox,
    QSpinBox,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
    QMainWindow,
)

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Finn Made Uno")
        self.setWindowIcon(QIcon('Finn-Made-Uno/src/finn_made_uno/assets/uno_icon_32.png'))
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
