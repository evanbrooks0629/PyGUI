from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import json
from components.alert import Alert

class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Are You Sure You Want to Delete?")
        self.setStyleSheet("background-color: #464545;") 
        self.setGeometry(((QGuiApplication.primaryScreen().size().width()//2) - 150), ((QGuiApplication.primaryScreen().size().height()//2) - 75), 300, 150)
        layout = QVBoxLayout()
        label = QLabel("Delete this team?")
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
        self.willDelete = True
        self.close()

class TeamsFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__()

        self.teamsPanel = TeamsPanel(self)

        self.editPanel = AddAgents(self)
        
        # Set tab style
        self.setStyleSheet("background-color: #464545; border-radius: 20;")
        self.mainhbox = QHBoxLayout()

        self.mainhbox.addWidget(self.teamsPanel)
        self.mainhbox.addWidget(self.editPanel)

        self.mainhbox.setStretchFactor(self.teamsPanel, 1) #equally sized left and right panels
        self.mainhbox.setStretchFactor(self.editPanel, 1)
        self.setLayout(self.mainhbox)


class TeamsPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mainFrame = parent
        self.clickableTeams = []
        self.setStyleSheet("background-color: #5E5E5E; border-radius: 20;")
        self.viewVBox = QVBoxLayout()
        bold = QFont()
        bold.setBold(True)
        self.teamLabel = QLabel('Teams')
        self.teamLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.teamLabel.setFont(bold)
        self.row = 1
        self.col = 0
        
        self.teams = QFrame()
        self.teamsLayout = QGridLayout()

        self.teamsInfo = self.loadTeams()
        self.teamBox(self.teamsInfo)
        self.teamsScroll = QScrollArea()
        self.teamsScroll.verticalScrollBar().setStyleSheet("""
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
        self.teamsScroll.setWidgetResizable(True)
        self.teamsScroll.setWidget(self.teams)
        self.viewVBox.addWidget(self.teamsScroll)
        self.setLayout(self.viewVBox)

    def teamBox(self, list_of_team_objects):
        self.teams.setStyleSheet("background-color: #5E5E5E; border-radius: 20;")
        self.teamsLayout.addWidget(self.teamLabel, 0, 0, 1, 6) 
        addButton = AddTeamButton()
        # addButton.setFixedSize(80, 40)
        self.teamsLayout.addWidget(addButton, 0, 4, 1, 2)

        ind = 0
        for currentTeam in list_of_team_objects:
            obj = currentTeam
            teamBox = ClickableFrame(obj, self.mainFrame, ind, self)
            ind = ind + 1
            self.clickableTeams.append(teamBox)

            self.teamsLayout.addWidget(teamBox, self.row, self.col * 3, 1, 3)
            self.col += 1
            if self.col == 2:
                self.col = 0
                self.row += 1
            #self.teamsLayout.setStretchFactor(teamBox, 1) 
        self.teamsLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.teams.setLayout(self.teamsLayout)
    
    def add_team(self, obj):
        new_box = ClickableFrame(obj, self.mainFrame, len(self.clickableTeams), self)
        self.clickableTeams.append(new_box)
        self.teamsLayout.addWidget(new_box, self.row, self.col * 3, 1, 3)
        self.col += 1
        if self.col == 2:
            self.col = 0
            self.row += 1
        #self.teamsLayout.setStretchFactor(teamBox, 1) 

    def resetBorders(self, clicked_frame):
        # Reset borders of all clickable frames except the clicked frame
        for current in self.clickableTeams:
            if current != clicked_frame:
                current.clicked = False
                current.update()
    
    def loadTeams(self):
        # parse json data and get all chats
        file = open('./data/teams.json')
        data = json.load(file)
        teams = data["teams"]
        return teams
        
    def refreshFrame(self):
        for current in self.clickableTeams:
            current.setParent(None)  # Remove from layout
            current.deleteLater()  # Delete widget

        new_frame = TeamsPanel(parent=self.parent())
        self.mainFrame.editPanel.teamsFrame = new_frame
        self.mainFrame.teamsPanel = new_frame
        self.parent().layout().replaceWidget(self, new_frame)
        self.deleteLater()
    
class AddTeamButton(QPushButton):
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
        self.setText("Create Team")
        self.setIcon(QIcon('./assets/AddTeamIcon.png'))
        self.setIconSize(QSize(48, 24))

    def mousePressEvent(self, event):
        for checkbox in self.parent().parent().parent().parent().mainFrame.editPanel.checkboxes:
            if checkbox.isChecked():
                checkbox.setChecked(False)
        newTeam = {
            "name": "",
            "id": "",
            "agents": []
        }

        self.parent().parent().parent().parent().mainFrame.editPanel.currentTeam = newTeam
        self.parent().parent().parent().parent().mainFrame.editPanel.setFields(newTeam)
        self.parent().parent().parent().parent().mainFrame.editPanel.editLabel.setText("Build Your Team")
        self.parent().parent().parent().parent().mainFrame.editPanel.createButton.setText("Create Team")
        self.parent().parent().parent().parent().mainFrame.editPanel.deleteButton.hide()
        self.parent().parent().parent().parent().mainFrame.teamsPanel.resetBorders(self)

class ClickableFrame(QFrame):
    def __init__(self, currentTeam, widget, pos, parent=None):
        super().__init__(parent)
        self.teamsPanel = parent
        self.position = pos
        self.widget = widget # Keeps track of associated AgentsFrame class

        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # import any information needed from the agent for editing
        self.team = currentTeam #raw json information
        self.clicked = False #variable to keep tracked of click
        self.setFixedWidth(285)
        self.setFixedHeight(200)
        self.setStyleSheet("""
            background-color: #464545;
            border-radius: 10;
        """)
        bold = QFont()
        bold.setBold(True)
        teamVBox = QVBoxLayout()
        self.name = currentTeam['name']
        self.agents = currentTeam["agents"]
        self.nameLabel = QLabel(self.name)
        self.nameLabel.setFixedHeight(25)
        self.nameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.nameLabel.setFont(bold)

        descriptionLine = QLabel()
        descriptionLine.setStyleSheet("""
            background-color: #5E5E5E;
            border-radius: 0;
        """)
        descriptionLine.setFixedHeight(2)
        
        teamVBox.addWidget(self.nameLabel)
        teamVBox.addWidget(descriptionLine)
        agentsText = QLabel("Agents")
        teamVBox.addWidget(agentsText)

        file = open('./data/agents.json')
        data = json.load(file)
        #make sure synchronized w/ deleted agents

        for i in range(len(self.agents)):
            filtered_agents = filter(lambda agent: agent.get('id') == self.agents[i], data.get('agents', []))
            found_agent = next(filtered_agents, None)
            agentLabel = QLabel(found_agent['name'])
            agentLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            agentLabel.setStyleSheet("""
                border: 1px solid white;
                padding-left: 2;
                padding-right: 2;
                border-radius: 5;
                font-size: 24;
            """)
            agentLabel.setFixedHeight(25)
            teamVBox.addWidget(agentLabel)
        self.setLayout(teamVBox)

    def mousePressEvent(self, event):
        self.widget.editPanel.deselect_all_checkboxes()
        self.widget.teamsPanel.resetBorders(self) #unmark the borders of the previously clicked agent
        self.clicked = not self.clicked
        if self.clicked:
            self.widget.editPanel.clickedTeam = self
            self.widget.editPanel.currentTeam = self.team 
            self.widget.editPanel.setFields(self.team)    
            self.widget.editPanel.update() 
            self.widget.editPanel.editLabel.setText("Edit Your Team")
            self.widget.editPanel.createButton.setText("Edit Team")
            self.widget.editPanel.deleteButton.show()

            for checkbox in self.widget.editPanel.checkboxes:
                if checkbox.property("value") in self.agents:
                    checkbox.setChecked(True)

        else :
            self.widget.editPanel.currentTeam = {
                "name": "",
                "id": "",
                "agents": []
            }  
            self.widget.editPanel.setFields(self.widget.editPanel.currentTeam)
            self.widget.editPanel.deselect_all_checkboxes()
            self.widget.editPanel.editLabel.setText("Build Your Team")
            self.widget.editPanel.createButton.setText("Create Team")
            self.widget.editPanel.deleteButton.hide()
            self.widget.editPanel.update()
            
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
        new_box = ClickableFrame(obj, self.widget, self.position, self.teamsPanel)
        self.teamsPanel.clickableTeams[self.position] = new_box
        self.parent().layout().replaceWidget(self, new_box)
        self.deleteLater()

class AddAgents(QFrame):
    def __init__(self, frame):
        super().__init__()
        
        self.teamsFrame = frame.teamsPanel 

        #Keep track of all skills checkboxes
        self.checkboxes = []
        self.clickedTeam = QFrame()
        self.currentTeam = {
            "name": "",
            "id": "",
            "agents": []
        }

        self.editLabel = QLabel("Build Your Team")
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

        #text field
        self.name_input = QLineEdit()
        self.name_input.setText(self.currentTeam['name'])
        self.name_input.setStyleSheet("QLineEdit { background-color: #5E5E5E; border-radius: 10px; padding: 5px; }")
        contentLayout.addWidget(self.alignTextEditFields("Team Name", self.name_input))
        
        #agents checkbox section
        widge = QWidget()
        scroll_area = QScrollArea(widge)
        scroll_area.setWidgetResizable(True)
        scroll_bar = scroll_area.verticalScrollBar()
        scroll_bar.setStyleSheet("QScrollBar:vertical { background: #5E5E5E; width: 14px;}")
        scroll_area.setStyleSheet("QScrollArea { margin-left: 20px; margin-right: 40px; min-height: 20em; max-width: 20em }")

        checkbox_widget = QWidget()
        checkbox_layout = QVBoxLayout(checkbox_widget)
        checkbox_layout.setContentsMargins(80, 0, 0, 0)

        file = open('./data/agents.json')
        data = json.load(file)
        agents = data["agents"]

        for currentFunction in agents:
            checkbox = QCheckBox('   ' + currentFunction['name'])
            checkbox.setProperty("value", currentFunction['id'])
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
        agentsWidget = QWidget()
        agentLayout = QHBoxLayout()
        agentLabel = self.setLabel('Agents')

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
        agentLabel.setAlignment(Qt.AlignmentFlag.AlignTop)
        agentLayout.addWidget(agentLabel)
        agentLayout.addWidget(checksWidget)
        agentsWidget.setLayout(agentLayout)
        agentsWidget.setFixedHeight(375)
        contentLayout.addWidget(agentsWidget)

        self.deleteButton = QPushButton("Delete Team")
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
            text=" Create Team", icon=QIcon('./assets/Sparkling.png')
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

    def setFields(self, team):
        self.name_input.setText(team['name'])
        #add checks?

    def createClicked(self):
        #upload new edits into json
        print('create clicked')
        file = open('./data/teams.json')
        data = json.load(file)
        filtered_teams = filter(lambda team: team.get('id') == self.currentTeam['id'], data.get('teams', []))

        found_team = next(filtered_teams, None)

        selected_agents = []
        for checkbox in self.checkboxes:
            if checkbox.isChecked():
                selected_agents.append(checkbox.property("value"))
                checkbox.setChecked(False)

        self.currentTeam["agents"] = selected_agents

        if found_team:
            found_team['id'] = self.currentTeam['id'] 
            found_team['name'] = self.name_input.text()
            found_team['agents'] = self.currentTeam['agents']
 
        else:
            self.currentTeam['id'] = str(int(data.get('teams', [])[-1]['id']) + 1)  #add id functionality
            print(str(int(data.get('teams', [])[-1]['id'])))
            self.currentTeam['name'] = self.name_input.text()
            self.currentTeam['agents'] = selected_agents
            data['teams'].append(self.currentTeam)

        with open('./data/teams.json', 'w') as file:
                # Write the updated data back to the file
                json.dump(data, file, indent=2)
        
        dialog = Alert("SUCCESS", "Team created successfully.")

        if found_team:
            self.clickedTeam.refreshFrame(found_team)
            self.clickedTeam = QFrame()
            dialog = Alert("SUCCESS", "Team edited successfully.")
        else:
            self.teamsFrame.add_team(self.currentTeam)

        self.currentTeam = {
            "name": "",
            "id": "",
            "agents": []
        }  
        self.setFields(self.currentTeam)
        self.deselect_all_checkboxes()
        self.editLabel.setText("Build Your Tean")
        self.createButton.setText("Create Team")
        self.deleteButton.hide()
        self.update()

        
        dialog_width = 250
        dialog_height = 50

        main_window = self.window()

        # Calculate the new position
        new_x = main_window.geometry().x() + main_window.geometry().width() - dialog_width - 100
        new_y = main_window.geometry().y() + main_window.geometry().height() - dialog_height - 50

        # Move the dialog to the bottom right corner of the main application window
        dialog.move(new_x, new_y)
        
        # Optional: Set dialog window flags, like making it frameless
        dialog.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        
        dialog.exec()

    def deleteClicked(self):
        dialog = DeleteDialog()
        screen = self.screen()  # Get the screen of the main window
        rect = screen.geometry()  # Get the geometry of this screen
        
        # Optional: Center the dialog within the screen
        dialog.move(
            rect.x() + (rect.width() - dialog.width()) // 2,
            rect.y() + (rect.height() - dialog.height()) // 2,
        )
        
        dialog.exec()
        willDelete = dialog.willDelete
        print(willDelete)

        if willDelete:
            print('delete clicked')
            teamId = self.currentTeam["id"]

            file = open('./data/teams.json')
            data = json.load(file)
            updatedTeams = []
            for team in data["teams"]:
                if team["id"] != teamId:
                    updatedTeams.append(team)
            data["teams"] = updatedTeams
            with open('./data/teams.json', 'w') as file:
                # Write the updated data back to the file
                json.dump(data, file, indent=2)

            self.teamsFrame.refreshFrame()
            self.currentTeam = {
                "name": "",
                "id": "",
                "agents": []
            }  
            self.setFields(self.currentTeam)
            self.deselect_all_checkboxes()
            self.editLabel.setText("Build Your Team")
            self.createButton.setText("Create Team")
            self.deleteButton.hide()
            self.update()

            dialog = Alert("SUCCESS", "Team deleted successfully.")
            dialog_width = 250
            dialog_height = 50

            main_window = self.window()

            # Calculate the new position
            new_x = main_window.geometry().x() + main_window.geometry().width() - dialog_width - 100
            new_y = main_window.geometry().y() + main_window.geometry().height() - dialog_height - 50

            # Move the dialog to the bottom right corner of the main application window
            dialog.move(new_x, new_y)
            
            # Optional: Set dialog window flags, like making it frameless
            dialog.setWindowFlags(Qt.WindowType.FramelessWindowHint)
            
            dialog.exec()

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