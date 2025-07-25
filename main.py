from PySide6.QtWidgets import QApplication, QWidget, QPushButton
from ui import GameUI

import sys

app = QApplication(sys.argv)
window = QWidget()
window.show()
button = QPushButton("Press if you are LOH")
button.setCheckable(True)

button.show()
app.exec()