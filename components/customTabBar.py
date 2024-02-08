import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


class CustomTabBar(QTabBar):
    def __init__(self):
        super().__init__()
        
    def tabSizeHint(self, index):
        size = super().tabSizeHint(index)  # Get the default size
        size.setWidth(100)  # Set the width to 150 pixels (or any value you prefer)
        size.setHeight(100)
        return size
    
    def paintEvent(self, event):
        painter = QPainter(self)
        option = QTextOption()
        option.setAlignment(Qt.AlignmentFlag.AlignCenter)

        font = QFont()
        font.setBold(True)
        painter.setFont(font)

        for index in range(self.count()):
            tab_rect = self.tabRect(index)
            tab_text = self.tabText(index)

            if index == self.currentIndex():
                painter.setBrush(QBrush(QColor('#5E5E5E')))  # Active tab color
                
            else:
                painter.setBrush(QBrush(QColor('#464545')))  # Inactive tab color

            painter.setPen(Qt.PenStyle.NoPen)  # No border
            painter.drawRect(tab_rect)

            # Set the pen for the text
            if index == self.currentIndex():
                painter.setPen(QColor('#75DBE9'))  # Active tab text color
            else:
                painter.setPen(QColor('white'))  # Inactive tab text color

            painter.save()

            # Calculate the position to draw the text.
            painter.translate(tab_rect.left(), tab_rect.top() + tab_rect.height() / 2)

            # Create a QRectF for the text, positioned at the center of the tab vertically
            text_rect = QRectF(0, -tab_rect.width() / 2, tab_rect.height(), tab_rect.width())

            # Draw the text using the text rectangle
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, tab_text)

            painter.restore()
