import sys
from PyQt6.QtGui import QIcon, QPixmap, QPainter

from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QDialog,
    QCheckBox,
    QMainWindow,
    QStackedWidget,
    QStackedLayout,
    QHBoxLayout,
    QButtonGroup,
)


from functools import partial
from game import Game


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Central Layout
        self.setWindowTitle("Finn Made Uno")
        self.setWindowIcon(QIcon('Finn-Made-Uno/src/finn_made_uno/assets/uno_icon_32.png'))
        self.setGeometry(800, 600, 800, 600)
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Page 1
        self.home_page = QWidget()
        layout1 = QHBoxLayout(self.home_page)

        # Create title
        layout1.addWidget(QLabel("Finn Made Uno"))

        # Create play button
        start_button = QPushButton()
        start_button.setText("Play")
        start_button.setFixedSize(64, 32)
        start_button.clicked.connect(self.play_game)
        layout1.addWidget(start_button)

        # Create settings button
        settings_button = QPushButton()
        settings_button.setIcon(QIcon('Finn-Made-Uno/src/finn_made_uno/assets/settings.png'))
        settings_button.setFixedSize(32, 32)
        settings_button.clicked.connect(self.open_settings)
        layout1.addWidget(settings_button)
        
        self.home_page.setLayout(layout1)

        # Page 2
        self.game_page = QWidget()
        layout2 = QStackedLayout(self.game_page)

        # Add the pages to the layout
        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.game_page)

    def play_game(self):
        # Change the window to be the game
        self.stacked_widget.setCurrentIndex(1)
        
        # Setup the game
        """ Game Setup """
        uno = Game()

        """ Settings """
        uno.place_after_draw = SettingsWindow.after_draw_cbox.isChecked() # Working
        uno.draw_till_place = SettingsWindow.til_place_cbox.isChecked() # Working
        uno.stack_plus_cards = SettingsWindow.stack_plus_cbox.isChecked() # Working

        # Start game loop
        """ Game Loop """
        while uno.playerHasCards():
            uno.displayTurnInfo()
            uno.playerTurn()
            uno.nextTurn()
        
        """ Game Loop Ends """
        print(uno.winnerMessage())

    def open_settings(self):
        """Slot to handle the button click and open the settings dialog."""
        dlg = SettingsWindow(self)
        # Use exec() to run the dialog modally (blocks input to other windows)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            print("Settings saved/accepted")
        else:
            print("Settings canceled/closed")
        

class SettingsWindow(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        layout = QVBoxLayout()
        # Add settings widgets here
        layout.addWidget(QLabel("Select Settings:"))
        
        self.settings_buttons = []
        for text in ("Place after drawing", 
                     "Draw until place", 
                     "Stack plus cards"):
            checkbox = QCheckBox(text)
            checkbox.clicked.connect(partial(self.check_settings, text))
            #checkbox.toggle()
            layout.addWidget(checkbox)
            self.settings_buttons.append(checkbox)


        layout.addStretch()
        self.setLayout(layout)

    def check_settings(self, text): 
        place,draw,stack = self.settings_buttons
        if draw.isChecked() and place.isChecked():
            if "Place" in text:
                draw.toggle()
            else:
                place.toggle()


        for button in self.settings_buttons:
            print(f"Checkbox = {button.isChecked()}")
    


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
