from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from components.agents import AgentsFrame
import json
from datetime import datetime

class NewChatButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.clicked = False
        self.setStyleSheet("""
            background-color: transparent;
            border: 2px solid #75DBE9;
            height: 50;
            border-radius: 10;
            color: #75DBE9;
        """)
        self.setText("New Chat")
        self.setIcon(QIcon('./assets/NewChatIcon.png'))
        self.setIconSize(QSize(48, 24))
    
    def mousePressEvent(self, event):
        print("New Chat Clicked")

class SendChatButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.clicked = False
        self.setStyleSheet("""
            background-color: transparent;
            height: 50;
            border-radius: 10;
            color: #75DBE9;
        """)
        self.setFixedWidth(100)
        self.setIcon(QIcon('./assets/SendIcon.png'))
        self.setIconSize(QSize(48, 48))
    
    def mousePressEvent(self, event):
        print("Send Chat Clicked")

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

        # top of chats
        # new chat button and line
        newChatButton = NewChatButton()
        newChatLine = QLabel()
        newChatLine.setStyleSheet("""
            background-color: #464545;
            border-radius: 0;
        """)
        newChatLine.setFixedHeight(2)

        vlay.addWidget(newChatButton)
        vlay.addWidget(newChatLine)
        
        # chat boxes
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
        # chatBox.setFixedHeight(200)
        chatBox.setWordWrap(True)
        chatBox.setAlignment(Qt.AlignmentFlag.AlignTop)

        bottom = QFrame()
        bottom.setFixedHeight(150)
        bottomlay = QHBoxLayout()
        bottomlay.setContentsMargins(0, 0, 10, 0)
        
        textBox = QPlainTextEdit()
        textBox.setStyleSheet("""
            background-color: #464545;
            color: #ffffff;
            padding: 20;
        """)
        # textBox.setFixedHeight(50)
        textBox.setPlaceholderText("Type anything...")

        sendChatButton = SendChatButton()

        bottomlay.addWidget(textBox)
        bottomlay.addWidget(sendChatButton)
        bottom.setLayout(bottomlay)

        chatVBox.addWidget(chatBox)
        chatVBox.addWidget(bottom)
        

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
    