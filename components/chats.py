from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from components.agents import AgentsFrame
import json
from datetime import datetime

class ClickableFrame(QFrame):
    def __init__(self, currentChat, widget, pos, parent=None):
        super().__init__(parent)
        self.chatPanel = parent
        self.position = pos
        self.widget = widget # Keeps track of associated AgentsFrame class

        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # import any information needed from the agent for editing
        self.chat = currentChat #raw json information
        self.clicked = False #variable to keep tracked of click
        #self.setFixedWidth(190)
        # self.setFixedHeight(200)
        self.setStyleSheet("""
            background-color: #464545;
            border-radius: 10;
        """)
        bold = QFont()
        bold.setBold(True)
        chatVBox = QVBoxLayout()
        self.name = currentChat['name']
        self.date = currentChat['date']
        self.teamID = currentChat['team']
        self.conversation = currentChat['conversation']
        self.nameLabel = QLabel(self.name)
        self.nameLabel.setWordWrap(True)
        self.dateLabel = QLabel(self.date)
        
        chatVBox.addWidget(self.nameLabel)
        chatVBox.addWidget(self.dateLabel)

        self.setLayout(chatVBox)

    def mousePressEvent(self, event):
        print(self.chat['name'] ,"Frame Clicked!")
        print(self.conversation)
        self.widget.resetBorders(self) #unmark the borders of the previously clicked agent
        self.clicked = not self.clicked
        if self.clicked:
            self.widget.clickedChat = self
            self.widget.currentChat = self.chat

        # load chat in parent window
        # in form of :
        # <title> at top
        # then conversation in chunks with scroll
        # each chunk (interaction between user / agent) will have two boxes for each

        self.update()
        self.widget.loadChat(self.chat)

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.clicked:
            painter = QPainter(self)
            color = QColor(117, 219, 233)  # From Figma
            pen = QPen(color, 3, Qt.PenStyle.SolidLine)
            pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)  # For rounded corners
            painter.setPen(pen)
            painter.drawRoundedRect(1, 1, self.width() - 2, self.height() - 2, 10, 10)  


class NewChatButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setStyleSheet("""
            QPushButton {  
                background-color: transparent;
                border: 2px solid #75DBE9;
                height: 50;
                border-radius: 10;
                color: #75DBE9;
            }
                           
            QPushButton:hover {
                background-color: #111111;
            }

            QPushButton:pressed {
                background-color: #5E5E5E;
            }
        """)
        self.setText("New Chat")
        self.setIcon(QIcon('./assets/NewChatIcon.png'))
        self.setIconSize(QSize(48, 24))

class SendChatButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setStyleSheet("""
            QPushButton {  
                background-color: transparent;
                border: 2px solid #75DBE9;
                border-radius: 10;
                color: #75DBE9;
            }
                           
            QPushButton:hover {
                background-color: #111111;
            }

            QPushButton:pressed {
                background-color: #5E5E5E;
            }
        """)
        self.setFixedWidth(100)
        self.setFixedHeight(100)
        self.setIcon(QIcon('./assets/SendIcon.png'))
        self.setIconSize(QSize(48, 48))
    
    def mousePressEvent(self, event):
        print("Send Chat Clicked")
        self.parent().parent().parent().uploadPrompt()

class ChatsFrame(QFrame):
    def __init__(self):
        super().__init__()

        self.clickableChats = []
        self.currentChat = {}
        self.allTeams = []
        self.selectedTeam = {}

        self.setStyleSheet("""
            background-color: #464545; 
            border-radius: 20;
        """)

        self.mainhbox = QHBoxLayout()

        self.chatHistoryFrame = QFrame()
        self.chatHistoryFrame.setStyleSheet("""
            background-color: #5E5E5E; 
            border-radius: 20;              
        """)
        self.chatHistoryFrame.setFixedWidth(250)

        chatHistoryLayout = QVBoxLayout()

        # New chat button and line
        newChatButton = NewChatButton()
        newChatButton.clicked.connect(self.loadDefaultChatView)  # Ensure this method is defined to reset the chat view
        newChatLine = QLabel()
        newChatLine.setStyleSheet("""
            background-color: #464545;
            border-radius: 0;
        """)
        newChatLine.setFixedHeight(2)

        chatHistoryLayout.addWidget(newChatButton)
        chatHistoryLayout.addWidget(newChatLine)

        # Scroll Area for Past Chats
        scrollArea = QScrollArea()
        scrollArea.verticalScrollBar().setStyleSheet("""
            QScrollBar:vertical
            {
                background-color: #5E5E5E;
                width: 15px;
                margin: 15px 3px 15px 3px;
                border: 3px transparent #5E5E5E;
                border-radius: 4px;
            }

            QScrollBar::handle:vertical
            {
                background-color: #464545;
                min-height: 5px;
                border-radius: 4px;
            }

            QScrollBar::sub-line:vertical
            {
                margin: 3px 0px 3px 0px;
                border-image: url(:/qss_icons/rc/up_arrow_disabled.png);
                height: 10px;
                width: 10px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }

            QScrollBar::add-line:vertical
            {
                margin: 3px 0px 3px 0px;
                border-image: url(:/qss_icons/rc/down_arrow_disabled.png);
                height: 10px;
                width: 10px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }

            QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on
            {
                border-image: url(:/qss_icons/rc/up_arrow.png);
                height: 10px;
                width: 10px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }

            QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on
            {
                border-image: url(:/qss_icons/rc/down_arrow.png);
                height: 10px;
                width: 10px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }

            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical
            {
                background: none;
            }

            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
            {
                background: none;
            }
        """)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scrollArea.setWidgetResizable(True)
        # scrollArea.setStyleSheet("border: none;")  # Optional, for aesthetics

        # Container for past chats, with its own layout
        chatsContainer = QWidget()
        chatsLayout = QVBoxLayout()
        chatsContainer.setLayout(chatsLayout)

        # Load and add past chats to the chatsLayout instead of directly to the frame
        pastChats = self.loadChats()
        for chat in pastChats:
            chatsLayout.addWidget(chat)
        chatsLayout.addStretch()

        # Add the container to the scroll area
        scrollArea.setWidget(chatsContainer)

        # Add the scroll area to the chat history layout
        chatHistoryLayout.addWidget(scrollArea)

        self.chatHistoryFrame.setLayout(chatHistoryLayout)
        self.mainhbox.addWidget(self.chatHistoryFrame)

        # Additional setup for the rest of your layout...
        self.setLayout(self.mainhbox)

        self.chatFrame = QFrame()
        self.chatFrame.setStyleSheet("""
            background-color: #5E5E5E; 
            border-radius: 20;
        """)

        self.chatVBox = QVBoxLayout()

        self.loadDefaultChatView()

        self.chatFrame.setLayout(self.chatVBox)

        self.mainhbox.addWidget(self.chatHistoryFrame)
        self.mainhbox.addWidget(self.chatFrame)
        self.setLayout(self.mainhbox)

    def loadDefaultChatView(self):
        # Clear existing content from the chat layout
        for i in reversed(range(self.chatVBox.count())): 
            widget = self.chatVBox.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        chatBox = QLabel("Welcome to TaskForceAI. Select a Team of Agents to complete your task. Then, type the task you’d like your Team to complete.")
        chatBox.setStyleSheet("""
            background-color: #464545; 
            border-radius: 20;
            padding: 20;
            font: 16px;
        """)
        # chatBox.setFixedHeight(80)
        chatBox.setWordWrap(True)
        chatBox.setAlignment(Qt.AlignmentFlag.AlignTop)

        teamSelectFrame = QFrame()
        teamSelectFrame.setStyleSheet("""
            background-color: #464545;
            color: #ffffff;
            padding: 20;
        """)
        teamSelectFrame.setFixedHeight(300)

        selectFrame = QFrame()
        teamBox = QHBoxLayout()
        selectBox = QVBoxLayout()
        
        # select team

        selectTeamLabel = QLabel('Select a Team')
        selectTeamLabel.setStyleSheet("""
            background-color: #464545;
            padding: 0;
        """)
        selectTeamLabel.setFixedWidth(200)

        self.teamComboBox = QComboBox()
        # self.teamComboBox.setStyleSheet("background-color: #5E5E5E;")
        # self.teamComboBox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        # #pull from models.json
        teamsFile = open('./data/teams.json')
        teamsData = json.load(teamsFile)
        teams = teamsData["teams"]

        agentsFile = open('./data/agents.json')
        agentsData = json.load(agentsFile)
        agents = agentsData["agents"]

        teamsList = []

        # #pulls default models for new agent (add functionality for pulling from agents.json)
        for team in teams:
            self.teamComboBox.addItem(team['name'])

            agentIds = team['agents']

            teamObj = {
                "name": team["name"],
                "id": team["id"],
                "agents": []
            }

            teamAgents = []

            for id in agentIds:
                agent = [agent for agent in agents if agent["id"] == id][0]
                teamAgents.append(agent)

            teamObj["agents"] = teamAgents
            # print(teamObj)
            teamsList.append(teamObj)
        # print(teamsList)
        self.allTeams = teamsList

        selectBox.addWidget(selectTeamLabel)
        selectBox.addWidget(self.teamComboBox)
        selectFrame.setLayout(selectBox)

        teamBox.addWidget(selectFrame)
        teamSelectFrame.setLayout(teamBox)

        middleSpacer = QFrame()

        self.bottom = QFrame()
        self.bottom.setFixedHeight(150)
        self.bottomlay = QHBoxLayout()
        self.bottomlay.setContentsMargins(0, 0, 10, 0)
        
        self.textBox = QPlainTextEdit()
        self.textBox.setStyleSheet("""
            background-color: #464545;
            color: #ffffff;
            padding: 20;
        """)
        # textBox.setFixedHeight(50)
        self.textBox.setPlaceholderText("Type anything...")

        self.sendChatButton = SendChatButton()

        self.bottomlay.addWidget(self.textBox)
        self.bottomlay.addWidget(self.sendChatButton)
        self.bottom.setLayout(self.bottomlay)

        self.chatVBox.addWidget(chatBox)
        self.chatVBox.addWidget(teamSelectFrame)
        self.chatVBox.addWidget(middleSpacer, 1)
        self.chatVBox.addWidget(self.bottom)
        self.chatFrame.setStyleSheet("""
            background-color: #5E5E5E;
        """)
        self.resetBorders(None)

    def resetBorders(self, clicked_frame):
        # Reset borders of all clickable frames except the clicked frame
        for current in self.clickableChats:
            if current != clicked_frame:
                current.clicked = False
                current.update()

    def chatBox(self, list_of_chat_objects):
        # return a small box for recent chat
        chatBoxes = []
        N = range(len(list_of_chat_objects))[::-1]
        for i in N:
            chatBox = ClickableFrame(list_of_chat_objects[i], self, i, self)
            self.clickableChats.append(chatBox)
            chatBoxes.append(chatBox)
        return chatBoxes

    def loadChats(self):
        # parse json data and get all chats
        file = open('./data/chats.json')
        data = json.load(file)
        chats = self.chatBox(data["chats"])
        return chats
    
    def find_first_matched_agent(self, agents, interaction):
        agent_id = interaction['agent']['id']
        for agent in agents:
            if agent['id'] == agent_id:
                return agent  # Return the first match immediately
        # If no match is found, return a default object
        return {"name": "Agent"}
    
    def find_first_matched_team(self, teams, conversation):
        team_id = conversation['team']
        for team in teams:
            if team['id'] == team_id:
                return team  # Return the first match immediately
        # If no match is found, return a default object
        return {
            "name": "Crew",
            "agents": []
        }
    
    def createUserBox(self, user):
        userFrame = QFrame()
        userFrame.setStyleSheet("""
            background-color: #5E5E5E;
            border-radius: 5;
        """)
        userBox = QVBoxLayout()
        userLabel = QLabel("You:")
        # userLabel.setStyleSheet("""
        #     background-color: #464545;
        #     border-radius: 5;
        #     padding: 5;
        # """)
        textLabel = QLabel(user["text"])
        textLabel.setStyleSheet("""
            background-color: #464545;
            border-radius: 5;
            padding: 5;
        """)
        userBox.addWidget(userLabel)
        userBox.addWidget(textLabel)
        userFrame.setLayout(userBox)
        return userFrame

    def createAgentBox(self, agent, agentName):
        agentFrame = QFrame()
        agentFrame.setStyleSheet("""
            background-color: #5E5E5E;
            border-radius: 5;
        """)
        agentBox = QVBoxLayout()
        agentLabel = QLabel(agentName + ":")
        # agentLabel.setStyleSheet("""
        #     background-color: #464545;
        #     border-radius: 5;
        #     padding: 5;
        # """)
        textLabel = QLabel(agent["text"])
        textLabel.setStyleSheet("""
            background-color: #464545;
            border-radius: 5;
            padding: 5;
        """)
        agentBox.addWidget(agentLabel)
        agentBox.addWidget(textLabel)
        agentFrame.setLayout(agentBox)
        return agentFrame

    def createInteractionBox(self, interaction, agentName):
        interactionFrame = QFrame()
        interactionFrame.setStyleSheet("""
            background-color: #464545;
            border-radius: 10;
        """)
        userBox = self.createUserBox(interaction["user"])
        agentBox = self.createAgentBox(interaction["agent"], agentName)
        interactionBox = QVBoxLayout()
        interactionBox.addWidget(userBox)
        interactionBox.addWidget(agentBox)
        interactionFrame.setLayout(interactionBox)
        return interactionFrame
    
    def loadChat(self, chat):
        for i in reversed(range(self.chatVBox.count())): 
            widget = self.chatVBox.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
    
        # Load teams and agents data
        with open('./data/teams.json') as teamsFile:
            teamsData = json.load(teamsFile)
        teams = teamsData["teams"]
        team = self.find_first_matched_team(teams, chat)

        with open('./data/agents.json') as agentsFile:
            agentsData = json.load(agentsFile)
        agents = agentsData["agents"]
        conversation = chat["conversation"]

        nameLabel = QLabel(chat["name"])
        nameLabel.setStyleSheet("""
            font: 16px;
            margin-left: 8px;
        """)
        teamLabelLeft = QLabel("            Team: [")
        teamLabel = QLabel(team["name"])
        teamLabel.setStyleSheet("""
            color: #75DBE9;
        """)
        teamLabelRight = QLabel("]")
        dateLabel = QLabel(chat["date"])

        topFrame = QFrame()
        toplayout = QHBoxLayout()
        toplayout.addWidget(nameLabel)
        toplayout.addWidget(teamLabelLeft)
        toplayout.addWidget(teamLabel)
        toplayout.addWidget(teamLabelRight)
        toplayout.addStretch()
        toplayout.addWidget(dateLabel)
        topFrame.setLayout(toplayout)

        self.chatVBox.addWidget(topFrame)
        
        scrollArea = QScrollArea()
        scrollArea.verticalScrollBar().setStyleSheet("""
            QScrollBar:vertical
            {
                background-color: #464545;
                width: 15px;
                margin: 15px 3px 15px 3px;
                border: 3px transparent #464545;
                border-radius: 4px;
            }

            QScrollBar::handle:vertical
            {
                background-color: #5E5E5E;
                min-height: 5px;
                border-radius: 4px;
            }

            QScrollBar::sub-line:vertical
            {
                margin: 3px 0px 3px 0px;
                border-image: url(:/qss_icons/rc/up_arrow_disabled.png);
                height: 10px;
                width: 10px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }

            QScrollBar::add-line:vertical
            {
                margin: 3px 0px 3px 0px;
                border-image: url(:/qss_icons/rc/down_arrow_disabled.png);
                height: 10px;
                width: 10px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }

            QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on
            {
                border-image: url(:/qss_icons/rc/up_arrow.png);
                height: 10px;
                width: 10px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }

            QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on
            {
                border-image: url(:/qss_icons/rc/down_arrow.png);
                height: 10px;
                width: 10px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }

            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical
            {
                background: none;
            }

            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
            {
                background: none;
            }
        """)
        scrollArea.setWidgetResizable(True)
        scrollAreaWidgetContents = QWidget()
        scrollArea.setWidget(scrollAreaWidgetContents)

        scrollLayout = QVBoxLayout(scrollAreaWidgetContents)
        # For each interaction, create and add its box to the layout
        for interaction in conversation:
            agent = self.find_first_matched_agent(agents, interaction)
            agentName = agent["name"]
            interactionBox = self.createInteractionBox(interaction, agentName)
            scrollLayout.addWidget(interactionBox)

        scrollLayout.addStretch()
        self.chatVBox.addWidget(scrollArea)
        # Add stretch to push everything up and make the layout scrollable if needed
        self.chatFrame.setStyleSheet("""
            background-color: #464545;
        """)
        print("Chat loaded")

    def uploadPrompt(self):
        # get the text from user input (self.textBox)
        systemMessage = self.textBox.toPlainText()
        self.textBox.clear() # empty text box
        print("Prompt: " + systemMessage)

        selectedTeamName = self.teamComboBox.currentText()
        print("Team: " + selectedTeamName)

        
        # find team with matching name (will be id but name for now)
        selectedTeam = [team for team in self.allTeams if team["name"] == selectedTeamName][0]
        chatObject = {
            "message": systemMessage,
            "team": selectedTeam["agents"]
        }

        print(chatObject) # Bryan this is what u want!!

        # send the prompt to server where LLM is running
        # userproxy.initiatechat
        # get models, functions, teams, agents
        # functions will have nothing for now
