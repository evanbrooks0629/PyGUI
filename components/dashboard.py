from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from components.agents import AgentsFrame

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

        agentsTasksFrame = QFrame()
        agentsTasksFrame.setStyleSheet("""
            background-color: #5E5E5E; 
            border-radius: 20;
        """)
        agentsTasksVBox = QVBoxLayout() 
        ### ADD CONTENT TO AGENTSSTASKSVBOX HERE ###

        agentsFrame = self.createAgentsFrame("Agents", 40)
        scroll1 = QScrollArea()
        scroll1.setWidgetResizable(True)
        scroll1.setWidget(agentsFrame)
        scroll1.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll1.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        agentsTasksVBox.addWidget(scroll1)

        agentsTasks = self.createAgentsTasks("Tasks", 40)
        scroll2 = QScrollArea()
        scroll2.setWidgetResizable(True)
        scroll2.setWidget(agentsTasks)
        scroll2.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll2.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        agentsTasksVBox.addWidget(scroll2)

        agentsTasksFrame.setLayout(agentsTasksVBox)
        agentsTasksFrame.setFixedWidth(400)

        mainhbox.addWidget(chatFrame)
        mainhbox.addWidget(agentsTasksFrame)
        self.setLayout(mainhbox)

       
    def createAgentsFrame(self, title, numAgents):
        agentsFrame = QFrame()
        agentsLayout = QGridLayout()
        agentsLabel = QLabel(title)
        agentsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        agentsFrame.setStyleSheet("""
            background-color: #464545;
            color: #ffffff;
        """)
        agentsFrame.setFixedWidth(375)
        agentsLayout.addWidget(agentsLabel, 0, 0, 1, 3)  # Span label across 3 columns

        # Add buttons to agentsFrame in a grid layout
        row, col = 1, 0
        for i in range(1, numAgents + 1):
            agent = QIcon('./assets/agentJim.png')
            button = QToolButton(agentsFrame)
            button.setIcon(agent)
            button.setIconSize(QSize(64, 45))
            button.clicked.connect(self.switchToAgents)
            agentsLayout.addWidget(button, row, col)
            col += 1
            if col == 3:
                col = 0
                row += 1

        agentsFrame.setLayout(agentsLayout)
        return agentsFrame

    def switchToAgents(self):
        # agentsFrame = AgentsFrame()
        # self.setCentralWidget(agentsFrame)
        #figure out how to navigate to agent info in agent tab
        return

    def createAgentsTasks(self, title, numTasks):
        tasksFrame = QFrame()
        tasksLayout = QGridLayout()
        tasksLabel = QLabel(title)
        tasksLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tasksFrame.setStyleSheet("""
            background-color: #464545;
            color: #ffffff;
        """)
        tasksFrame.setFixedWidth(375)
        tasksLayout.addWidget(tasksLabel, 0, 0, 1, 1)
        row, col = 1, 0
        for i in range(1, numTasks + 1):
            button = QPushButton(f"Button {i}", tasksFrame)
            tasksLayout.addWidget(button, row, col)
            col = 0
            row += 1

        tasksFrame.setLayout(tasksLayout)
        return tasksFrame