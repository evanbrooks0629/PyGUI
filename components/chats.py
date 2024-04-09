from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from components.agents import AgentsFrame
import json
import autogen
import ast
from datetime import datetime

class CustomComboBox(QComboBox):
    def __init__(self, *args, **kwargs):
        super(CustomComboBox, self).__init__(*args, **kwargs)
        self.setIconSize(QSize(16, 16))
        self.setStyleSheet("""
            QComboBox::down-arrow {
                image: url('./assets/DropdownIcon.png');
                width: 30px;
                height: 30px;
                padding-right: 10px;
            }
            QComboBox::drop-down {
                border: 0px;
            }
            QComboBox {
                background-color: #5E5E5E;
                border-radius: 10px;
                color: #ffffff;
                margin-top: 30px
            } 
        """)

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
        self.clicked = False 
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
        super().mousePressEvent(event)
        print(self.chat['name'] ,"Frame Clicked!")
        print(self.conversation)
        self.widget.resetBorders(self) #unmark the borders of the previously clicked agent
        self.clicked = not self.clicked
        if self.clicked:
            self.widget.clickedChat = self
            self.widget.currentChat = self.chat

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
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setStyleSheet("""
            QPushButton {  
                background-color: transparent;
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
        self.setFixedWidth(60)
        self.setFixedHeight(60)
        self.setIcon(QIcon('./assets/SendIcon.png'))
        self.setIconSize(QSize(48, 48))
    
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        print("Send Chat Clicked")
        # self.uploadPrompt()

class ChatsFrame(QFrame):
    def __init__(self):
        super().__init__()

        self.clickableChats = []
        self.currentChat = {}
        self.allTeams = []
        self.selectedTeam = {}

        self.sendChatButton = SendChatButton(self)
        self.sendChatButton.show()
        self.sendChatButton.clicked.connect(self.uploadPrompt)

        self.setStyleSheet("""
            background-color: #464545; 
            border-radius: 20;
        """)

        self.mainhbox = QHBoxLayout()
        self.setLayout(self.mainhbox)

        self.chatHistoryFrame = QFrame()
        self.chatHistoryFrame.setStyleSheet("""
            background-color: #5E5E5E; 
            border-radius: 20;              
        """)
        self.chatHistoryFrame.setFixedWidth(250)

        chatHistoryLayout = QVBoxLayout()

        # New chat button and line
        newChatButton = NewChatButton()
        newChatButton.clicked.connect(self.loadDefaultChatView)
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
        chatHistoryLayout.addWidget(scrollArea)

        self.chatHistoryFrame.setLayout(chatHistoryLayout)
        self.mainhbox.addWidget(self.chatHistoryFrame)

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

        self.teamSelectFrame = QFrame()
        self.teamSelectFrame.setStyleSheet("""
            background-color: #464545;
            color: #ffffff;
            padding: 20px;
        """)
        self.teamSelectFrame.setFixedHeight(300)

        selectFrame = QFrame()
        self.agentsFrame = QFrame()
        teamBox = QHBoxLayout()
        selectBox = QVBoxLayout()
        self.agentsBox = QVBoxLayout()
        self.agentsFrame.setLayout(self.agentsBox)
        self.agentsFrame.setStyleSheet("background-color: #464545;")

        verticalLine = QLabel("")
        verticalLine.setStyleSheet("""
            background-color: #5E5E5E;
        """)
        verticalLine.setFixedWidth(2)

        selectTeamLabel = QLabel('Select a Team')
        selectTeamLabel.setStyleSheet("""
            background-color: #464545;
            padding: 0;
            padding-bottom: 10px;
        """)

        self.teamComboBox = CustomComboBox()
        self.teamComboBox.currentIndexChanged[int].connect(self.retrieveTeamOnChange)
        
        teamsFile = open('./data/teams.json')
        teamsData = json.load(teamsFile)
        teams = teamsData["teams"]

        agentsFile = open('./data/agents.json')
        agentsData = json.load(agentsFile)
        agents = agentsData["agents"]

        teamsList = []

        for team in teams:
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
            teamsList.append(teamObj)

            self.teamComboBox.addItem(team["name"], teamObj)

        self.allTeams = teamsList
        self.selectedTeam = self.allTeams[0]

        selectBox.addWidget(selectTeamLabel)
        selectBox.addWidget(self.teamComboBox, 1)
        selectBox.addStretch(1)
        selectFrame.setLayout(selectBox)

        teamBox.addWidget(selectFrame)
        teamBox.addWidget(verticalLine)
        teamBox.addWidget(self.agentsFrame)
        self.teamSelectFrame.setLayout(teamBox)

        self.bottom = QFrame()
        self.bottomlay = QHBoxLayout()
        self.bottomlay.setContentsMargins(0, 0, 0, 0)
        
        self.textBox = QPlainTextEdit()
        self.textBox.setStyleSheet("""
            background-color: #464545;
            color: #ffffff;
            padding: 20;
        """)
        self.textBox.setPlaceholderText("Type anything...")
        self.sendChatButton.show()  
        self.sendChatButton.raise_()  

        self.bottomlay.addWidget(self.textBox)
        self.bottom.setLayout(self.bottomlay)

        self.chatVBox.addWidget(chatBox)
        self.chatVBox.addWidget(self.teamSelectFrame)
        self.chatVBox.addWidget(self.bottom, 1)
        self.chatFrame.setStyleSheet("""
            background-color: #5E5E5E;
        """)
        self.resetBorders(None)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Calculate the new position
        newX = self.width() - self.sendChatButton.width() - 50
        newY = self.height() - self.sendChatButton.height() - 50
        self.sendChatButton.move(newX, newY)
        self.sendChatButton.raise_()  

    @pyqtSlot(int)
    def retrieveTeamOnChange(self, index):
        agentObject = self.teamComboBox.itemData(index)
        if agentObject is not None:
            self.selectedTeam = agentObject
            agentsListText = ""
            for agent in self.selectedTeam["agents"]:
                agentsListText += "→   " + agent["name"] + ": " + agent["description"] + "\n"
            
            agentTitle = QLabel(agentObject["name"] + " Agents:")
            agentTitle.setStyleSheet("""
                background-color: #464545;
                padding: 0;
                padding-bottom: 10px;
            """)

            agentsList = QLabel(agentsListText)
            agentsList.setStyleSheet("""
                background-color: #464545;
                padding: 10px;
            """)
            agentsList.setFixedHeight(150)
            
            self.clearLayout(self.agentsFrame.layout())
            self.agentsFrame.layout().addWidget(agentTitle)
            self.agentsFrame.layout().addWidget(agentsList)
            self.agentsFrame.layout().addStretch()

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

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
        self.sendChatButton.hide()
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

    def create_assistant_agent(self, agent_info):
        #Assuming AssistantAgent creation logic based on agent_info
        if len(agent_info["skills"]) == 0:
            return autogen.AssistantAgent(
                name=agent_info["name"],
                system_message=agent_info["description"],
                llm_config=agent_info["llm_config"],
                #Add other parameters based on your agent_info structure
            )
        else: 
            allSkills = []
            with open('./data/functions.json') as funcFile:
                func = json.load(funcFile)
            functions = func["functions"]

            fmap = {}
            o = open("./functions/skills.py", "r")
            text = o.read()
            p = ast.parse(text)

            for i in agent_info["skills"]:
                for j in functions:
                    if i == j["name"]:
                        toadd = {"name": j["name"],
                                "description": j["description"],
                                "parameters": j["parameters"]
                                }
                        allSkills.append(toadd)
                for node in ast.walk(p):
                    if isinstance(node, ast.FunctionDef):
                        if node.name == i:
                            fmap[node.name] = node
            #print(allSkills)
            #print(fmap)
            llm_config = agent_info["llm_config"]
            llm_config["functions"] = allSkills
            agent = autogen.AssistantAgent(
                name=agent_info["name"],
                system_message=agent_info["description"],
                llm_config=llm_config
            )

            agent.register_function(
                function_map = fmap
            )

            return agent

    def uploadPrompt(self):
        # get the text from user input (self.textBox)
        systemMessage = self.textBox.toPlainText()
        self.textBox.clear() # empty text box

        if self.selectedTeam == {}:
            return
        
        print(systemMessage)

        #Create the UserProxyAgent
        user_proxy = autogen.UserProxyAgent(
            name="User_proxy",
            system_message="A human admin.",
            code_execution_config={
                "last_n_messages": 2,
                "work_dir": "groupchat",
                "use_docker": False,
            },
            human_input_mode="TERMINATE",
        )

        # Create other AssistantAgent objects from the team
        assistant_agents = [self.create_assistant_agent(agent_info) for agent_info in self.selectedTeam["agents"]]

        # Combine UserProxyAgent with other agents for the group chat
        all_agents = [user_proxy] + assistant_agents

        # Create GroupChat and GroupChatManager
        groupchat = autogen.GroupChat(agents=all_agents, messages=[], max_round=5)
        manager = autogen.GroupChatManager(groupchat=groupchat, llm_config = {"model": "openhermes",
                                                                              "base_url": "http://localhost:11434/v1",
                                                                              "api_type": "openai",
                                                                              "api_key": "ollama"
                                                                            }
        )

         # # Start the chat with the specified message
        #when not using group manager just user proxy 
        user_proxy.initiate_chat(manager, message=systemMessage)
