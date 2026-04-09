import sys
from PyQt6.QtGui import QIcon, QPixmap, QPainter
from PyQt6.QtCore import QSettings, Qt
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
    QSlider,
)


from functools import partial
from game import Game
import threading


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = SettingsWindow()
        
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
        start_button.clicked.connect(self.setPlayerAmount)
        self.layout1.addWidget(start_button)

        # Create settings button
        settings_button = QPushButton()
        settings_button.setIcon(QIcon('Finn-Made-Uno/src/finn_made_uno/assets/settings.png'))
        settings_button.setFixedSize(32, 32)
        settings_button.clicked.connect(self.open_settings)
        self.layout1.addWidget(settings_button)
        
        self.home_page.setLayout(self.layout1)

        # Page 2
        self.player_amount_selection = QWidget()
        self.layout2 = QVBoxLayout(self.player_amount_selection)

        # Page 3
        self.game_page = QWidget()
        self.layout3 = QVBoxLayout(self.game_page)

        # Add the pages to the layout
        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.player_amount_selection)
        self.stacked_widget.addWidget(self.game_page)
    
    def setPlayerAmount(self):

        # Change the window to be the game
        self.stacked_widget.setCurrentIndex(1)

        slider_title = QLabel("Select the amount of players:")
        self.layout2.addWidget(slider_title)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(2)
        self.slider.setMaximum(6)
        self.slider.setSingleStep(1)
        self.slider.valueChanged.connect(self.handle_change)
        self.layout2.addWidget(self.slider)

        self.slider_btn = QPushButton()
        self.slider_btn.setText(f"Play with {self.slider.value()} players")
        self.slider_btn.clicked.connect(self.play_game)
        self.layout2.addWidget(self.slider_btn)
        self.layout2.addStretch()

    def handle_change(self):
        print(f"Slider moved to: {self.slider.value()}")
        self.slider_btn.setText(f"Play with {self.slider.value()} players")

    def play_game(self):
        # Change the window to be the game
        self.stacked_widget.setCurrentIndex(2)
        
        # Setup the game
        """ Game Setup """
        uno = Game()
        uno.player_amount = self.slider.value() - 1
        uno.addPlayers()
            
        """ Settings """
        place, draw, stack = self.settings.settings_buttons
        uno.place_after_draw = place.isChecked()
        uno.draw_till_place = draw.isChecked()
        uno.stack_plus_cards = stack.isChecked()

        # Displays player info
        self.current_card = QLabel(str(uno.display_card))
        self.layout3.addWidget(self.current_card)

        # Start game loop
        """ Game Loop """
        self.game_loop(uno)
        
        """ Game Loop Ends """
        print(uno.winnerMessage())

    def game_loop(self, uno):
        """ Game Loop """
        if uno.playerHasCards():
            # Displays the turn info
            self.current_card.setText(f"Current Card: " + str(uno.display_card))
            uno.displayTurnInfo() # In terminal

            self.update_options(uno)

            # Ai plays its turn if its not the players
            if uno.turn != 0:
                uno.playerTurn()
                self.game_loop(uno)

        else: 
            """ Game Loop Ends """
            print(uno.winnerMessage())

    def update_options(self, uno):
        #Creates buttons to select cards
        for card in uno.players[0].hand.cards:
            btn = QPushButton()
            btn.setText(str(card))
            btn.adjustSize()
            btn.clicked.connect(lambda checked, i = card: self.play_card(uno, i))
            self.layout3.addWidget(btn)

        # Creates the draw button
        draw_btn = QPushButton()
        draw_btn.setText("Draw")
        draw_btn.adjustSize()
        draw_btn.clicked.connect(lambda checked, i = card: self.draw_card(uno))
        self.layout3.addWidget(draw_btn)

    def draw_card(self, uno):
        check = uno.players[0].drawCard(uno)
        if check: self.game_loop(uno)

    def play_card(self, uno, card):
        check = uno.players[0].playCard(uno, card)
        if check: self.game_loop(uno)

    def open_settings(self):
        """Slot to handle the button click and open the settings dialog."""
        # self.settings_window = SettingsWindow(self)
        # Use exec() to run the dialog modally (blocks input to other windows)
        if self.settings.exec() == QDialog.DialogCode.Accepted:
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
