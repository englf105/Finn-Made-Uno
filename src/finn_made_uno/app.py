import sys
import time
from PyQt6.QtGui import QIcon, QPixmap, QFont, QTransform
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
        self.setFixedSize(800, 600)
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Page 1
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
        self.slider.setFixedHeight(40)
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #ffea63;
                height: 10px;
                background: #ffea63;
                border-radius: 0px;
            }

            QSlider::handle:horizontal {
                image: url(Finn-Made-Uno/src/finn_made_uno/assets/slider_button.png); /* Set the handle image here */
                width: 32px;  /* Match handle width to your image */
                height: 32px; /* Match handle height to your image */
                margin: -16px 0; /* Use negative margin to make handle larger than groove */
            }
        """)
        self.slider.setFixedWidth(400)
        self.slider.setValue(4)
        self.slider.setMinimum(2)
        self.slider.setMaximum(6)
        self.slider.setSingleStep(1)
        self.slider.valueChanged.connect(self.handle_change)

        self.slider_btn = QPushButton()
        self.slider_btn.setStyleSheet("background-color: #ffea63; color: #0d171f; border-radius: 0px; padding: 16px;")
        self.slider_btn.setText(f"Play with {self.slider.value()} players")
        self.slider_btn.setFont(QFont("Disney Heroic", 16, QFont.Weight.Bold))
        self.slider_btn.clicked.connect(self.play_game)

        self.slider_stuff = QWidget()
        self.slider_layout = QVBoxLayout(self.slider_stuff)
        self.slider_layout.addStretch()
        self.slider_layout.addWidget(slider_title, alignment=Qt.AlignmentFlag.AlignCenter)
        self.slider_layout.addWidget(self.slider, alignment=Qt.AlignmentFlag.AlignCenter)
        self.slider_layout.addWidget(self.slider_btn, alignment=Qt.AlignmentFlag.AlignCenter)
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

        # Background Layer
        # /////////////////////////////////////////////////////////////////////
        self.background = QWidget()
        self.layer1 = QVBoxLayout(self.background)
        background_image = QLabel()
        file_path = "Finn-Made-Uno/src/finn_made_uno/assets/uno_background.png"
        background_image.setPixmap(QPixmap(file_path))
        self.layer1.setContentsMargins(0,0,0,0)
        self.layer1.setSpacing(0)
        self.layer1.addWidget(background_image)

        # Player options layer
        #//////////////////////////////////////////////////////////////////////

        # Create a QLabel that shows the current card
        current_card_display = QLabel()
        file_path = "Finn-Made-Uno/src/finn_made_uno/assets/cards/"
        file_path += f"{str(uno.display_card)}" + ".png"
        pixmap = QPixmap(file_path)
        pixmap = self.upscale_pixmap(pixmap, 2)
        current_card_display.setPixmap(QPixmap(pixmap))

        # Create a list of all the buttons
        self.buttons = []

        # Creates the draw button
        draw_btn = QPushButton()
        file_path = "Finn-Made-Uno/src/finn_made_uno/assets/cards/card_back.png"
        pixmap = QPixmap(file_path)
        pixmap = self.upscale_pixmap(pixmap, 2)
        draw_btn.setIcon(QIcon(pixmap))
        draw_btn.setIconSize(pixmap.size())
        draw_btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    padding: 1px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: white;
                    padding: 10px;
                    border: none;
                }
            """)
        draw_btn.clicked.connect(lambda checked: self.draw_card(uno))
        self.buttons.append(draw_btn)

        # Creates new buttons to select cards
        for card in uno.players[0].hand.cards:
            btn = QPushButton()
            file_path = "Finn-Made-Uno/src/finn_made_uno/assets/cards/"
            file_path += str(card) + ".png"
            pixmap = QPixmap(file_path)
            pixmap = self.upscale_pixmap(pixmap, 2)
            btn.setIcon(QIcon(pixmap))
            btn.setIconSize(pixmap.size())
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    padding: 1px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: white;
                    padding: 10px;
                    border: none;
                }
            """)
            btn.clicked.connect(lambda checked, i = card: self.play_card(uno, i))
            if uno.turn != 0: btn.setEnabled(False)
            self.buttons.append(btn)

        # Add the middle widgets to a layout with stretches
        middle_cards = QHBoxLayout()
        middle_cards.addStretch()
        middle_cards.addWidget(current_card_display, alignment=Qt.AlignmentFlag.AlignCenter)
        middle_cards.addWidget(draw_btn)
        middle_cards.addStretch()

        # Add card buttons to layout with stretches
        hand_layout = QHBoxLayout()
        hand_layout.addStretch()
        for btn in self.buttons[1:]:
            hand_layout.addWidget(btn)
        hand_layout.addStretch()
        
        # Create layer2 and add layouts & stretches
        self.card_display = QWidget()
        self.layer2 = QVBoxLayout(self.card_display)
        self.card_display.setStyleSheet("background: transparent;")
        self.layer2.setContentsMargins(40, 40, 40, 40)
        self.layer2.addStretch()
        self.layer2.addLayout(middle_cards)
        self.layer2.addStretch()
        self.layer2.addLayout(hand_layout)

        # General Info layer
        # /////////////////////////////////////////////////////////////////////

        # Create the general info layer
        self.general_info = QWidget()
        self.layer3 = QVBoxLayout(self.general_info)
        self.general_info.setStyleSheet("background: transparent;")
        self.layer3.setContentsMargins(40, 40, 40, 40)

        # Display player info
        for player in uno.players[1:]:
            
            player_cards = QHBoxLayout()

            # Container for the cards
            cards_widget = QWidget()
            cards_widget.setStyleSheet("background-color: transparent;")
            
            # Use QStackedLayout to overlay
            self.stack_layout = QStackedLayout()
            self.stack_layout.setStackingMode(QStackedLayout.StackingMode.StackAll)
            cards_widget.setLayout(self.stack_layout)

            for i, card in enumerate(player.hand.cards):
                card = QLabel()

                file_path = "Finn-Made-Uno/src/finn_made_uno/assets/cards/card_back.png"
                pixmap = QPixmap(file_path)
                pixmap = self.upscale_pixmap(pixmap, 2)
                card.setPixmap(pixmap)


                card.setStyleSheet("""QLabel {background-color: transparent;}""")
                card.setContentsMargins((i+1)*20, 0, 0, 0)

                self.stack_layout.addWidget(card)

            # Number that tells user how many cards this player has
            card_amount = QLabel()
            card_amount.setText(str(len(player.hand.cards)))
            card_amount.setFont(QFont("Disney Heroic", 16, QFont.Weight.Bold))
            card_amount.setFixedHeight(30) 
            card_amount.setStyleSheet("""
                QLabel {
                    background: #ffea63;
                    border-radius: 5px;
                    padding: 0px 1px 0px 1px;           
                }
            """)

            
            player_cards.addWidget(card_amount)
            player_cards.addWidget(cards_widget)
            player_cards.addStretch()
            self.layer3.addLayout(player_cards)

        self.layer3.addStretch()


        # Add Layers to Layout3
        # //////////////////////////////////////////////////////////////////////////
        self.layout3.addWidget(self.background)
        self.layout3.addWidget(self.general_info)
        self.layout3.addWidget(self.card_display)
        # Change the interactables to be in the front
        self.layout3.setCurrentIndex(1)
        self.layout3.setCurrentIndex(2)

    def upscale_pixmap(self, pixmap, upscale_int):
        new_width = pixmap.width() * upscale_int
        new_height = pixmap.height() * upscale_int
        scaled_pixmap = pixmap.scaled(
            new_width, 
            new_height, 
            Qt.AspectRatioMode.KeepAspectRatio, 
            Qt.TransformationMode.FastTransformation
        )
        return scaled_pixmap

    def draw_card(self, uno):
        check = uno.players[0].drawCard(uno)
        if check: self.game_loop(uno)

    def play_card(self, uno, card):
        check = uno.players[0].playCard(uno, card)
        if card.color == "wild":
            self.create_wild_buttons(uno)
        if check: self.game_loop(uno)

    def create_wild_buttons(self, uno):
        # Create the wild layer
        # //////////////////////////////////////////////////////////////////////////
        self.wild_layer = QWidget()
        self.layer4 = QVBoxLayout(self.wild_layer)
        self.wild_layer.setStyleSheet("background: transparent; color: black;")
        self.layer4.addStretch()
        self.layer4.addStretch()

        # Set label instruction
        current_card = QLabel("Choose color:")
        current_card.setFont(QFont("Disney Heroic", 16, QFont.Weight.Bold))
        self.layer4.addWidget(current_card, alignment=Qt.AlignmentFlag.AlignCenter)
        

        # Create the buttons for choosing your color
        color_layout = QHBoxLayout()
        color_layout.addStretch()
        self.color_buttons = []
        for color in Card.color[:-1]:
            btn = QPushButton()
            file_path = "Finn-Made-Uno/src/finn_made_uno/assets/wild/" + color + "_change.png"
            pixmap = QPixmap(file_path)
            pixmap = self.upscale_pixmap(pixmap, 2)
            btn.setIcon(QIcon(pixmap))
            btn.setIconSize(pixmap.size())
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    padding: 1px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: white;
                    padding: 10px;
                    border: none;
                }
            """)
            btn.clicked.connect(lambda checked, i = color: self.choose_color(uno, i))
            self.color_buttons.append(btn)
            color_layout.addWidget(btn)
        color_layout.addStretch()
        self.layer4.addLayout(color_layout)
        self.layer4.addStretch()

        # Add the wild layer to the main layer
        self.layout3.addWidget(self.wild_layer)
        self.layout3.setCurrentIndex(3)

    def choose_color(self, uno, color):
        uno.display_card.color = color
        uno.display_card.number = "any"
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
