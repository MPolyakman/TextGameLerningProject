from PySide6.QtCore import Qt, QSize, QLineF, QPointF
from PySide6.QtWidgets import  (QWidget, QPushButton, QMainWindow, QVBoxLayout,  QHBoxLayout, QLabel,
    QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsLineItem, QGraphicsSimpleTextItem)
from PySide6.QtGui import QPen, QBrush, QColor, QPainter
from collections import deque
from game.map import*

class RoomBox(QGraphicsRectItem):
    def __init__(self, room, is_current=False):
        super().__init__(0, 0, 100, 80)
        self.room = room
        self.setPos(room.x * 150, room.y * 150)  # Масштабирование позиции
        
        # Стиль комнаты
        if is_current:
            self.setBrush(QBrush(QColor(144, 238, 144)))  # Светло-зеленый для текущей
        else:
            self.setBrush(QBrush(QColor(240, 240, 240)))  # Серый для остальных
            
        # Отображение названия комнаты
        text = QGraphicsSimpleTextItem(room.name, self)
        text.setPos(10, 30)

class PathBox(QGraphicsLineItem):
    def __init__(self, start, end, has_door):
        super().__init__()
        self.setLine(QLineF(start, end))
        
        

class MapView(QGraphicsView):
    def __init__(self, graph, current_room):
        super().__init__()
        self.graph = graph
        self.current_room = current_room
        self.scene = QGraphicsScene


