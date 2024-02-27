from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import json

class ClickableFrame(QFrame):
    # acts as a button
    # note: we could implement multi-select functionality in the future for team creation?
    def __init__(self, currentAgent, widget):
        super().__init__()

        self.widget = widget # Keeps track of associated Agents class

        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # import any information needed from the agent for editing
        self.agent = currentAgent #raw json information
        self.name = currentAgent['name']
        self.description = currentAgent['description']
        self.system_message = currentAgent['system_message']
        self.skills = currentAgent['skills']

        self.clicked = False #variable to keep tracked of click

    def mousePressEvent(self, event):
        print(self.name ,"Frame Clicked!")
        self.widget.resetBorders(self) #unmark the borders of the previously clicked agent
        self.widget.editAgent(self.agent) #change the right panel to match the clicked agent's json info
        self.clicked = not self.clicked
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


class AgentsFrame(QFrame):
    def __init__(self):
        super().__init__()

        # Keep track of all agent boxes
        self.allBoxes = []

        #Keep track of all checkboxes
        self.checkboxes = []

        # Set tab style
        self.setStyleSheet("background-color: #464545; border-radius: 20;")
        mainhbox = QHBoxLayout()

        # Fixed frame to embed the scroll section in
        viewFrame = QFrame()
        viewFrame.setStyleSheet("background-color: #5E5E5E; border-radius: 20;")
        viewVBox = QVBoxLayout()

        # Scroll section
        agents = self.loadAgents()
        agentScroll = QScrollArea()
        agentScroll.setWidgetResizable(True)
        agentScroll.setWidget(agents)
        agentScroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        agentScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # Embed scroll into view agents section
        viewVBox.addWidget(agentScroll)
        viewFrame.setLayout(viewVBox)
       
        agentsBuildFrame = self.buildAgent() #initialize right panel to build a new agent

        mainhbox.addWidget(viewFrame)
        mainhbox.addWidget(agentsBuildFrame)

        mainhbox.setStretchFactor(viewFrame, 1) #equally sized left and right panels
        mainhbox.setStretchFactor(agentsBuildFrame, 1)
        self.setLayout(mainhbox)
        

    def agentBox(self, list_of_agent_objects):
        bold = QFont()
        bold.setBold(True)

        agentsFrame = QFrame()
        agentsLayout = QGridLayout()
        agentsLabel = QLabel("Agents")
        agentsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        agentsLabel.setFont(bold)
        agentsFrame.setStyleSheet("background-color: #5E5E5E; border-radius: 20;")
        agentsLayout.addWidget(agentsLabel, 0, 0, 1, 3)  # Span label across 3 columns

        row, col = 1, 0
        for currentAgent in list_of_agent_objects:
            obj = currentAgent
            #print(obj)
            agentBox = ClickableFrame(obj, self)
            agentBox.setFixedWidth(190)
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
            nameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            nameLabel.setFont(bold)
            descriptionLabel = QLabel(description)
            systemMessageLabel = QLabel(system_message)
            skillsLabel = QLabel(skills[0])
            skillsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            agentVBox.addWidget(nameLabel)
            agentVBox.addWidget(descriptionLabel)
            agentVBox.addWidget(systemMessageLabel)
            agentVBox.addWidget(skillsLabel)
            agentBox.setLayout(agentVBox)
            self.allBoxes.append(agentBox)
            agentsLayout.addWidget(agentBox, row, col)
            col += 1
            if col == 3:
                col = 0
                row += 1
        agentsLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        agentsFrame.setLayout(agentsLayout)
        return agentsFrame

    def editAgent(self, clicked_agent):
        bold = QFont()
        bold.setBold(True)

        editFrame = QFrame()
        editLayout = QVBoxLayout()
        editLabel = QLabel("Edit Your Agent")
        editLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        editLabel.setFont(bold)
        editFrame.setStyleSheet("background-color: #5E5E5E; border-radius: 20;")
        editLayout.addWidget(editLabel)

        return editFrame

    def buildAgent(self):
        bold = QFont() #font for title
        bold.setBold(True)
        text_color = QColor(117, 219, 233)  # blue for field labels

        #lighter outer box
        editFrame = QFrame()
        editLayout = QVBoxLayout()
        editLabel = QLabel("Build Your Agent")
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
        contentLayout.addWidget(self.alignTextEditFields("Role", "Ex. Backend Engineer"))
        contentLayout.addWidget(self.alignTextEditFields("Description", "Ex. ..."))
        contentLayout.addWidget(self.alignTextEditFields("System Message", "Ex. ..."))

        # LLM dropdown
        LLM_label = self.setLabel('LLM')
        LLMcombobox = QComboBox()
        LLMcombobox.setStyleSheet("QComboBox { background-color: #5E5E5E; border-radius: 10px; padding: 5px; }")
        
        #pull from models.json
        file = open('./data/models.json')
        data = json.load(file)
        models = data["models"]

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
        maxInput = QLineEdit()
        maxInput.setPlaceholderText("Enter an integer 0-8")  # Set example text
        maxInput.setStyleSheet("QLineEdit { background-color: #5E5E5E; border-radius: 10px; padding: 5px; }")

        onlyInt = QIntValidator()
        onlyInt.setRange(0, 8)
        maxInput.setValidator(onlyInt)

        contentLayout.addWidget(self.alignHorizontal(max_label, maxInput))

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

        file = open('./data/functions.json')
        data = json.load(file)
        functions = data["functions"]

        for currentFunction in functions:
            checkbox = QCheckBox('   ' + currentFunction['name'])
            checkbox_layout.addWidget(checkbox)
            self.checkboxes.append(checkbox)
        # for i in range(20):
        #     checkbox = QCheckBox(f"Checkbox {i+1}")
        #     checkbox_layout.addWidget(checkbox)
        #     self.checkboxes.append(checkbox)

        # select_all_checkbox = QCheckBox("Select All")
        # deselect_all_checkbox = QCheckBox("Deselect All")
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

        # select_all_checkbox.stateChanged.connect(self.select_all_checkboxes)
        # deselect_all_checkbox.stateChanged.connect(self.deselect_all_checkboxes)
        select_all_button.clicked.connect(self.select_all_checkboxes)
        deselect_all_button.clicked.connect(self.deselect_all_checkboxes)
        #selectDeselect = self.alignHorizontal(select_all_button, deselect_all_button)
        allWidget = QWidget()
        allLayout = QHBoxLayout()
        allLayout.addWidget(select_all_button)
        allLayout.addWidget(deselect_all_button)
        allWidget.setLayout(allLayout)
        # allWidget.setStyleSheet("QWidget { margin-right: 50px; }")

        # selectDeselect = self.alignHorizontal(select_all_checkbox, deselect_all_checkbox)
        # for i in range(20):
        #     checkbox = QCheckBox(f"Checkbox {i+1}")
        #     checkbox_layout.addWidget(checkbox)

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
        
        contentLayout.addWidget(createButton, alignment=Qt.AlignmentFlag.AlignCenter)
        contentLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        contentBox.setLayout(contentLayout)

        editLayout.addWidget(contentBox)
        editLayout.setStretchFactor(contentBox, 1)
        editFrame.setLayout(editLayout)


        #edit json file
        # file = open('./data/agents.json')
        # data = json.load(file)

        return editFrame

    def select_all_checkboxes(self):
        for checkbox in self.checkboxes:
            checkbox.setChecked(True)

    def deselect_all_checkboxes(self):
        for checkbox in self.checkboxes:
            checkbox.setChecked(False)
    # def select_all_checkboxes(self, state):
    #     for checkbox in self.checkboxes:
    #         checkbox.setChecked(state == Qt.CheckState.Checked)

    # def deselect_all_checkboxes(self, state):
    #     for checkbox in self.checkboxes:
    #         checkbox.setChecked(state != Qt.CheckState.Checked)

    def alignTextEditFields(self, label, fieldInput):
        fieldLabel = self.setLabel(label)
        # fieldLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        field_input = QLineEdit()
        field_input.setPlaceholderText(fieldInput)  # Set example text
        field_input.setStyleSheet("QLineEdit { background-color: #5E5E5E; border-radius: 10px; padding: 5px; }")

        box = self.alignHorizontal(fieldLabel, field_input)
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

    def resetBorders(self, clicked_frame):
        # Reset borders of all clickable frames except the clicked frame
        for current in self.allBoxes:
            if current != clicked_frame:
                current.clicked = False
                current.update()

    def loadAgents(self):
        file = open('./data/agents.json')
        data = json.load(file)
        agents = self.agentBox(data["agents"])
        return agents
        # loop through agents and display accordingly
### TODO:
    # [ ] Rename variables