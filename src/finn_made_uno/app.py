import sys
from PyQt6.QtGui import QIcon, QPixmap, QPainter

from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QGridLayout,
    QDialog,
    QCheckBox,
    QMainWindow,
    QStackedWidget,
)


from uno import Uno


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Central Layout
        self.setWindowTitle("Finn Made Uno")
        self.setWindowIcon(QIcon('Finn-Made-Uno/src/finn_made_uno/assets/uno_icon_32.png'))
        self.setGeometry(800, 600, 800, 600)
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        self.stacked_widget = QStackedWidget()

        # Page 1
        page1 = QWidget()
        layout1 = QGridLayout(page1)
        # Create title
        self.title = QLabel("Finn Made Uno")
        # Create play button
        self.start_button = QPushButton()
        self.start_button.setText("Play")
        self.start_button.move(750, 650)
        self.start_button.clicked.connect(self.start_game)
        # Create settings button
        self.settings_button = QPushButton()
        self.settings_button.setIcon(QIcon('Finn-Made-Uno/src/finn_made_uno/assets/settings.png'))
        self.settings_button.move(750, 650)
        self.settings_button.setFixedSize(32, 32)
        self.settings_button.clicked.connect(self.open_settings)
        # Add widgets
        layout1.addWidget(self.title)
        layout1.addWidget(self.start_button)
        layout1.addWidget(self.settings_button)

        self.stacked_widget.addWidget(page1)
        self.stacked_widget.addWidget(page2)

    def start_game(self):
        uno = Uno()

    def open_settings(self):
        """Slot to handle the button click and open the settings dialog."""
        dlg = SettingsWindow(self)
        # Use exec() to run the dialog modally (blocks input to other windows)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            print("Settings saved/accepted")
        else:
            print("Settings canceled/closed")

class GameWindow(QWidget):
    def __init__(self):
        # Window setup
        self.setWindowTitle("Finn Made Uno")
        self.setWindowIcon(QIcon('Finn-Made-Uno/src/finn_made_uno/assets/uno_icon_32.png'))
        self.setGeometry(800, 600, 800, 600)

        # Create layout
        layout = QGridLayout()
        self.setLayout(layout)
        
class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        layout = QVBoxLayout()
        # Add settings widgets here
        layout.addWidget(QLabel("Select Settings:"))
        layout.addWidget(QCheckBox("Place after drawing"))
        layout.addWidget(QCheckBox("Draw until place"))
        layout.addWidget(QCheckBox("Stack plus cards"))
        layout.addStretch()
        self.setLayout(layout)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
