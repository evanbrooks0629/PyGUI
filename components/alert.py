from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

class Alert(QDialog):
    def __init__(self, type, message, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet("""
            background-color: transparent;
            border-radius: 5px;
        """) 
        self.resize(250, 50)
        self.type = type
        self.message = message
        self.color = '#ffffff'

        if self.type == 'ERROR':
            self.color = '#E42323'
        elif self.type == 'SUCCESS':
            self.color = '#24C935'
        # self.setGeometry(((QGuiApplication.primaryScreen().size().width()//2) - 150), ((QGuiApplication.primaryScreen().size().height()//2) - 75), 300, 150)
        mainlayout = QHBoxLayout()
        frame = QFrame()
        frame.setStyleSheet("""
            background-color: #464545;
            border-radius: 5px;
        """)
        mainlayout.addWidget(frame)

        layout = QHBoxLayout()
        label = QLabel(message)
        label.setStyleSheet(f"color: {self.color};")
        layout.addWidget(label)

        self.closeButton = QPushButton("Close", self)
        self.closeButton.setStyleSheet("""
            border: 0px;
            background-color: #464545;
        """)
        self.closeButton.clicked.connect(self.close)
        layout.addWidget(self.closeButton)

        # Set the layout for the dialog
        frame.setLayout(layout)
        self.setLayout(mainlayout)

        self.closeTimer = QTimer(self)
        self.closeTimer.timeout.connect(self.close)
        self.closeTimer.start(1000)
