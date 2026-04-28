import sys
import time
from PyQt6.QtGui import QIcon, QPixmap, QFont
from PyQt6.QtCore import QSettings, Qt, QSize
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
    QGridLayout,
)


from functools import partial
from game import Game
from card import Card
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

        # Home page
        self.home_page = QWidget()
        self.layout1 = QStackedLayout(self.home_page)
        self.layout1.setStackingMode(QStackedLayout.StackingMode.StackAll)
        self.layout1.setContentsMargins(0,0,0,0)
        self.layout1.setSpacing(0)
        
        # Create background layer
        self.background = QWidget()
        background_layer = QVBoxLayout(self.background)

        # Create background image for the layer
        background_image = QLabel()
        file_path = QPixmap("Finn-Made-Uno/src/finn_made_uno/assets/uno_background.png")
        background_image.setPixmap(file_path)
        background_layer.setContentsMargins(0,0,0,0)
        background_layer.setSpacing(0)
        background_layer.addWidget(background_image)

        # Create menu layer
        self.menu = QWidget()
        menu_layer = QGridLayout(self.menu)
        self.menu.setStyleSheet("background: transparent; color: black;")

        # Create title for menu
        title = QLabel()
        pixmap = QPixmap("Finn-Made-Uno/src/finn_made_uno/assets/title.png") # Path to your image
        title.setPixmap(pixmap)

        # Create play button for menu
        start_button = QPushButton()
        pixmap = QPixmap("Finn-Made-Uno/src/finn_made_uno/assets/play.png")
        start_button.setIcon(QIcon(pixmap))
        start_button.setIconSize(pixmap.size())
        start_button.setStyleSheet("background-color: transparent; border: none;")
        start_button.clicked.connect(self.set_player_amount)

        # Create settings button for menu
        settings_button = QPushButton()
        pixmap = QPixmap("Finn-Made-Uno/src/finn_made_uno/assets/settings.png")
        settings_button.setIcon(QIcon(pixmap))
        settings_button.setIconSize(pixmap.size())
        settings_button.setStyleSheet("background-color: transparent; border: none;")
        settings_button.clicked.connect(self.open_settings)

        # Create a new layout for the buttons
        button_layout = QVBoxLayout()
        button_layout.addWidget(start_button)
        button_layout.addWidget(settings_button)
        button_layout.addStretch()

        # Add the menu and buttons to the gridlayout
        menu_layer.addWidget(title, 0, 2, 5, 3, alignment=Qt.AlignmentFlag.AlignCenter)
        menu_layer.addLayout(button_layout, 6, 2, 5, 3, alignment=Qt.AlignmentFlag.AlignCenter)

        # Add the pages to the layout
        self.layout1.addWidget(self.background)
        self.layout1.addWidget(self.menu)
        # Change the interactables to be in the front
        self.layout1.setCurrentIndex(1)

        # Page 2
        self.player_amount_selection = QWidget()
        self.layout2 = QStackedLayout(self.player_amount_selection)
        self.layout2.setStackingMode(QStackedLayout.StackingMode.StackAll)
        self.layout2.setContentsMargins(0,0,0,0)
        self.layout2.setSpacing(0)

        # Page 3
        self.game_page = QWidget()
        self.layout3 = QStackedLayout(self.game_page)
        self.layout3.setStackingMode(QStackedLayout.StackingMode.StackAll)
        self.layout3.setContentsMargins(0,0,0,0)
        self.layout3.setSpacing(0)

        # Add the pages to the layout
        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.player_amount_selection)
        self.stacked_widget.addWidget(self.game_page)
    
    def set_player_amount(self):

        # Change the window to be the game
        self.stacked_widget.setCurrentIndex(1)

        slider_title = QLabel("Select the amount of players:")
        slider_title.setFont(QFont("Disney Heroic", 16, QFont.Weight.Bold))

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setValue(4)
        self.slider.setMinimum(2)
        self.slider.setMaximum(6)
        self.slider.setSingleStep(1)
        self.slider.valueChanged.connect(self.handle_change)

        self.slider_btn = QPushButton()
        self.slider_btn.setText(f"Play with {self.slider.value()} players")
        self.slider_btn.setFont(QFont("Disney Heroic", 16, QFont.Weight.Bold))
        self.slider_btn.clicked.connect(self.play_game)

        self.slider_stuff = QWidget()
        self.slider_layout = QVBoxLayout(self.slider_stuff)
        self.slider_layout.addWidget(slider_title)
        self.slider_layout.addWidget(self.slider)
        self.slider_layout.addWidget(self.slider_btn)
        self.slider_layout.addStretch()

        # Create background layer
        self.slider_background = QWidget()
        background_layer = QVBoxLayout(self.slider_background)

        # Create background image for the layer
        background_image = QLabel()
        file_path = QPixmap("Finn-Made-Uno/src/finn_made_uno/assets/uno_background.png")
        background_image.setPixmap(file_path)
        background_layer.setContentsMargins(0,0,0,0)
        background_layer.setSpacing(0)
        background_layer.addWidget(background_image)

        # Add the widgets
        self.layout2.addWidget(self.slider_background)
        self.layout2.addWidget(self.slider_stuff)
        # Change the interactables to be in the front
        self.layout2.setCurrentIndex(1)

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

        # Start game loop
        """ Game Loop """
        self.game_loop(uno)
        
        """ Game Loop Ends """
        print(uno.winnerMessage())

    def game_loop(self, uno):
        """ Game Loop """
        if uno.playerHasCards():
            # Displays the turn info
            uno.displayTurnInfo() # In terminal

            self.update_options(uno)

            # Ai plays its turn if its not the players
            if uno.turn != 0:
                uno.playerTurn()
                self.game_loop(uno)

        else: 
            """ Game Loop Ends """
            self.game_win(uno)

    def update_options(self, uno):

        # Get rid of previous widgets
        self.clear_layout(self.layout3)

        # Create background layer
        self.background = QWidget()
        self.layer1 = QVBoxLayout(self.background)
        background_image = QLabel()
        file_path = QPixmap("Finn-Made-Uno/src/finn_made_uno/assets/uno_background.png")
        background_image.setPixmap(file_path)
        self.layer1.setContentsMargins(0,0,0,0)
        self.layer1.setSpacing(0)
        self.layer1.addWidget(background_image)

        # Create player info layer
        self.player_info = QWidget()
        self.layer2 = QVBoxLayout(self.player_info)
        self.player_info.setStyleSheet("background: transparent; color: black;")

        # Create card info layer
        self.card_display = QWidget()
        self.layer3 = QVBoxLayout(self.card_display)
        self.card_display.setStyleSheet("background: transparent; color: black;")

        # Displays turn info
        current_card = QLabel("Current Card:")
        self.layer2.addWidget(current_card)
        current_card_display = QLabel()
        file_path = QPixmap("Finn-Made-Uno/src/finn_made_uno/assets/cards/" + f"{str(uno.display_card)}" + ".png")
        current_card_display.setPixmap(file_path)
        self.layer2.addWidget(current_card_display)

        # Display player info
        for player in uno.players:
            current_player = str(uno.players.index(player) + 1)
            current_hand =  str(len(player.hand.cards))
            card_count = QLabel(f"Player {current_player}'s card amount: " + current_hand)
            self.layer2.addWidget(card_count)

        if uno.turn == 0:

            hand_text = QLabel("Your hand:")
            self.layer2.addWidget(hand_text)

            # Creates new buttons to select cards
            hand_layout = QHBoxLayout()
            self.buttons = []
            for card in uno.players[0].hand.cards:
                btn = QPushButton()
                file_path = "Finn-Made-Uno/src/finn_made_uno/assets/cards/" + f"{str(card)}" + ".png"
                btn.setIcon(QIcon(file_path))
                btn.setIconSize(QSize(96, 128))
                btn.setFixedSize(48, 64)
                btn.adjustSize()
                btn.setStyleSheet("background-color: transparent; border: none;")
                btn.clicked.connect(lambda checked, i = card: self.play_card(uno, i))
                self.buttons.append(btn)
                hand_layout.addWidget(btn)
            hand_layout.addStretch()
            if uno.turn != 0:
                for btn in self.buttons:
                    btn.setEnabled(False)
            self.layer3.addLayout(hand_layout)

            # Creates the draw button
            draw_btn = QPushButton()
            draw_btn.setText("Draw")
            draw_btn.adjustSize()
            draw_btn.clicked.connect(lambda checked, i = card: self.draw_card(uno))
            self.buttons.append(draw_btn)
            self.layer3.addWidget(draw_btn)

        self.layer2.addStretch()

        # Add the pages to the layout
        self.layout3.addWidget(self.background)
        self.layout3.addWidget(self.player_info)
        self.layout3.addWidget(self.card_display)
        # Change the interactables to be in the front
        self.layout3.setCurrentIndex(1)
        self.layout3.setCurrentIndex(2)

    def draw_card(self, uno):
        check = uno.players[0].drawCard(uno)
        if check: self.game_loop(uno)

    def play_card(self, uno, card):
        check = uno.players[0].playCard(uno, card)
        if card.color == "wild":
            self.create_wild_buttons(uno)
        if check: self.game_loop(uno)

    def create_wild_buttons(self, uno):
        for btn in self.buttons:
            btn.setEnabled(False)
        current_card = QLabel("What color do you want?:")
        self.layout3.addWidget(current_card)
        self.color_buttons = []
        for color in Card.color[:-1]:
            btn = QPushButton()
            btn.setText(str(color))
            btn.clicked.connect(lambda checked, i = color: self.choose_color(uno, i))
            self.color_buttons.append(btn)
            self.layout3.addWidget(btn)

    def choose_color(self, uno, color):
        uno.display_card.color = color
        uno.display_card.number = "<any>"
        print(f"\n===== Color has been changed to {uno.display_card.color}! =====")
        uno.nextTurn()
        for btn in self.color_buttons:
            btn.deleteLater()
        self.game_loop(uno)

    def game_win(self, uno):
        """ Game Loop Ends """
        print(uno.winnerMessage())
        self.stacked_widget.setCurrentIndex(0)
        self.clear_layout(self.layout2)
        self.clear_layout(self.layout3)
        del uno
    
    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    # Remove the widget and schedule it for deletion
                    widget.deleteLater()
                else:
                    # If the item is another layout, clear it recursively
                    self.clear_layout(item.layout())


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
