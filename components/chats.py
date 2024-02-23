from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from components.agents import AgentsFrame
import json

class ChatsFrame(QFrame):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            background-color: #464545; 
            border-radius: 20;
        """)
        mainhbox = QHBoxLayout()

        chatFrame = QFrame()
        chatFrame.setStyleSheet("""
            background-color: #5E5E5E; 
            border-radius: 20;
        """)
        # chatHBox = QHBoxLayout()
        ## GET ALL CHATS

        chatVBox = QVBoxLayout()

        ### ADD CONTENT TO CHATVBOX HERE ###

        chatBox = QLabel("Welcome to TaskForceAI. Type the task you’d like our engineering team to complete, and we’ll make sure everything is done perfectly! To get started, just type below.")
        chatBox.setStyleSheet("""
            background-color: #464545; 
            border-radius: 20;
            padding: 20;
        """)
        chatBox.setFixedHeight(200)
        chatBox.setWordWrap(True)

        textBox = QPlainTextEdit()
        textBox.setStyleSheet("""
            background-color: #464545;
            color: #ffffff;
            padding: 20;
        """)
        textBox.setPlaceholderText("Type anything...")

        chatVBox.addWidget(chatBox)
        chatVBox.addWidget(textBox)

        chatFrame.setLayout(chatVBox)

        mainhbox.addWidget(chatFrame)
        self.setLayout(mainhbox)

    def chatBox(self, list_of_chat_objects):
        # return a small box for recent chat
        return []

    def loadChats(self):
        # parse json data and get all chats
        file = open('./data/chats.json')
        data = json.load(file)
        chats = self.chatBox(data["chats"])
        return chats
    