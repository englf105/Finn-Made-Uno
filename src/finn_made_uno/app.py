import sys
from PyQt6.QtGui import QIcon

from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QGridLayout,
    QDialog,
    QCheckBox,
)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Window setup
        self.setWindowTitle("Finn Made Uno")
        self.setWindowIcon(QIcon('Finn-Made-Uno/src/finn_made_uno/assets/uno_icon_32.png'))
        self.setGeometry(800, 600, 800, 600)
        
        # Create layout
        layout = QGridLayout()
        self.setLayout(layout)

        # Create header
        self.title = QLabel("Finn Made Uno")

        # Create settings button
        self.settings_button = QPushButton()
        self.settings_button.setIcon(QIcon('Finn-Made-Uno/src/finn_made_uno/assets/settings.png'))
        self.settings_button.move(750, 650)
        self.settings_button.setFixedSize(32, 32)
        self.settings_button.clicked.connect(self.open_settings)

        # Add widgets
        layout.addWidget(self.title, 2, 2)
        layout.addWidget(self.settings_button, 4, 4)
    
    def open_settings(self):
        """Slot to handle the button click and open the settings dialog."""
        dlg = SettingsDialog(self)
        # Use exec() to run the dialog modally (blocks input to other windows)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            print("Settings saved/accepted")
        else:
            print("Settings canceled/closed")

class SettingsDialog(QDialog):
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
