from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

class DashboardFrame(QFrame):
    def __init__(self):
        super().__init__()

        # Set tab style
        # frame = QFrame()
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
        chatVBox = QVBoxLayout()

        ### ADD CONTENT TO CHATVBOX HERE ###

        chatBox = QLabel("Hi, I’m Sparky, your AI assistant. Type the task you’d like our engineering team to complete, and I’ll make sure everything is done perfectly! To get started, just type below.")
        chatBox.setStyleSheet("""
            background-color: #464545; 
            border-radius: 20;
            padding: 20; 
        """)
        chatBox.setFixedHeight(200)
        chatBox.setWordWrap(True)

        sparkyFrame = QFrame()
        sparkyHBox = QHBoxLayout()
        sparky = QLabel(self)
        sparkyPixmap = QPixmap('./assets/Spark.png')
        sparkyPixmapScaled = sparkyPixmap.scaled(250, 250)
        sparky.setPixmap(sparkyPixmapScaled)
        sparkyHBox.addWidget(sparky, alignment=Qt.AlignmentFlag.AlignCenter)
        sparkyFrame.setLayout(sparkyHBox)

        textBox = QPlainTextEdit()
        textBox.setStyleSheet("""
            background-color: #464545;
            color: #ffffff;
            padding: 20;
        """)
        textBox.setPlaceholderText("Type anything...")
        # textBox.setFixedHeight(200)

        chatVBox.addWidget(chatBox)
        chatVBox.addWidget(sparkyFrame)
        chatVBox.addWidget(textBox)

        chatFrame.setLayout(chatVBox)

        employeesTasksFrame = QFrame()
        employeesTasksFrame.setStyleSheet("""
            background-color: #5E5E5E; 
            border-radius: 20;
        """)
        employeesTasksVBox = QVBoxLayout()

        ### ADD CONTENT TO EMPLOYEESTASKSVBOX HERE ###

        employeesFrame = QFrame()
        employeesHBox = QHBoxLayout()
        employeesLabel = QLabel("Employees")
        employeesFrame.setStyleSheet("""
            background-color: #464545;
            color: #ffffff;
        """)
        employeesFrame.setFixedWidth(400)
        employeesHBox.addWidget(employ