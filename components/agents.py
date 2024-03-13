from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import json

class ClickableFrame(QFrame):
    # acts as a button
    # note: we could implement multi-select functionality in the future for team creation?
    def __init__(self, currentAgent, widget):
        super().__init__()

        self.widget = widget # Keeps track of associated AgentsFrame class

        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # import any information needed from the agent for editing
        self.agent = currentAgent #raw json information
        self.clicked = False #variable to keep tracked of click
        self.setFixedWidth(190)
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
        self.nameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.nameLabel.setFont(bold)
        self.descriptionLabel = QLabel(self.description)
        self.systemMessageLabel = QLabel(self.system_message)
        #self.skillsLabel = QLabel(self.skills[0])
        #self.skillsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        agentVBox.addWidget(self.nameLabel)
        agentVBox.addWidget(self.descriptionLabel)
        agentVBox.addWidget(self.systemMessageLabel)
        #agentVBox.addWidget(self.skillsLabel)
        self.setLayout(agentVBox)

    def mousePressEvent(self, event):
        print(self.agent['name'] ,"Frame Clicked!")
        self.widget.agentPanel.resetBorders(self) #unmark the borders of the previously clicked agent
        self.clicked = not self.clicked
        self.widget.editPanel.currentAgent = self.agent #self.widget.editPanel is AgentValues class
        self.widget.editPanel.name_input.setText(self.agent['name'])
        self.widget.editPanel.descrip_input.setText(self.agent['description'])
        self.widget.editPanel.sys_input.setText(self.agent['system_message'])
        self.widget.editPanel.slider.setValue(self.agent['max_consecutive_auto_reply'])     
        self.widget.editPanel.update() # = AgentValues(self.agent).buildAgent() #change the right panel to reflect the current agent
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

class AgentValues(QFrame):
    def __init__(self, frame):
        super().__init__()

        #parent frame
        self.agentFrame = frame.agentPanel 

        #Keep track of all skills checkboxes
        self.checkboxes = []
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

        if self.currentAgent['name'] == '':
            print('new agent')
            editLabel = QLabel("Build Your Agent")
            #can set placeholder values
            #ex. field_input.setPlaceholderText(fieldInput)
        else:
            print(self.currentAgent['name'])
            editLabel = QLabel("Edit Your Agent")
        bold = QFont() #font for title
        bold.setBold(True)
        text_color = QColor(117, 219, 233)  # blue for field labels

        #lighter outer box
        editFrame = QFrame()
        editLayout = QVBoxLayout()
        
        editLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        editLabel.setFont(bold)
        editFrame.setStyleSheet("background-color: #5E5E5E; border-radius: 20;")
        editLayout.addWidget(editLabel)
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
        #importButton.setFixedWidth(0)
        importButton.setFixedHeight(30)
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
                background-color: #ffffff;
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
        max_label = self.setLabel('Max. Consecutive Auto Reply')
        max_label.setFixedWidth(200)
        self.slider = QSlider(Qt.Orientation.Horizontal)
        
        # Set slider properties
        self.slider.setRange(0, 8)  # Set the range of integers
        self.slider.setSingleStep(1)  # Set the step size to 1
        self.slider.setValue(self.currentAgent['max_consecutive_auto_reply'])      # Set initial value
        self.slider.setContentsMargins(0,100,0,0)
        self.slider.setFixedHeight(50)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)  # Display ticks above and below the slider handle
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.setTickInterval(1)  # Set the interval between tick values
    
        #slider.valueChanged.connect()
        contentLayout.addWidget(self.alignHorizontal(max_label, self.slider))

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
                background-color: #ffffff;
            }

            QPushButton:pressed {
                background-color: #5E5E5E;
            }
        ''')
        deselect_all_button = QPushButton("Deselect All")
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
                background-color: #ffffff;
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

        createButton = QPushButton(
            text=" Create Agent", icon=QIcon('./assets/Sparkling.png')
        )
        createButton.setFixedWidth(150)
        createButton.setFixedHeight(50)
        createButton.setStyleSheet('''
            QPushButton {
                border: 0px solid #ffffff;
                border-radius: 10px;
                padding: 5px;
                background-color: #5E5E5E;
                color: #75DBE9;
                font: 15px;
            }

            QPushButton:hover {
                background-color: #ffffff;
            }

            QPushButton:pressed {
                background-color: #5E5E5E;
            }
        ''')
        createButton.clicked.connect(self.createClicked)
        contentLayout.addWidget(createButton, alignment=Qt.AlignmentFlag.AlignCenter)
        contentLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        contentBox.setLayout(contentLayout)

        editLayout.addWidget(contentBox)
        editLayout.setStretchFactor(contentBox, 1)
        #editFrame.setLayout(editLayout)
        self.setLayout(editLayout)

    def createClicked(self):
        #upload new edits into json
        print('create clicked')
        file = open('./data/agents.json')
        data = json.load(file)
        filtered_agents = filter(lambda agent: agent.get('id') == self.currentAgent['id'], data.get('agents', []))

        found_agent = next(filtered_agents, None)

        if found_agent:
            #Update at agent id
            #add functionality for getting value from dropdown and check boxes (LLM and skills)
            print(self.name_input.text())
            found_agent['id'] = self.currentAgent['id'] 
            found_agent['name'] = self.name_input.text()
            found_agent['description'] = self.descrip_input.text()
            found_agent['max_consecutive_auto_reply'] = self.slider.value()
            found_agent['default_auto_reply'] = self.currentAgent['default_auto_reply'] #have to check if json has these fields (threw error on first one)
            found_agent['llm_config'] = self.currentAgent['llm_config'] #same issue as above
            found_agent['skills'] = self.currentAgent['skills']
            found_agent['system_message'] = self.sys_input.text()
 
        else:
            #Create new agent
            print('new added')
            self.currentAgent['id'] = str(int(self.agentFrame.agentInfo[-1]['id']) + 1)  #add id functionality
            self.currentAgent['name'] = self.name_input.text()
            self.currentAgent['description'] = self.descrip_input.text()
            self.currentAgent['max_consecutive_auto_reply'] = self.slider.value()
            self.currentAgent['default_auto_reply'] = self.currentAgent['default_auto_reply'] #have to check if json has these fields (threw error on first one)
            self.currentAgent['llm_config'] = self.currentAgent['llm_config'] #same issue as above
            self.currentAgent['skills'] = self.currentAgent['skills']
            self.currentAgent['system_message'] = self.sys_input.text()
            data['agents'].append(self.currentAgent)

        with open('./data/agents.json', 'w') as file:
                # Write the updated data back to the file
                json.dump(data, file, indent=2)
        #call for a new AgentsFrame QFrame
        self.agentFrame.refreshFrame()

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

class AgentsPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Keep track of all agent boxes
        self.mainFrame = parent
        self.clickableAgents = []
        self.clickedAgent = QFrame()
        self.setStyleSheet("background-color: #5E5E5E; border-radius: 20;")
        self.viewVBox = QVBoxLayout()
        self.agentsLabel = QLabel()
        bold = QFont()
        bold.setBold(True)
        self.agentsLabel = QLabel('Agents')
        self.agentsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.agentsLabel.setFont(bold)

        # Scroll section
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

        row, col = 1, 0
        for currentAgent in list_of_agent_objects:
            obj = currentAgent
            agentBox = ClickableFrame(obj, self.mainFrame)
            self.clickableAgents.append(agentBox)
            self.agentsLayout.addWidget(agentBox, row, col)
            col += 1
            if col == 3:
                col = 0
                row += 1
        self.agentsLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.agents.setLayout(self.agentsLayout)
    
    def add_agent(self):
        #set obj to new json
        new_box = ClickableFrame(obj, self.mainFrame)
        self.widgets.append(new_box)
        self.layout().insertWidget(len(self.clickableAgents) - 1, new_box)

    def resetBorders(self, clicked_frame):
        # Reset borders of all clickable frames except the clicked frame
        # causes error bc we must update self.clickableAgents when refreshClickable frame
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
        # for each clickable frame, delete
        # for current in self.clickableAgents:
        #     current.setParent(None)  # Remove from layout
        #     current.deleteLater()  # Delete widget
        new_frame = AgentsPanel(parent=self.parent())
        self.mainFrame.editPanel.agentFrame = new_frame
        self.mainFrame.agentPanel = new_frame
        self.parent().layout().replaceWidget(self, new_frame)
        self.deleteLater()


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

    # @pyqtSlot(str)
    # def updateParent(self, new_value):
    #     # Update the parent widget based on the new value
    #     self.label.setText("Value in Parent Widget: " + new_value)
    
# from PyQt6.QtWidgets import *
# from PyQt6.QtGui import *
# from PyQt6.QtCore import *
# import json

# class ClickableFrame(QFrame):
#     # acts as a button
#     # note: we could implement multi-select functionality in the future for team creation?
#     def __init__(self, currentAgent, mainFrame):
#         super().__init__()

#         self.mainFrame = panel # Keeps track of associated AgentsPanel class

#         self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
#         self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

#         # import any information needed from the agent for editing
#         self.agent = currentAgent #raw json information
#         self.clicked = False #variable to keep tracked of click
#         self.setFixedWidth(190)
#         self.setFixedHeight(200)
#         self.setStyleSheet("""
#             background-color: #464545;
#             border-radius: 10;
#         """)
#         bold = QFont()
#         bold.setBold(True)
#         agentVBox = QVBoxLayout()
#         self.name = currentAgent['name']
#         self.description = currentAgent['description']
#         self.system_message = currentAgent["system_message"]
#         self.skills = currentAgent["skills"]
#         self.nameLabel = QLabel(self.name)
#         self.nameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.nameLabel.setFont(bold)
#         self.descriptionLabel = QLabel(self.description)
#         self.systemMessageLabel = QLabel(self.system_message)
#         #self.skillsLabel = QLabel(self.skills[0])
#         #self.skillsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         agentVBox.addWidget(self.nameLabel)
#         agentVBox.addWidget(self.descriptionLabel)
#         agentVBox.addWidget(self.systemMessageLabel)
#         #agentVBox.addWidget(self.skillsLabel)
#         self.setLayout(agentVBox)

#     def mousePressEvent(self, event):
#         print(self.agent['name'] ,"Frame Clicked!")
#         self.agentPanel.resetBorders(self) #unmark the borders of the previously clicked agent
#         self.clicked = not self.clicked
#         self.mainFrame.editPanel.currentAgent = self.agent #self.widget.editPanel is AgentValues class
#         self.mainFrame.editPanel.currentClickable = self #for updating UI after edited
#         self.mainFrame.editPanel.name_input.setText(self.agent['name'])
#         self.mainFrame.editPanel.descrip_input.setText(self.agent['description'])
#         self.mainFrame.editPanel.sys_input.setText(self.agent['system_message'])
#         self.mainFrame.editPanel.slider.setValue(self.agent['max_consecutive_auto_reply'])     
#         # self.widget.editPanel.update() # = AgentValues(self.agent).buildAgent() #change the right panel to reflect the current agent
#         # self.update()

#     def paintEvent(self, event):
#         super().paintEvent(event)
#         if self.clicked:
#             painter = QPainter(self)
#             color = QColor(117, 219, 233)  # From Figma
#             pen = QPen(color, 3, Qt.PenStyle.SolidLine)
#             pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)  # For rounded corners
#             painter.setPen(pen)
#             painter.drawRoundedRect(1, 1, self.width() - 2, self.height() - 2, 10, 10)  
    
#     def refreshFrame(self, currentAgent, widget):
#         #replacing only a single agent on edit agent
#         new_frame = ClickableFrame(currentAgent, widget, parent=self.parent())
#         self.parent().layout().replaceWidget(self, new_frame)
#         self.deleteLater()
#         # self.widget.clickableAgents

# class AgentValues(QFrame):
#     def __init__(self, parent):
#         super().__init__()

#         #parent frame
#         self.agentFrame = parent
#         self.currentClickable = QFrame()

#         #Keep track of all skills checkboxes
#         self.checkboxes = []
#         self.currentAgent = {
#             "id": '',
#             "name": "",
#             "description": "",
#             "max_consecutive_auto_reply": 0,
#             "default_auto_reply": "",
#             "llm_config": {
#                 "model": "Mistral-7B Chat Int4",
#                 "base_url": "127.0.0.1:8081",
#                 "api_type": "openai",
#                 "api_key": "NULL"
#             },
#             "skills": [],
#             "system_message": ""
#         }

#         if self.currentAgent['name'] == '':
#             print('new agent')
#             editLabel = QLabel("Build Your Agent")
#             #can set placeholder values
#             #ex. field_input.setPlaceholderText(fieldInput)
#         else:
#             print(self.currentAgent['name'])
#             editLabel = QLabel("Edit Your Agent")
#         bold = QFont() #font for title
#         bold.setBold(True)
#         text_color = QColor(117, 219, 233)  # blue for field labels

#         #lighter outer box
#         editFrame = QFrame()
#         editLayout = QVBoxLayout()
        
#         editLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         editLabel.setFont(bold)
#         editFrame.setStyleSheet("background-color: #5E5E5E; border-radius: 20;")
#         editLayout.addWidget(editLabel)
#         editLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

#         #darker box
#         contentBox = QFrame()
#         contentLayout = QVBoxLayout()
#         contentBox.setStyleSheet("""
#                 background-color: #464545;
#                 border-radius: 10;
#             """)

#         #text fields
#         self.name_input = QLineEdit()
#         self.name_input.setText(self.currentAgent['name'])
#         self.name_input.setStyleSheet("QLineEdit { background-color: #5E5E5E; border-radius: 10px; padding: 5px; }")
#         contentLayout.addWidget(self.alignTextEditFields("Role", self.name_input))
#         self.descrip_input = QLineEdit()
#         self.descrip_input.setText(self.currentAgent['description'])
#         self.descrip_input.setStyleSheet("QLineEdit { background-color: #5E5E5E; border-radius: 10px; padding: 5px; }")
#         contentLayout.addWidget(self.alignTextEditFields("Description", self.descrip_input))
#         self.sys_input = QLineEdit()
#         self.sys_input.setText(self.currentAgent['system_message'])
#         self.sys_input.setStyleSheet("QLineEdit { background-color: #5E5E5E; border-radius: 10px; padding: 5px; }")
#         contentLayout.addWidget(self.alignTextEditFields("System Message", self.sys_input))

#         # LLM dropdown
#         #add functionality for importing and saved LLMs
#         LLM_label = self.setLabel('LLM')
#         LLMcombobox = QComboBox()
#         LLMcombobox.setStyleSheet("QComboBox { background-color: #5E5E5E; border-radius: 10px; padding: 5px; }")
        
#         #pull from models.json
#         file = open('./data/models.json')
#         data = json.load(file)
#         models = data["models"]

#         #pulls default models for new agent (add functionality for pulling from agents.json)
#         for currentModel in models:
#             LLMcombobox.addItem(currentModel['model'])

#         importButton = QPushButton(
#             text=" Import", icon=QIcon('./assets/Vector.png')
#         )
#         #importButton.setFixedWidth(0)
#         importButton.setFixedHeight(30)
#         importButton.setStyleSheet('''
#             QPushButton {
#                 border: 0px solid #ffffff;
#                 border-radius: 10px;
#                 padding: 5px;
#                 background-color: #5E5E5E;
#                 color: #ffffff;
#                 font: 12px;
#             }

#             QPushButton:hover {
#                 background-color: #ffffff;
#             }

#             QPushButton:pressed {
#                 background-color: #5E5E5E;
#             }
#         ''')

#         box = QFrame()
#         layout = QHBoxLayout()
#         layout.addWidget(LLM_label)
#         layout.addWidget(LLMcombobox)
#         layout.addWidget(importButton)
#         box.setLayout(layout)

#         contentLayout.addWidget(box)

#         # Max consec auto reply
#         max_label = self.setLabel('Max. Consecutive Auto Reply')
#         max_label.setFixedWidth(200)
#         self.slider = QSlider(Qt.Orientation.Horizontal)
        
#         # Set slider properties
#         self.slider.setRange(0, 8)  # Set the range of integers
#         self.slider.setSingleStep(1)  # Set the step size to 1
#         self.slider.setValue(self.currentAgent['max_consecutive_auto_reply'])      # Set initial value
#         self.slider.setContentsMargins(0,100,0,0)
#         self.slider.setFixedHeight(50)
#         self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)  # Display ticks above and below the slider handle
#         self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
#         self.slider.setTickInterval(1)  # Set the interval between tick values
    
#         #slider.valueChanged.connect()
#         contentLayout.addWidget(self.alignHorizontal(max_label, self.slider))

#         #skills checkbox section
#         widge = QWidget()
#         scroll_area = QScrollArea(widge)
#         scroll_area.setWidgetResizable(True)
#         scroll_bar = scroll_area.verticalScrollBar()
#         scroll_bar.setStyleSheet("QScrollBar:vertical { background: #5E5E5E; width: 14px;}")
#         scroll_area.setStyleSheet("QScrollArea { margin-left: 20px; margin-right: 40px; max-height: 10em; max-width: 20em }")

#         checkbox_widget = QWidget()
#         checkbox_layout = QVBoxLayout(checkbox_widget)
#         checkbox_layout.setContentsMargins(80, 0, 0, 0)

#         #this is for new agents, add functionality for agent's specified skills
#         #or just define default values when creating new_agent and ONLY pull from agent.json
#         file = open('./data/functions.json')
#         data = json.load(file)
#         functions = data["functions"]

#         for currentFunction in functions:
#             checkbox = QCheckBox('   ' + currentFunction['name'])
#             checkbox_layout.addWidget(checkbox)
#             self.checkboxes.append(checkbox)
    
#         select_all_button = QPushButton("Select All")
#         select_all_button.setStyleSheet('''
#             QPushButton {
#                 border: 0px solid #ffffff;
#                 border-radius: 10px;
#                 padding: 5px;
#                 background-color: #5E5E5E;
#                 color: #ffffff;
#                 font: 12px;
#             }

#             QPushButton:hover {
#                 background-color: #ffffff;
#             }

#             QPushButton:pressed {
#                 background-color: #5E5E5E;
#             }
#         ''')
#         deselect_all_button = QPushButton("Deselect All")
#         deselect_all_button.setStyleSheet('''
#             QPushButton {
#                 border: 0px solid #ffffff;
#                 border-radius: 10px;
#                 padding: 5px;
#                 background-color: #5E5E5E;
#                 color: #ffffff;
#                 font: 12px;
#             }

#             QPushButton:hover {
#                 background-color: #ffffff;
#             }

#             QPushButton:pressed {
#                 background-color: #5E5E5E;
#             }
#         ''')

#         select_all_button.clicked.connect(self.select_all_checkboxes)
#         deselect_all_button.clicked.connect(self.deselect_all_checkboxes)
#         allWidget = QWidget()
#         allLayout = QHBoxLayout()
#         allLayout.addWidget(select_all_button)
#         allLayout.addWidget(deselect_all_button)
#         allWidget.setLayout(allLayout)

#         scroll_area.setWidget(checkbox_widget)
#         skillsWidget = QWidget()
#         skillLayout = QHBoxLayout()
#         skillLabel = self.setLabel('Skills')
#         #skillLabel.setContentsMargins(0,0,50,0)

#         checksWidget = QWidget()
#         checksWidget.setContentsMargins(0,0,125,0)
#         checksLayout = QVBoxLayout()
#         separateLine = QLabel()
#         separateLine.setStyleSheet("""
#             background-color: #5E5E5E;
#             border-radius: 0;
#         """)
#         separateLine.setFixedHeight(2)
#         checksLayout.addWidget(scroll_area)
#         checksLayout.addWidget(separateLine)
#         checksLayout.addWidget(allWidget)
#         checksWidget.setLayout(checksLayout)
#         skillLabel.setAlignment(Qt.AlignmentFlag.AlignTop)
#         skillLayout.addWidget(skillLabel)
#         skillLayout.addWidget(checksWidget)
#         skillsWidget.setLayout(skillLayout)
#         skillsWidget.setFixedHeight(250)
#         contentLayout.addWidget(skillsWidget)

#         createButton = QPushButton(
#             text=" Create Agent", icon=QIcon('./assets/Sparkling.png')
#         )
#         createButton.setFixedWidth(150)
#         createButton.setFixedHeight(50)
#         createButton.setStyleSheet('''
#             QPushButton {
#                 border: 0px solid #ffffff;
#                 border-radius: 10px;
#                 padding: 5px;
#                 background-color: #5E5E5E;
#                 color: #75DBE9;
#                 font: 15px;
#             }

#             QPushButton:hover {
#                 background-color: #ffffff;
#             }

#             QPushButton:pressed {
#                 background-color: #5E5E5E;
#             }
#         ''')
#         createButton.clicked.connect(self.createClicked)
#         contentLayout.addWidget(createButton, alignment=Qt.AlignmentFlag.AlignCenter)
#         contentLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
#         contentBox.setLayout(contentLayout)

#         editLayout.addWidget(contentBox)
#         editLayout.setStretchFactor(contentBox, 1)
#         #editFrame.setLayout(editLayout)
#         self.setLayout(editLayout)

#     def createClicked(self):
#         #upload new edits into json
#         print('create clicked')
#         file = open('./data/agents.json')
#         data = json.load(file)
#         filtered_agents = filter(lambda agent: agent.get('id') == self.currentAgent['id'], data.get('agents', []))

#         found_agent = next(filtered_agents, None)

#         if found_agent:
#             #Update at agent id
#             #add functionality for getting value from dropdown and check boxes (LLM and skills)
#             print(self.name_input.text())
#             found_agent['id'] = self.currentAgent['id'] 
#             found_agent['name'] = self.name_input.text()
#             found_agent['description'] = self.descrip_input.text()
#             found_agent['max_consecutive_auto_reply'] = self.slider.value()
#             found_agent['default_auto_reply'] = self.currentAgent['default_auto_reply'] #have to check if json has these fields (threw error on first one)
#             found_agent['llm_config'] = self.currentAgent['llm_config'] #same issue as above
#             found_agent['skills'] = self.currentAgent['skills']
#             found_agent['system_message'] = self.sys_input.text()
 
#         else:
#             #Create new agent
#             print('new added')
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
#                 #implement check if json dump successful here
        
#         if found_agent:
#             #replace only clickable frame (agent button)
#             print('clickable replaced')
#             self.currentClickable.refreshFrame(found_agent, self.agentFrame)
#         else:
#             #call for a new AgentsFrame QFrame
#             self.agentFrame.refreshFrame()

#     def select_all_checkboxes(self):
#         for checkbox in self.checkboxes:
#             checkbox.setChecked(True)

#     def deselect_all_checkboxes(self):
#         for checkbox in self.checkboxes:
#             checkbox.setChecked(False)
  
#     def alignTextEditFields(self, label, fieldInput):
#         fieldLabel = self.setLabel(label)
#         box = self.alignHorizontal(fieldLabel, fieldInput)
#         return box
    
#     def alignHorizontal(self, content1, content2):
#         box = QFrame()
#         layout = QHBoxLayout()
#         layout.addWidget(content1)
#         layout.addWidget(content2)
#         box.setLayout(layout)
#         return box
    
#     def setLabel(self, label):
#         bold = QFont() #font for title
#         bold.setBold(True)
#         text_color = QColor(117, 219, 233)  # blue for field labels

#         fieldLabel = QLabel(label)
#         fieldLabel.setFont(bold)
#         fieldLabel.setStyleSheet(f"color: {text_color.name()};")
#         fieldLabel.setFixedWidth(110)  # Set a fixed width for the label

#         return fieldLabel

# class AgentsPanel(QFrame):
#     def __init__(self, parent):
#         super().__init__()
#         # Keep track of all agent boxes
#         self.mainFrame = parent
#         self.clickableAgents = []
#         self.clickedAgent = QFrame()
#         self.setStyleSheet("background-color: #5E5E5E; border-radius: 20;")
#         self.viewVBox = QVBoxLayout()
#         self.agentsLabel = QLabel()
#         bold = QFont()
#         bold.setBold(True)
#         self.agentsLabel = QLabel('Agents')
#         self.agentsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.agentsLabel.setFont(bold)

#         # Scroll section
#         self.agents = QFrame()
#         self.agentsLayout = QGridLayout()
#         self.agentInfo = self.loadAgents()
#         self.agentBox(self.agentInfo)
#         self.agentScroll = QScrollArea()
#         self.agentScroll.setWidgetResizable(True)
#         self.agentScroll.setWidget(self.agents)
#         self.agentScroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
#         self.agentScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

#         # Embed scroll into view agents section
#         self.viewVBox.addWidget(self.agentScroll)
#         self.setLayout(self.viewVBox)

#     def agentBox(self, list_of_agent_objects):
#         self.agents.setStyleSheet("background-color: #5E5E5E; border-radius: 20;")
#         self.agentsLayout.addWidget(self.agentsLabel, 0, 0, 1, 3)  # Span label across 3 columns

#         row, col = 1, 0
#         for currentAgent in list_of_agent_objects:
#             obj = currentAgent
#             agentBox = ClickableFrame(obj, self.mainFrame)
#             self.clickableAgents.append(agentBox)
#             self.agentsLayout.addWidget(agentBox, row, col)
#             col += 1
#             if col == 3:
#                 col = 0
#                 row += 1
#         self.agentsLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
#         self.agents.setLayout(self.agentsLayout)
    
#     def add_agent(self):
#         #set obj to new json
#         new_box = ClickableFrame(obj, self.mainFrame)
#         self.widgets.append(new_box)
#         self.layout().insertWidget(len(self.clickableAgents) - 1, new_box)

#     def resetBorders(self, clicked_frame):
#         # Reset borders of all clickable frames except the clicked frame
#         # causes error bc we must update self.clickableAgents when refreshClickable frame
#         for current in self.clickableAgents:
#             if current != clicked_frame:
#                 current.clicked = False
#                 current.update()

#     def loadAgents(self):
#         file = open('./data/agents.json')
#         data = json.load(file)
#         agents = data['agents']
#         return agents
    
#     def refreshFrame(self):
#         new_frame = AgentsPanel(parent=self.parent())

#         self.parent().layout().replaceWidget(self, new_frame)
#         self.deleteLater()


# class AgentsFrame(QFrame):
#     def __init__(self, parent=None):
#         super().__init__()

#         # for agents display on left panel
#         self.agentPanel = AgentsPanel(self)

#         #for changing contents of right panel
#         self.editPanel = AgentValues(self)
        
#         # Set tab style
#         self.setStyleSheet("background-color: #464545; border-radius: 20;")
#         self.mainhbox = QHBoxLayout()

#         self.mainhbox.addWidget(self.agentPanel)
#         self.mainhbox.addWidget(self.editPanel)

#         self.mainhbox.setStretchFactor(self.agentPanel, 1) #equally sized left and right panels
#         self.mainhbox.setStretchFactor(self.editPanel, 1)
#         self.setLayout(self.mainhbox)