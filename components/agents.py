from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import json

class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Are You Sure You Want to Delete?")
        self.setStyleSheet("background-color: #464545;") 
        self.setGeometry(((QGuiApplication.primaryScreen().size().width()//2) - 150), ((QGuiApplication.primaryScreen().size().height()//2) - 75), 300, 150)
        layout = QVBoxLayout()
        label = QLabel("Delete this agent?")
        layout.addWidget(label)

        # Add a button to the dialog
        deleteButton = QPushButton("Yes, Delete")
        deleteButton.setStyleSheet("""
            background-color: transparent;
            text-decoration: underline;
        """)
        deleteButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        noButton = QPushButton("Cancel")
        noButton.setStyleSheet("""
            background-color: #5E5E5E;
            border-radius: 10px;
            padding: 5px;
        """)
        noButton.setFixedHeight(30)
        noButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        layout.addWidget(deleteButton)
        layout.addWidget(noButton)

        # Set the layout for the dialog
        self.setLayout(layout)

        self.willDelete = False

        # Connect the button to a slot
        deleteButton.clicked.connect(self.on_delete_button_clicked)
        noButton.clicked.connect(self.on_no_button_clicked)

    def on_no_button_clicked(self):
        self.close()

    def on_delete_button_clicked(self):
        print('delete clicked')
        self.willDelete = True
        self.close()

#mainframe (holds rest of classes -> left side = AgentsPanel (which holds one AddAgentButton and a ClickableFrame for each agent), right side = AgentValues)
class AgentsFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__()

        # for agents display on left panel
        self.agentPanel = AgentsPanel(self)

        #for changing contents of right panel
        self.editPanel = AgentValues(self)
        
        # Set tab style
        self.setStyleSheet("background-color: #464545; border-radius: 20;")
        self.mainhbox = QHBoxLayout()

        self.mainhbox.addWidget(self.agentPanel)
        self.mainhbox.addWidget(self.editPanel)

        self.mainhbox.setStretchFactor(self.agentPanel, 1) #equally sized left and right panels
        self.mainhbox.setStretchFactor(self.editPanel, 1)
        self.setLayout(self.mainhbox)


#left side panel that holds one AddAgentButton and a ClickableFrame for each agent
class AgentsPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Keep track of all agent boxes
        self.mainFrame = parent
        self.clickableAgents = []
        self.setStyleSheet("background-color: #5E5E5E; border-radius: 20;")
        self.viewVBox = QVBoxLayout()
        self.agentsLabel = QLabel()
        bold = QFont()
        bold.setBold(True)
        self.agentsLabel = QLabel('Agents')
        self.agentsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.agentsLabel.setFont(bold)
        self.row = 1
        self.col = 0
        
        # Scroll section and add agent button
        self.agents = QFrame()
        self.agentsLayout = QGridLayout()

        self.agentInfo = self.loadAgents()
        self.agentBox(self.agentInfo)
        self.agentScroll = QScrollArea()
        self.agentScroll.setWidgetResizable(True)
        self.agentScroll.setWidget(self.agents)
        self.agentScroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.agentScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Embed scroll into view agents section
        self.viewVBox.addWidget(self.agentScroll)
        self.setLayout(self.viewVBox)

    def agentBox(self, list_of_agent_objects):
        self.agents.setStyleSheet("background-color: #5E5E5E; border-radius: 20;")
        self.agentsLayout.addWidget(self.agentsLabel, 0, 0, 1, 3)  # Span label across 3 columns

        addButton = AddAgentButton()
        # addButton.setFixedSize(80, 40)
        self.agentsLayout.addWidget(addButton, 0, 2, 1, 1)

        ind = 0
        for currentAgent in list_of_agent_objects:
            obj = currentAgent
            agentBox = ClickableFrame(obj, self.mainFrame, ind, self)
            ind = ind + 1
            self.clickableAgents.append(agentBox)
            self.agentsLayout.addWidget(agentBox, self.row, self.col)
            self.col += 1
            if self.col == 3:
                self.col = 0
                self.row += 1
        self.agentsLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.agents.setLayout(self.agentsLayout)
    
    def add_agent(self, obj):
        #set obj to new json
        #self.clickableAgents[-1].position + 1
        new_box = ClickableFrame(obj, self.mainFrame, len(self.clickableAgents), self)
        self.clickableAgents.append(new_box)
        self.agentsLayout.addWidget(new_box, self.row, self.col)
        self.col += 1
        if self.col == 3:
            self.col = 0
            self.row += 1

    # def delete_agent(self, agent):
    #     #agent is the ClickableFrame widget
    #     del self.clickableAgents[agent.position]
    #     ind = 0
    #     for i in self.clickableAgents:
    #         i.position = ind
    #         ind = ind + 1
    #     self.agentsLayout.removeWidget(agent)
    #     self.parent().layout().removeWidget(agent)
    #     agent.deleteLater()
    #     return QFrame()

    def resetBorders(self, clicked_frame):
        # Reset borders of all clickable frames except the clicked frame
        for current in self.clickableAgents:
            if current != clicked_frame:
                current.clicked = False
                current.update()

    def loadAgents(self):
        file = open('./data/agents.json')
        data = json.load(file)
        agents = data['agents']
        return agents
        
    def refreshFrame(self):
        #not in use rn (bc of add_agent), but useful to keep around for retrieving a refreshed display of the json
        #for each clickable frame, delete (works without - may be redundant since clickable is child of panel so it deletes when panel deletes, but safer to delete than leave it hanging)
        for current in self.clickableAgents:
            current.setParent(None)  # Remove from layout
            current.deleteLater()  # Delete widget

        new_frame = AgentsPanel(parent=self.parent())
        self.mainFrame.editPanel.agentFrame = new_frame
        self.mainFrame.agentPanel = new_frame
        self.parent().layout().replaceWidget(self, new_frame)
        self.deleteLater()

#button class for a new agent
class AddAgentButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.clicked = False
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
        self.setText("Add Agent")
        self.setIcon(QIcon('./assets/AddAgentIcon.png'))
        self.setIconSize(QSize(48, 24))

    def mousePressEvent(self, event):
        print("Adding Agent Clicked")
        newAgent = {
            "id": '',
            "name": "",
            "description": "",
            "max_consecutive_auto_reply": 0,
            "default_auto_reply": "",
            "llm_config": {
                "model": "Mistral-7B Chat Int4",
                "base_url": "127.0.0.1:8081",
                "api_type": "openai",
                "api_key": "NULL"
            },
            "skills": [],
            "system_message": ""
        }

        # Update current agent, text, and borders 
        # if theres a better way to do this that would be great, but this is working well
        self.parent().parent().parent().parent().mainFrame.editPanel.currentAgent = newAgent
        self.parent().parent().parent().parent().mainFrame.editPanel.setFields(newAgent)
        self.parent().parent().parent().parent().mainFrame.editPanel.editLabel.setText("Build Your Agent")
        self.parent().parent().parent().parent().mainFrame.editPanel.createButton.setText("Create Agent")
        self.parent().parent().parent().parent().mainFrame.editPanel.deleteButton.hide()
        self.parent().parent().parent().parent().mainFrame.agentPanel.resetBorders(self)

#button box class for holding/selecting an agent
class ClickableFrame(QFrame):
    # acts as a button
    # note: we could implement multi-select functionality in the future for team creation?
    def __init__(self, currentAgent, widget, pos, parent=None):
        super().__init__(parent)
        self.agentPanel = parent
        self.position = pos
        self.widget = widget # Keeps track of associated AgentsFrame class

        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # import any information needed from the agent for editing
        self.agent = currentAgent #raw json information
        self.clicked = False #variable to keep tracked of click
        #self.setFixedWidth(190)
        self.setFixedHeight(200)
        self.setStyleSheet("""
            background-color: #464545;
            border-radius: 10;
        """)
        bold = QFont()
        bold.setBold(True)
        agentVBox = QVBoxLayout()
        self.name = currentAgent['name']
        self.description = currentAgent['description']
        self.system_message = currentAgent["system_message"]
        self.skills = currentAgent["skills"]
        self.nameLabel = QLabel(self.name)
        self.nameLabel.setFixedHeight(25)
        self.nameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.nameLabel.setFont(bold)
        self.descriptionLabel = QLabel(self.description)
        self.descriptionLabel.setWordWrap(True)
        self.systemMessageLabel = QLabel(self.system_message)

        # nameLine = QLabel()
        # nameLine.setStyleSheet("""
        #     background-color: #5E5E5E;
        #     border-radius: 0;
        # """)
        # nameLine.setFixedHeight(2)
        # agentVBox.addWidget(nameLine)
        descriptionLine = QLabel()
        descriptionLine.setStyleSheet("""
            background-color: #5E5E5E;
            border-radius: 0;
        """)
        descriptionLine.setFixedHeight(2)
        
        #self.skillsLabel = QLabel(self.skills[0])
        #self.skillsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        agentVBox.addWidget(self.nameLabel)
        agentVBox.addWidget(self.descriptionLabel)
        # agentVBox.addWidget(self.systemMessageLabel)
        agentVBox.addWidget(descriptionLine)
        # agentVBox.addWidget(systemMessageLabel)

        skillsText = QLabel("Functions:")
        agentVBox.addWidget(skillsText)
        for i in range(len(self.skills)):
            skillsLabel = QLabel(self.skills[i])
            skillsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            skillsLabel.setStyleSheet("""
                border: 1px solid white;
                padding-left: 2;
                padding-right: 2;
                border-radius: 5;
                font-size: 24;
            """)
            skillsLabel.setFixedHeight(25)
            agentVBox.addWidget(skillsLabel)
        #agentVBox.addWidget(self.skillsLabel)
        self.setLayout(agentVBox)

    def mousePressEvent(self, event):
        self.widget.editPanel.deselect_all_checkboxes()
        print(self.agent['name'] ,"Frame Clicked!")
        self.widget.agentPanel.resetBorders(self) #unmark the borders of the previously clicked agent
        self.clicked = not self.clicked
        if self.clicked:
            self.widget.editPanel.clickedAgent = self
            self.widget.editPanel.currentAgent = self.agent #self.widget.editPanel is AgentValues class
            self.widget.editPanel.setFields(self.agent)    
            self.widget.editPanel.update() 
            self.widget.editPanel.editLabel.setText("Edit Your Agent")
            self.widget.editPanel.createButton.setText("Edit Agent")
            self.widget.editPanel.deleteButton.show()

            for checkbox in self.widget.editPanel.checkboxes:
                if checkbox.text().strip() in self.skills:
                    checkbox.setChecked(True)

        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.clicked:
            painter = QPainter(self)
            color = QColor(117, 219, 233)  # From Figma
            pen = QPen(color, 3, Qt.PenStyle.SolidLine)
            pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)  # For rounded corners
            painter.setPen(pen)
            painter.drawRoundedRect(1, 1, self.width() - 2, self.height() - 2, 10, 10)  

    def refreshFrame(self, obj):
        #for editing agents, only replace the one agent box instead of the entire AgentsPanel
        new_box = ClickableFrame(obj, self.widget, self.position, self.agentPanel)
        self.agentPanel.clickableAgents[self.position] = new_box
        self.parent().layout().replaceWidget(self, new_box)
        self.deleteLater()

#right side panel for editing the selected or new agent
class AgentValues(QFrame):
    def __init__(self, frame):
        super().__init__()
        
        #agent panel (left side)
        self.agentFrame = frame.agentPanel 

        #Keep track of all skills checkboxes
        self.checkboxes = []
        self.clickedAgent = QFrame()
        self.currentAgent = {
            "id": '',
            "name": "",
            "description": "",
            "max_consecutive_auto_reply": 0,
            "default_auto_reply": "",
            "llm_config": {
                "model": "Mistral-7B Chat Int4",
                "base_url": "127.0.0.1:8081",
                "api_type": "openai",
                "api_key": "NULL"
            },
            "skills": [],
            "system_message": ""
        }

        self.editLabel = QLabel("Build Your Agent")
        # doesnt do anything
        # if isEdit:
        #     print('new agent')
        #     self.editLabel = QLabel("Build Your Agent")
        #     #can set placeholder values
        #     #ex. field_input.setPlaceholderText(fieldInput)
        # else:
        #     print(self.currentAgent['name'])
        #     self.editLabel = QLabel("Edit Your Agent")
        bold = QFont() #font for title
        bold.setBold(True)
        text_color = QColor(117, 219, 233)  # blue for field labels

        #lighter outer box
        editFrame = QFrame()
        editLayout = QVBoxLayout()
        
        self.editLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.editLabel.setFont(bold)
        editFrame.setStyleSheet("background-color: #5E5E5E; border-radius: 20;")
        editLayout.addWidget(self.editLabel)
        editLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #darker box
        contentBox = QFrame()
        contentLayout = QVBoxLayout()
        contentBox.setStyleSheet("""
                background-color: #464545;
                border-radius: 10;
            """)

        #text fields
        self.name_input = QLineEdit()
        self.name_input.setText(self.currentAgent['name'])
        self.name_input.setStyleSheet("QLineEdit { background-color: #5E5E5E; border-radius: 10px; padding: 5px; }")
        contentLayout.addWidget(self.alignTextEditFields("Role", self.name_input))
        self.descrip_input = QLineEdit()
        self.descrip_input.setText(self.currentAgent['description'])
        self.descrip_input.setStyleSheet("QLineEdit { background-color: #5E5E5E; border-radius: 10px; padding: 5px; }")
        contentLayout.addWidget(self.alignTextEditFields("Description", self.descrip_input))
        self.sys_input = QLineEdit()
        self.sys_input.setText(self.currentAgent['system_message'])
        self.sys_input.setStyleSheet("QLineEdit { background-color: #5E5E5E; border-radius: 10px; padding: 5px; }")
        contentLayout.addWidget(self.alignTextEditFields("System Message", self.sys_input))

        # LLM dropdown
        #add functionality for importing and saved LLMs
        LLM_label = self.setLabel('LLM')
        LLMcombobox = QComboBox()
        LLMcombobox.setStyleSheet("QComboBox { background-color: #5E5E5E; border-radius: 10px; padding: 5px; }")
        LLMcombobox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        #pull from models.json
        file = open('./data/models.json')
        data = json.load(file)
        models = data["models"]

        #pulls default models for new agent (add functionality for pulling from agents.json)
        for currentModel in models:
            LLMcombobox.addItem(currentModel['model'])

        importButton = QPushButton(
            text=" Import", icon=QIcon('./assets/Vector.png')
        )
        importButton.setFixedHeight(30)
        importButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        importButton.setStyleSheet('''
            QPushButton {
                border: 0px solid #ffffff;
                border-radius: 10px;
                padding: 5px;
                background-color: #5E5E5E;
                color: #ffffff;
                font: 12px;
            }

            QPushButton:hover {
                background-color: #111111;
            }

            QPushButton:pressed {
                background-color: #5E5E5E;
            }
        ''')

        box = QFrame()
        layout = QHBoxLayout()
        layout.addWidget(LLM_label)
        layout.addWidget(LLMcombobox)
        layout.addWidget(importButton)
        box.setLayout(layout)

        contentLayout.addWidget(box)

        # Max consec auto reply
        self.sliderValue = 0
        self.max_label = QLabel('Max. Consecutive Auto Reply: [' + str(self.sliderValue) + ']')
        self.max_label.setFixedWidth(220)
        self.max_label.setStyleSheet("""
            color: #75DBE9;
            font-weight: bold;
        """)
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        # Set slider properties
        self.slider.setRange(0, 8)  # Set the range of integers
        self.slider.setSingleStep(1)  # Set the step size to 1
        self.slider.setValue(self.currentAgent['max_consecutive_auto_reply'])      # Set initial value
        self.slider.setContentsMargins(0,100,0,0)
        self.slider.setFixedHeight(50)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)  # Display ticks above and below the slider handle
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.setTickInterval(1)  # Set the interval between tick values
        self.slider.valueChanged[int].connect(self.updateSlider)

        #slider.valueChanged.connect()
        contentLayout.addWidget(self.alignHorizontal(self.max_label, self.slider))

        #skills checkbox section
        widge = QWidget()
        scroll_area = QScrollArea(widge)
        scroll_area.setWidgetResizable(True)
        scroll_bar = scroll_area.verticalScrollBar()
        scroll_bar.setStyleSheet("QScrollBar:vertical { background: #5E5E5E; width: 14px;}")
        scroll_area.setStyleSheet("QScrollArea { margin-left: 20px; margin-right: 40px; max-height: 10em; max-width: 20em }")

        checkbox_widget = QWidget()
        checkbox_layout = QVBoxLayout(checkbox_widget)
        checkbox_layout.setContentsMargins(80, 0, 0, 0)

        #this is for new agents, add functionality for agent's specified skills
        #or just define default values when creating new_agent and ONLY pull from agent.json
        file = open('./data/functions.json')
        data = json.load(file)
        functions = data["functions"]

        for currentFunction in functions:
            checkbox = QCheckBox('   ' + currentFunction['name'])
            checkbox_layout.addWidget(checkbox)
            self.checkboxes.append(checkbox)
    
        select_all_button = QPushButton("Select All")
        select_all_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        select_all_button.setStyleSheet('''
            QPushButton {
                border: 0px solid #ffffff;
                border-radius: 10px;
                padding: 5px;
                background-color: #5E5E5E;
                color: #ffffff;
                font: 12px;
            }

            QPushButton:hover {
                background-color: #111111;
            }

            QPushButton:pressed {
                background-color: #5E5E5E;
            }
        ''')
        deselect_all_button = QPushButton("Deselect All")
        deselect_all_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        deselect_all_button.setStyleSheet('''
            QPushButton {
                border: 0px solid #ffffff;
                border-radius: 10px;
                padding: 5px;
                background-color: #5E5E5E;
                color: #ffffff;
                font: 12px;
            }

            QPushButton:hover {
                background-color: #111111;
            }

            QPushButton:pressed {
                background-color: #5E5E5E;
            }
        ''')

        select_all_button.clicked.connect(self.select_all_checkboxes)
        deselect_all_button.clicked.connect(self.deselect_all_checkboxes)
        allWidget = QWidget()
        allLayout = QHBoxLayout()
        allLayout.addWidget(select_all_button)
        allLayout.addWidget(deselect_all_button)
        allWidget.setLayout(allLayout)

        scroll_area.setWidget(checkbox_widget)
        skillsWidget = QWidget()
        skillLayout = QHBoxLayout()
        skillLabel = self.setLabel('Skills')
        #skillLabel.setContentsMargins(0,0,50,0)

        checksWidget = QWidget()
        checksWidget.setContentsMargins(0,0,125,0)
        checksLayout = QVBoxLayout()
        separateLine = QLabel()
        separateLine.setStyleSheet("""
            background-color: #5E5E5E;
            border-radius: 0;
        """)
        separateLine.setFixedHeight(2)
        checksLayout.addWidget(scroll_area)
        checksLayout.addWidget(separateLine)
        checksLayout.addWidget(allWidget)
        checksWidget.setLayout(checksLayout)
        skillLabel.setAlignment(Qt.AlignmentFlag.AlignTop)
        skillLayout.addWidget(skillLabel)
        skillLayout.addWidget(checksWidget)
        skillsWidget.setLayout(skillLayout)
        skillsWidget.setFixedHeight(250)
        contentLayout.addWidget(skillsWidget)

        self.deleteButton = QPushButton("Delete Agent")
        self.deleteButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.deleteButton.setFixedWidth(150)
        self.deleteButton.setFixedHeight(50)
        self.deleteButton.setStyleSheet("""
            padding: 5px;
            background-color: transparent;
            font: 15px;
            text-decoration: underline;
            color: #ffffff;
        """)
        self.deleteButton.clicked.connect(self.deleteClicked)
        self.deleteButton.hide()

        self.createButton = QPushButton(
            text=" Create Agent", icon=QIcon('./assets/Sparkling.png')
        )
        self.createButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.createButton.setFixedWidth(150)
        self.createButton.setFixedHeight(50)
        self.createButton.setStyleSheet('''
            QPushButton {
                border: 0px solid #ffffff;
                border-radius: 10px;
                padding: 5px;
                background-color: #5E5E5E;
                color: #75DBE9;
                font: 15px;
            }

            QPushButton:hover {
                background-color: #111111;
            }

            QPushButton:pressed {
                background-color: #5E5E5E;
            }
        ''')
        self.createButton.clicked.connect(self.createClicked)

        self.bottomButtonFrame = QFrame()
        self.bottomButtonBox = QHBoxLayout()

        self.bottomButtonBox.addWidget(self.deleteButton)
        self.bottomButtonBox.addWidget(self.createButton)
        self.bottomButtonFrame.setLayout(self.bottomButtonBox)

        contentLayout.addWidget(self.bottomButtonFrame, alignment=Qt.AlignmentFlag.AlignCenter)
        contentLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        contentBox.setLayout(contentLayout)

        editLayout.addWidget(contentBox)
        editLayout.setStretchFactor(contentBox, 1)
        self.setLayout(editLayout)

    def updateSlider(self, newValue):
        print("slider: " + str(newValue))
        self.sliderValue = newValue
        self.max_label.setText('Max. Consecutive Auto Reply: [' + str(self.sliderValue) + ']')

    def setFields(self, agent):
        self.name_input.setText(agent['name'])
        self.descrip_input.setText(agent['description'])
        self.sys_input.setText(agent['system_message'])
        self.slider.setValue(agent['max_consecutive_auto_reply'])     

    def createClicked(self):
        #upload new edits into json
        print('create clicked')
        file = open('./data/agents.json')
        data = json.load(file)
        filtered_agents = filter(lambda agent: agent.get('id') == self.currentAgent['id'], data.get('agents', []))

        found_agent = next(filtered_agents, None)

        selected_skills = []
        for checkbox in self.checkboxes:
            if checkbox.isChecked():
                selected_skills.append(checkbox.text().strip())
                checkbox.setChecked(False)

        self.currentAgent["skills"] = selected_skills

        if found_agent:
            #Update at agent id
            #add functionality for getting value from dropdown and check boxes (LLM and skills)
            print(self.name_input.text())
            found_agent['id'] = self.currentAgent['id'] 
            found_agent['name'] = self.name_input.text()
            found_agent['description'] = self.descrip_input.text()
            found_agent['max_consecutive_auto_reply'] = self.slider.value()
            if hasattr(self.currentAgent, 'default_auto_reply'):
                found_agent['default_auto_reply'] = self.currentAgent['default_auto_reply'] #have to check if json has these fields (threw error on first one)
            if hasattr(self.currentAgent, 'llm_config'):
                found_agent['llm_config'] = self.currentAgent['llm_config'] #same issue as above
            found_agent['skills'] = self.currentAgent['skills']
            found_agent['system_message'] = self.sys_input.text()
 
        else:
            #Create new agent
            print('new added')
            self.currentAgent['id'] = str(int(data.get('agents', [])[-1]['id']) + 1)  #add id functionality
            print(str(int(data.get('agents', [])[-1]['id'])))
            self.currentAgent['name'] = self.name_input.text()
            self.currentAgent['description'] = self.descrip_input.text()
            self.currentAgent['max_consecutive_auto_reply'] = self.slider.value()
            self.currentAgent['default_auto_reply'] = self.currentAgent['default_auto_reply'] #have to check if json has these fields (threw error on first one)
            self.currentAgent['llm_config'] = self.currentAgent['llm_config'] #same issue as above
            self.currentAgent['skills'] = selected_skills
            self.currentAgent['system_message'] = self.sys_input.text()
            data['agents'].append(self.currentAgent)

        with open('./data/agents.json', 'w') as file:
                # Write the updated data back to the file
                json.dump(data, file, indent=2)
        
        if found_agent:
            self.clickedAgent.refreshFrame(found_agent)
            self.clickedAgent = QFrame()
        else:
            self.agentFrame.add_agent(self.currentAgent)

        self.currentAgent = {
            "id": '',
            "name": "",
            "description": "",
            "max_consecutive_auto_reply": 0,
            "default_auto_reply": "",
            "llm_config": {
                "model": "Mistral-7B Chat Int4",
                "base_url": "127.0.0.1:8081",
                "api_type": "openai",
                "api_key": "NULL"
            },
            "skills": [],
            "system_message": ""
        }  
        self.setFields(self.currentAgent)
        self.editLabel.setText("Build Your Agent")
        self.createButton.setText("Create Agent")
        self.deleteButton.hide()
        self.update()

    def deleteClicked(self):
        dialog = DeleteDialog()
        dialog.exec()
        willDelete = dialog.willDelete
        print(willDelete)

        if willDelete:
            print('delete clicked')
            agentId = self.currentAgent["id"]

            file = open('./data/agents.json')
            data = json.load(file)
            # data['agents]
            updatedAgents = []
            for agent in data["agents"]:
                if agent["id"] != agentId:
                    updatedAgents.append(agent)
            data["agents"] = updatedAgents
            with open('./data/agents.json', 'w') as file:
                # Write the updated data back to the file
                json.dump(data, file, indent=2)

            # self.clickedAgent = self.agentFrame.delete_agent(self.clickedAgent)
            self.agentFrame.refreshFrame()
            self.currentAgent = {
                "id": '',
                "name": "",
                "description": "",
                "max_consecutive_auto_reply": 0,
                "default_auto_reply": "",
                "llm_config": {
                    "model": "Mistral-7B Chat Int4",
                    "base_url": "127.0.0.1:8081",
                    "api_type": "openai",
                    "api_key": "NULL"
                },
                "skills": [],
                "system_message": ""
            }  
            self.setFields(self.currentAgent)
            self.editLabel.setText("Build Your Agent")
            self.createButton.setText("Create Agent")
            self.deleteButton.hide()
            self.update()

    def select_all_checkboxes(self):
        for checkbox in self.checkboxes:
            checkbox.setChecked(True)

    def deselect_all_checkboxes(self):
        for checkbox in self.checkboxes:
            checkbox.setChecked(False)
  
    def alignTextEditFields(self, label, fieldInput):
        fieldLabel = self.setLabel(label)
        box = self.alignHorizontal(fieldLabel, fieldInput)
        return box
    
    def alignHorizontal(self, content1, content2):
        box = QFrame()
        layout = QHBoxLayout()
        layout.addWidget(content1)
        layout.addWidget(content2)
        box.setLayout(layout)
        return box
    
    def setLabel(self, label):
        bold = QFont() #font for title
        bold.setBold(True)
        text_color = QColor(117, 219, 233)  # blue for field labels

        fieldLabel = QLabel(label)
        fieldLabel.setFont(bold)
        fieldLabel.setStyleSheet(f"color: {text_color.name()};")
        fieldLabel.setFixedWidth(110)  # Set a fixed width for the label

        return fieldLabel

#skeleton of basic moving parts without visual display details to understand the code structure between classes

# class AgentsFrame(QFrame):
#     def __init__(self, parent=None):
#         super().__init__()

#         # for agents display on left panel
#         self.agentPanel = AgentsPanel(self)

#         #for changing contents of right panel
#         self.editPanel = AgentValues(self)



# #left side panel that holds one AddAgentButton and a ClickableFrame for each agent
# class AgentsPanel(QFrame):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         # Keep track of all agent boxes
#         self.mainFrame = parent #parent is the AgentsFrame class
#         self.clickableAgents = [] #tracks all the ClickableFrames it creates and displays

#         self.agentInfo = self.loadAgents()
#         self.agentBox(self.agentInfo)

#     def agentBox(self, list_of_agent_objects):
#         addButton = AddAgentButton() #call class for new agent button
#         
#         for currentAgent in list_of_agent_objects: #traverse the raw json agents
#             obj = currentAgent
#             agentBox = ClickableFrame(obj, self.mainFrame, ind, self) #display each raw json in a ClickableFrame
#             ind = ind + 1 #tracks the position of the ClickableFrame in the clickableAgents array - eventually used for replacing the ClickableFrame in clickableAgents that has been edited (seen in ClickableFrame's refreshFrame)
#             self.clickableAgents.append(agentBox) 
#             self.agentsLayout.addWidget(agentBox, row, col)

#     def loadAgents(self):
#         file = open('./data/agents.json')
#         data = json.load(file)
#         agents = data['agents']
#         return agents
        
#     def refreshFrame(self): #for refreshing AgentPanel class when adding or deleting an agent
#         #for each clickable frame, delete (works without - may be redundant since clickable is child of panel so it deletes when panel deletes, but safer to delete than leave it hanging)
#         #clear out children ClickableFrames
#         for current in self.clickableAgents:
#             current.setParent(None)  # Remove from layout
#             current.deleteLater()  # Delete widget

#         new_frame = AgentsPanel(parent=self.parent()) #create new panel
#         self.mainFrame.editPanel.agentFrame = new_frame #replace panel in all associated connections
#         self.mainFrame.agentPanel = new_frame #same as above
#         self.parent().layout().replaceWidget(self, new_frame) #replace panel in mainframe (AgentsFrame)
#         self.deleteLater() #delete old frame

# #button class for a new agent
# class AddAgentButton(QPushButton):
#     def __init__(self):
#         super().__init__()


# #button box class for holding/selecting an agent
# class ClickableFrame(QFrame):
#     # acts as a button
#     # note: we could implement multi-select functionality in the future for team creation?
#     def __init__(self, currentAgent, widget, pos, parent=None):
#         super().__init__(parent)
#         self.agentPanel = parent
#         self.position = pos
#         self.widget = widget # Keeps track of associated AgentsFrame class
#         self.agent = currentAgent #raw json information
#         self.clicked = False #variable to keep tracked of click

#     def mousePressEvent(self, event):
#         self.clicked = not self.clicked
#         if self.clicked:
#             self.widget.editPanel.update() #make right side editing panel match the chosen clicked agent
#         self.update()

#     def refreshFrame(self, obj):
#         #for editing agents, only replace the one agent box instead of the entire AgentsPanel
#         new_box = ClickableFrame(obj, self.widget, self.position, self.agentPanel)

# #right side panel for editing the selected or new agent
# class AgentValues(QFrame):
#     def __init__(self, frame):
#         super().__init__()

#         #agent panel (left side)
#         self.agentFrame = frame.agentPanel 
#         
#         #button for saving edits
#         createButton = QPushButton(
#             text=" Create Agent", icon=QIcon('./assets/Sparkling.png')
#         )
#        
#         createButton.clicked.connect(self.createClicked) 

#     def createClicked(self):
#         file = open('./data/agents.json')
#         data = json.load(file)
#         filtered_agents = filter(lambda agent: agent.get('id') == self.currentAgent['id'], data.get('agents', []))

#         found_agent = next(filtered_agents, None)

#         if found_agent:
#             #Update raw json at agent id
#             found_agent['id'] = self.currentAgent['id'] 
#             found_agent['name'] = self.name_input.text()
#             found_agent['description'] = self.descrip_input.text()
#             found_agent['max_consecutive_auto_reply'] = self.slider.value()
#             found_agent['default_auto_reply'] = self.currentAgent['default_auto_reply'] #have to check if json has these fields (threw error on first one)
#             found_agent['llm_config'] = self.currentAgent['llm_config'] #same issue as above
#             found_agent['skills'] = self.currentAgent['skills']
#             found_agent['system_message'] = self.sys_input.text()
 
#         else:
#             #Create new agent to be added to raw json
#             self.currentAgent['id'] = str(int(self.agentFrame.agentInfo[-1]['id']) + 1)  #add id functionality
#             self.currentAgent['name'] = self.name_input.text()
#             self.currentAgent['description'] = self.descrip_input.text()
#             self.currentAgent['max_consecutive_auto_reply'] = self.slider.value()
#             self.currentAgent['default_auto_reply'] = self.currentAgent['default_auto_reply'] #have to check if json has these fields (threw error on first one)
#             self.currentAgent['llm_config'] = self.currentAgent['llm_config'] #same issue as above
#             self.currentAgent['skills'] = self.currentAgent['skills']
#             self.currentAgent['system_message'] = self.sys_input.text()
#             data['agents'].append(self.currentAgent)

#         with open('./data/agents.json', 'w') as file:
#                 # Write the updated data back to the file
#                 json.dump(data, file, indent=2)
        
#         if found_agent: #if agent exists, only update it's ClickableFrame
#             self.clickedAgent.refreshFrame(found_agent)
#             self.clickedAgent = QFrame()
#         else: #if brand new agent, update whole AgentPanel
#             self.agentFrame.refreshFrame()