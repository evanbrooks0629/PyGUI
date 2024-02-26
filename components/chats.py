from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from components.agents import AgentsFrame
import json
from datetime import datetime

class ChatsFrame(QFrame):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            background-color: #464545; 
            border-radius: 20;
        """)
        mainhbox = QHBoxLayout()

        chatHistoryFrame = QFrame()
        chatHistoryFrame.setStyleSheet("""
            background-color: #5E5E5E; 
            border-radius: 20;              
        """)
        chatHistoryFrame.setFixedWidth(200)
        vlay = QVBoxLayout()
        
        pastChats = self.loadChats()
        for i in range(len(pastChats)):
            vlay.addWidget(pastChats[i])
        vlay.addStretch()
        chatHistoryFrame.setLayout(vlay)

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

        mainhbox.addWidget(chatHistoryFrame)
        mainhbox.addWidget(chatFrame)
        self.setLayout(mainhbox)

    def chatBox(self, list_of_chat_objects):
        # return a small box for recent chat
        chatBoxes = []
        N = range(len(list_of_chat_objects))[::-1]
        for i in N:
            box = QFrame()
            name = QLabel(list_of_chat_objects[i]["name"])
            date = QLabel(list_of_chat_objects[i]["date"])
            vlay = QVBoxLayout()
            vlay.addWidget(name)
            vlay.addWidget(date)
            box.setLayout(vlay)
            box.setStyleSheet("""
                background-color: #464545;
                border-radius: 10;
            """)
            chatBoxes.append(box)
        return chatBoxes

    def loadChats(self):
        # parse json data and get all chats
        file = open('./data/chats.json')
        data = json.load(file)
        chats = self.chatBox(data["chats"])
        return chats
    