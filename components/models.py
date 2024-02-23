from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import json

class ModelsFrame(QFrame):
    def __init__(self):
        super().__init__()

        # Set tab style
        # frame = QFrame()
        self.setStyleSheet("background-color: #464545; border-radius: 20;")
        mainhbox = QHBoxLayout()

        chatFrame = QFrame()
        chatFrame.setStyleSheet("background-color: #5E5E5E; border-radius: 20;")
        chatVBox = QVBoxLayout()
        chatFrame.setLayout(chatVBox)

        agentsTasksFrame = QFrame()
        agentsTasksFrame.setStyleSheet("background-color: #5E5E5E; border-radius: 20;")
        agentsTasksVBox = QVBoxLayout()
        agentsTasksFrame.setLayout(agentsTasksVBox)

        mainhbox.addWidget(chatFrame)
        mainhbox.addWidget(agentsTasksFrame)
        self.setLayout(mainhbox)

    def modelBox(self, lis