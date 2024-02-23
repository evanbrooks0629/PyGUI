from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import json

class TeamsFrame(QFrame):
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

    def teamBox(self, list_of_team_objects):
        # return a small box for recent chat
        return []

    def loadTeams(self):
        # parse json data and get all chats
        file = open('./data/teams.json')
        data = json.load(file)
        teams = self.teamBox(data["teams"])
        return teams
    

### TODO:
    # [ ] Rename variables