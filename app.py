import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from components.customTabBar import CustomTabBar
from components.dashboard import DashboardFrame
from components.employees import EmployeesFrame
from components.chats import ChatsFrame
from components.settings import SettingsFrame

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TaskForceAI")
        self.showMaximized()
        self.setStyleSheet("background-color: #464545;") 

        self.tab_widget = QTabWidget()
        self.tab_widget.setTabBar(CustomTabBar())
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.West)  # Set tabs to the left side
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane { 
                position: absolute;
                top: 0em;
                margin-right: 1px;
            }
            """)

        # Create tabs
        self.create_tabs()

        # Set the main window's layout
        self.setCentralWidget(self.tab_widget)

    def create_tabs(self):
        # Top Bar With Logo - Dashboard
        dashboardLogoLabel = QLabel("TaskForceAI - Dashboard")
        dashboardLogoLabel.setFixedHeight(80)
        dashboardLogoLabel.setStyleSheet("""
            background-color: #464545; 
            border-radius: 20; 
            padding-left: 20; 
            font-weight: bold; 
            color: #75DBE9;
        """)

        # Top Bar With Logo - Employees
        employeesLogoLabel = QLabel("TaskForceAI - Employees")
        employeesLogoLabel.setFixedHeight(80)
        employeesLogoLabel.setStyleSheet("""
            background-color: #464545; 
            border-radius: 20; 
            padding-left: 20; 
            font-weight: bold; 
            color: #75DBE9;
        """)

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

        # Top Bar With Logo - Settings
        settingsLogoLabel = QLabel("TaskForceAI - Settings")
        settingsLogoLabel.setFixedHeight(80)
        settingsLogoLabel.setStyleSheet("""
            background-color: #464545; 
            border-radius: 20; 
            padding-left: 20; 
            font-weight: bold; 
            color: #75DBE9;
        """)

        # Dashboard Tab 
        dashboard = QWidget()
        dashboard.setStyleSheet("background-color: #5E5E5E")

        dashboardLayout = QVBoxLayout()
        dashboardLayout.setSpacing(20)
        dashboardLayout.addWidget(dashboardLogoLabel)

        dashoardFrame = DashboardFrame()
        dashboardLayout.addWidget(dashoardFrame)

        dashboard.setLayout(dashboardLayout)

        # Employees Tab
        employees = QWidget()
        employees.setStyleSheet("background-color: #5E5E5E")

        employeesLayout = QVBoxLayout()
        employeesLayout.setSpacing(20)
        employeesLayout.addWidget(employeesLogoLabel)

        employeesFrame = EmployeesFrame()
        employeesLayout.addWidget(employeesFrame)

        employees.setLayout(employeesLayout)

        # Chats Tab
        chats = QWidget()
        chats.setStyleSheet("background-color: #5E5E5E")

        chatsLayout = QVBoxLayout()
        chatsLayout.setSpacing(20)
        chatsLayout.addWidget(chatsLogoLabel)

        chatsFrame = ChatsFrame()
        chatsLayout.addWidget(chatsFrame)

        chats.setLayout(chatsLayout)

        # Settings Tab
        settings = QWidget()
        settings.setStyleSheet("background-color: #5E5E5E")

        settingsLayout = QVBoxLayout()
        settingsLayout.setSpacing(20)
        settingsLayout.addWidget(settingsLogoLabel)

        settingsFrame = SettingsFrame()
        settingsLayout.addWidget(settingsFrame)

        settings.setLayout(settingsLayout)

        # Add tabs to the QTabWidget
        self.tab_widget.addTab(dashboard, "Dashboard")
        self.tab_widget.addTab(employees, "Employees")
        self.tab_widget.addTab(chats, "Chats")
        self.tab_widget.addTab(settings, "Settings")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = App()
    window.show()
    app.exec()
