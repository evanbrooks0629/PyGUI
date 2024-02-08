from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

class DashboardFrame(QFrame):
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
        employeesHBox.addWidget(employeesLabel)
        employeesFrame.setLayout(employeesHBox)
        employeesTasksVBox.addWidget(employeesFrame)

        tasksLabel = QLabel("Tasks")

        employeesTasksVBox.addWidget(tasksLabel)
        employeesTasksFrame.setLayout(employeesTasksVBox)

        mainhbox.addWidget(chatFrame)
        mainhbox.addWidget(employeesTasksFrame)
        self.setLayout(mainhbox)
