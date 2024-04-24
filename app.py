import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from components.customTabBar import CustomTabBar
# from components.dashboard import DashboardFrame
from components.agents import AgentsFrame
from components.teams import TeamsFrame
# from components.functions import FunctionsFrame
from components.chats import ChatsFrame
from components.models import ModelsFrame

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TaskForceAI")
        self.showMaximized()
        self.setStyleSheet("background-color: #464545; color: #ffffff;") 

        self.tab_widget = QTabWidget()
        self.tab_widget.currentChanged.connect(self.tab_changed)  # Connect the signal to the slot function
        self.tab_widget.setTabBar(CustomTabBar())
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.West)  # Set tabs to the left side
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane { 
                position: absolute;
                top: 0em;
                margin-right: 1px;
            }
            """)

        self.agentsFrame = AgentsFrame()
        self.chats = QWidget()
        self.chatsFrame = ChatsFrame()
        # self.functionsFrame = FunctionsFrame()
        self.teamsFrame = TeamsFrame()
        self.modelsFrame = ModelsFrame()

        # Create tabs
        self.create_tabs()

        # Set the main window's layout
        self.setCentralWidget(self.tab_widget)

    def create_tabs(self):
        # Top Bar With Logo - Chats
        chatsLogoLabel = QLabel("TaskForceAI - Chats")
        chatsLogoLabel.setFixedHeight(80)
        chatsLogoLabel.setStyleSheet("""
            background-color: #464545; 
            border-radius: 20; 
            padding-left: 20; 
            font-weight: bold; 
            color: #75DBE9;
        """)

        # Top Bar With Logo - Agents
        agentsLogoLabel = QLabel("TaskForceAI - Agents")
        agentsLogoLabel.setFixedHeight(80)
        agentsLogoLabel.setStyleSheet("""
            background-color: #464545; 
            border-radius: 20; 
            padding-left: 20; 
            font-weight: bold; \
            color: #75DBE9;
        """)

        # Top Bar With Logo - Dashboard
        teamsLogoLabel = QLabel("TaskForceAI - Teams")
        teamsLogoLabel.setFixedHeight(80)
        teamsLogoLabel.setStyleSheet("""
            background-color: #464545; 
            border-radius: 20; 
            padding-left: 20; 
            font-weight: bold; 
            color: #75DBE9;
        """)

        # Top Bar With Logo - Dashboard
        functionsLogoLabel = QLabel("TaskForceAI - Functions")
        functionsLogoLabel.setFixedHeight(80)
        functionsLogoLabel.setStyleSheet("""
            background-color: #464545; 
            border-radius: 20; 
            padding-left: 20; 
            font-weight: bold; 
            color: #75DBE9;
        """)

        # Top Bar With Logo - Settings
        modelsLogoLabel = QLabel("TaskForceAI - Models")
        modelsLogoLabel.setFixedHeight(80)
        modelsLogoLabel.setStyleSheet("""
            background-color: #464545; 
            border-radius: 20; 
            padding-left: 20; 
            font-weight: bold; 
            color: #75DBE9;
        """)

        # Chats Tab
        
        self.chats.setStyleSheet("background-color: #5E5E5E")

        chatsLayout = QVBoxLayout()
        chatsLayout.setSpacing(20)
        chatsLayout.addWidget(chatsLogoLabel)

        chatsLayout.addWidget(self.chatsFrame)

        self.chats.setLayout(chatsLayout)

        # Agents Tab
        agents = QWidget()
        agents.setStyleSheet("background-color: #5E5E5E")

        agentsLayout = QVBoxLayout()
        agentsLayout.setSpacing(20)
        agentsLayout.addWidget(agentsLogoLabel)

        agentsLayout.addWidget(self.agentsFrame)

        agents.setLayout(agentsLayout)

        # Teams Tab 
        teams = QWidget()
        teams.setStyleSheet("background-color: #5E5E5E")

        teamsLayout = QVBoxLayout()
        teamsLayout.setSpacing(20)
        teamsLayout.addWidget(teamsLogoLabel)

        teamsLayout.addWidget(self.teamsFrame)

        teams.setLayout(teamsLayout)

        # Teams Tab 
        # functions = QWidget()
        # functions.setStyleSheet("background-color: #5E5E5E")

        # functionsLayout = QVBoxLayout()
        # functionsLayout.setSpacing(20)
        # functionsLayout.addWidget(functionsLogoLabel)

        # functionsLayout.addWidget(self.functionsFrame)

        # functions.setLayout(functionsLayout)

        # Settings Tab
        models = QWidget()
        models.setStyleSheet("background-color: #5E5E5E")

        modelsLayout = QVBoxLayout()
        modelsLayout.setSpacing(20)
        modelsLayout.addWidget(modelsLogoLabel)

        modelsLayout.addWidget(self.modelsFrame)

        models.setLayout(modelsLayout)

        # Add tabs to the QTabWidget
        # self.tab_widget.addTab(dashboard, "Dashboard")
        self.tab_widget.addTab(self.chats, "Chats")
        self.tab_widget.addTab(agents, "Agents")
        self.tab_widget.addTab(teams, "Teams")
        # self.tab_widget.addTab(functions, "Functions")
        self.tab_widget.addTab(models, "Models")

    def tab_changed(self, index):
        current_tab_text = self.tab_widget.tabText(index)

        if current_tab_text == "Chats":
            new_frame = ChatsFrame() 
        if current_tab_text == "Agents":
            new_frame = AgentsFrame() 
        if current_tab_text == "Teams":
            new_frame = TeamsFrame() 
        # if current_tab_text == "Functions":
        #     new_frame = FunctionsFrame()
        if current_tab_text == "Models":
            new_frame = ModelsFrame()
        old_frame = self.tab_widget.widget(index).layout().itemAt(1).widget()  # Get the old frame from the layout
        self.tab_widget.widget(index).layout().replaceWidget(old_frame, new_frame)  # Replace the old frame with the new one
        old_frame.deleteLater() 

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = App()
    window.show()
    app.exec()
