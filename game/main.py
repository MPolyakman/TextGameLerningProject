from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
from PySide6.QtCore import Qt, QSize

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("TextGame")
        self.setMinimumSize(QSize(144,144))
        self.setMaximumSize(QSize(1080, 740))
        self.resize(1080, 740)

        exitbutton = QPushButton('EXIT')
        exitbutton.setCheckable(True)
        exitbutton.setFixedSize(100,100)
        exitbutton.clicked.connect(self.close_the_game)

        self.setCentralWidget(exitbutton)



    def close_the_game(self):
        game.quit()

game = QApplication([])

window = MainWindow()
window.show()


game.exec()
print("Завершено успешно!")
