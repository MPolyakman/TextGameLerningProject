from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QVBoxLayout
from PySide6.QtCore import Qt, QSize

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("TextGame")
        self.setMinimumSize(QSize(144,144))
        self.setMaximumSize(QSize(1080, 740))
        self.resize(1080, 740)
        
        # кнопка выхода
        exitbutton = QPushButton('EXIT')
        exitbutton.setCheckable(True)
        exitbutton.setFixedSize(100,100)
        exitbutton.clicked.connect(self.close_the_game)

        # кнопка игрулькать
        newgame_button = QPushButton('New Gay')
        newgame_button.setCheckable(True)
        newgame_button.setFixedSize(100,100)
        # newgame_button.clicked.connect(self.close_the_game)

        # self.setCentralWidget(exitbutton)

        #менюха
        main_menu_bar = QWidget()
        self.setCentralWidget(main_menu_bar)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(30)

        layout.addWidget(newgame_button)
        layout.addWidget(exitbutton)

        main_menu_bar.setLayout(layout)


    def close_the_game(self):
        game.quit()

game = QApplication([])

window = MainWindow()
window.show()


game.exec()
print("Завершено успешно!")