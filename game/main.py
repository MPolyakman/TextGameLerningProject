from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtCore import Qt, QSize

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("TextGame")
        self.setMinimumSize(QSize(144,144))
        self.setMaximumSize(QSize(1080, 740))
        self.resize(1080, 740)

        self.show_main_menu()

    def show_main_menu(self):
        main_menu = MainMenuWidget(self)
        self.setCentralWidget(main_menu)

    def open_the_menu(self):
        main_menu_bar = MainMenuWidget(self)
        self.setCentralWidget(main_menu_bar)
        
    def close_the_game(self):
        game.quit()

    def start_the_game(self):
        game = GameWidget(self)
        self.setCentralWidget(game)

class MainMenuWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        # кнопка выхода
        self.exit_button = QPushButton('EXIT')
        self.exit_button.setCheckable(True)
        self.exit_button.setFixedSize(100,100)
        self.exit_button.clicked.connect(self.main_window.close_the_game)

        # кнопка игрулькать
        self.newgame_button = QPushButton('New Game')
        self.newgame_button.setCheckable(True)
        self.newgame_button.setFixedSize(100,100)
        self.newgame_button.clicked.connect(self.main_window.start_the_game)



        #менюхаf

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(30)

        layout.addWidget(self.newgame_button)
        layout.addWidget(self.exit_button)


class GameWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        #кнопка меню виджет
        interface_layout = QVBoxLayout(self)

        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignmentFlag.AlignLeft |Qt.AlignmentFlag.AlignTop)

        self.menu_button = QPushButton("Menu")
        self.menu_button.setCheckable(True)
        self.menu_button.clicked.connect(self.main_window.open_the_menu)
        top_layout.addWidget(self.menu_button)

        #игровой текст виджет
        text_layout = QVBoxLayout()
        text_layout.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignVCenter)

        self.text = QLabel("*ИГРА")
        text_layout.addWidget(self.text)

        interface_layout.addLayout(top_layout)
        interface_layout.addLayout(text_layout)




game = QApplication([])

window = MainWindow()
window.show()


game.exec()
print("Завершено успешно!")
