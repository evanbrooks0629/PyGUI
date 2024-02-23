from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import json

class AgentsFrame(QFrame):
    def __init__(self):
        super().__init__()

        # Set tab style
        # frame = QFrame()
        self.setStyleSheet("background-color: #464545; border-radius: 20;")
        mainhbox = QHBoxLayout()

        agent = self.loadAgents()
        chatFrame = QFrame()
        chatFrame.setStyleSheet("background-color: #5E5E5E; border-radius: 20;")
        chatVBox = QVBoxLayout()
        chatVBox.addWidget(agent)
        chatFrame.setLayout(chatVBox)

        agentsTasksFrame = QFrame()
        agentsTasksFrame.setStyleSheet("background-color: #5E5E5E; border-radius: 20;")
        agentsTasksVBox = QVBoxLayout()
        agentsTasksFrame.setLayout(agentsTasksVBox)

        mainhbox.addWidget(chatFrame)
        mainhbox.addWidget(agentsTasksFrame)
        self.setLayout(mainhbox)
        

    def agentBox(self, list_of_agent_objects):
        # print(list_of_agent_objects)
        obj = list_of_agent_objects[0]
        print(obj)
        agentBox = QFrame()
        agentBox.setFixedWidth(200)
        agentBox.setFixedHeight(200)
        agentBox.setStyleSheet("""
            background-color: #464545;
            border-radius: 10;
        """)
        agentVBox = QVBoxLayout()
        name = obj['name']
        description = obj['description']
        system_message = obj["system_message"]
        skills = obj["skills"]
        nameLabel = QLabel(name)
        descriptionLabel = QLabel(description)
        systemMessageLabel = QLabel(system_message)
        skillsLabel = QLabel(skills[0])
        agentVBox.addWidget(nameLabel)
        agentVBox.addWidget(descriptionLabel)
        agentVBox.addWidget(systemMessageLabel)
        agentVBox.addWidget(skillsLabel)
        agentBox.setLayout(agentVBox)
        return agentBox

    def loadAgents(self):
        file = open('./data/agents.json')
        data = json.load(file)
        agents = self.agentBox(data["agents"])
        return agents
        # loop through agents and display accordingly
### TODO:
    # [ ] Rename variables