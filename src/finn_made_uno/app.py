import sys
from PyQt6.QtGui import QIcon, QPixmap, QPainter
from PyQt6.QtCore import QSettings
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
        self.layout1 = QHBoxLayout(self.home_page)

        # Create title
        self.layout1.addWidget(QLabel("Finn Made Uno"))

        # Create play button
        start_button = QPushButton()
        start_button.setText("Play")
        start_button.setFixedSize(64, 32)
        start_button.clicked.connect(self.play_game)
        self.layout1.addWidget(start_button)

        # Create settings button
        settings_button = QPushButton()
        settings_button.setIcon(QIcon('Finn-Made-Uno/src/finn_made_uno/assets/settings.png'))
        settings_button.setFixedSize(32, 32)
        settings_button.clicked.connect(self.open_settings)
        self.layout1.addWidget(settings_button)
        
        self.home_page.setLayout(self.layout1)

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
        place,draw,stack = SettingsWindow.settings_buttons
        uno.place_after_draw = place.isChecked()
        uno.draw_till_place = draw.isChecked()
        uno.stack_plus_cards = stack.isChecked()



        # Start game loop
        """ Game Loop """
        while uno.playerHasCards():

            # Displays the turn info
            uno.displayTurnInfo() # In terminal
            cards = QLabel()
            cards = uno.players[0].hand.cards


            # Lets the player/robot either play their card or draw
            uno.playerTurn()

            # Goes to the next turn
            uno.nextTurn()
        
        """ Game Loop Ends """
        print(uno.winnerMessage())

    def open_settings(self):
        """Slot to handle the button click and open the settings dialog."""
        settings_window = SettingsWindow(self)
        # Use exec() to run the dialog modally (blocks input to other windows)
        if settings_window.exec() == QDialog.DialogCode.Accepted:
            print("Settings saved/accepted")
        else:
            print("Settings canceled/closed")
        

class SettingsWindow(QDialog):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.settings = QSettings('Finn-Made-Uno', 'Settings')

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
            layout.addWidget(checkbox)
            self.settings_buttons.append(checkbox)
        layout.addStretch()
        self.setLayout(layout)

        self.load_settings()

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.accept) 
        layout.addWidget(self.save_button)


    def check_settings(self, text): 
        place,draw,stack = self.settings_buttons
        if draw.isChecked() and place.isChecked():
            if "Place" in text:
                draw.toggle()
            else:
                place.toggle()

    def load_settings(self):
        place,draw,stack = self.settings_buttons
        place = self.settings.value('check1', place.setChecked(False))
        draw = self.settings.value('check2', draw.setChecked(False))
        stack = self.settings.value('check3', stack.setChecked(False))
        print("Settings loaded.")

    def save_settings(self):
        place,draw,stack = self.settings_buttons
        self.settings.setValue('check1', place.isChecked())
        self.settings.setValue('check2', draw.isChecked())
        self.settings.setValue('check3', stack.isChecked())
        print("Settings saved.")
        print(self.settings.value('check1'))

    def closeEvent(self, event):
        self.save_settings()
        super().closeEvent(event)
    


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
