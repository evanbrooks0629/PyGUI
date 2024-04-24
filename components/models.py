from PyQt6.QtGui import QMouseEvent
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
        self.resize(300, 150)
        # self.setGeometry(((QGuiApplication.primaryScreen().size().width()//2) - 150), ((QGuiApplication.primaryScreen().size().height()//2) - 75), 300, 150)
        layout = QVBoxLayout()
        label = QLabel("Delete this model?")
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

class ModelsFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__()

        self.modelsPanel = ModelsPanel(self)

        #for changing contents of right panel
        self.editPanel = ModelsValues(self)
        
        # Set tab style
        self.setStyleSheet("background-color: #464545; border-radius: 20;")
        self.mainhbox = QVBoxLayout()

        self.mainhbox.addWidget(self.editPanel)
        self.mainhbox.addWidget(self.modelsPanel)
        

        # self.mainhbox.setStretchFactor(self.modelsPanel) #equally sized left and right panels
        # self.mainhbox.setStretchFactor(self.editPanel, 1)
        self.setLayout(self.mainhbox)

class ModelsPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mainFrame = parent
        self.clickableModels = []
        self.setStyleSheet("background-color: #5E5E5E; border-radius: 20;")
        self.viewVBox = QVBoxLayout()
        self.modelsLabel = QLabel('Select your model')
        bold = QFont()
        bold.setBold(True)
        text_color = QColor(117, 219, 233)  # blue for field labels
        
        self.modelsLabel.setStyleSheet(f"color: {text_color.name()};")
        self.modelsLabel.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        self.modelsLabel.setFont(bold)
       
        
        self.models = QFrame()
        self.modelsLayout = QVBoxLayout()

        self.modelsInfo = self.loadModels()
        self.modelsBox(self.modelsInfo)
        self.modelsScroll = QScrollArea()
        self.modelsScroll.verticalScrollBar().setStyleSheet("""
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
        self.modelsScroll.setWidgetResizable(True)
        self.modelsScroll.setWidget(self.models)
        self.viewVBox.addWidget(self.modelsScroll)
        self.setLayout(self.viewVBox)

    def modelsBox(self, list_of_models_objects):
        self.models.setStyleSheet("background-color: #5E5E5E; border-radius: 20;")
        self.modelsLayout.addSpacing(8)
        self.modelsLayout.addWidget(self.modelsLabel) 
        self.modelsLayout.addSpacing(8)

        # addButton = AddModelsButton()
        # addButton.setFixedSize(80, 40)
        # self.modelsLayout.addWidget(addButton, 0, 2, 1, 1)

        ind = 0
        for currentModel in list_of_models_objects:
            obj = currentModel
            modelBox = ClickableFrame(obj, self.mainFrame, ind, self)
            ind = ind + 1
            self.clickableModels.append(modelBox)
            self.modelsLayout.addWidget(modelBox)
            # self.col += 1
            # if self.col == 3:
            #     self.col = 0
            #     self.row += 1
        self.modelsLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        #self.modelsLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.models.setLayout(self.modelsLayout)
    
    def add_models(self, obj):
        #set obj to new json
        new_box = ClickableFrame(obj, self.mainFrame, len(self.clickableModels), self)
        self.clickableModels.append(new_box)
        self.modelsLayout.addWidget(new_box, self.row, self.col)
        self.col += 1
        if self.col == 3:
            self.col = 0
            self.row += 1

    def resetBorders(self, clicked_frame):
        # Reset borders of all clickable frames except the clicked frame
        for current in self.clickableModels:
            if current != clicked_frame:
                current.clicked = False
                current.update()

    def loadModels(self):
        file = open('./data/models.json')
        data = json.load(file)
        models = data['models']
        return models
        
    def refreshFrame(self):
        for current in self.clickableModels:
            current.setParent(None)  # Remove from layout
            current.deleteLater()  # Delete widget

        new_frame = ModelsPanel(parent=self.parent())
        self.mainFrame.editPanel.modelsFrame = new_frame
        self.mainFrame.modelsPanel = new_frame
        self.parent().layout().replaceWidget(self, new_frame)
        self.deleteLater()


class AddModelsButton(QPushButton):
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
        self.setText("Add New Model")
        self.setIcon(QIcon('./assets/AddModelIcon.png'))
        self.setIconSize(QSize(48, 24))
        
    def mousePressEvent(self, event):
        print("Adding Model Clicked")
       
        newModel = {
            "model": "",
            "base_url": "",
            "api_type": "",
            "api_key": ""
        }

        self.parent().parent().parent().parent().mainFrame.editPanel.currentModel = newModel
        self.parent().parent().parent().parent().mainFrame.editPanel.setFields(newModel)
        self.parent().parent().parent().parent().mainFrame.editPanel.editLabel.setText("Build Your Model")
        self.parent().parent().parent().parent().mainFrame.editPanel.createButton.setText("Create Model")
        self.parent().parent().parent().parent().mainFrame.editPanel.deleteButton.hide()
        self.parent().parent().parent().parent().mainFrame.modelsPanel.resetBorders(self)

class ClickableFrame(QFrame):
    def __init__(self, currentModel, widget, pos, parent=None):
        super().__init__(parent)
        self.modelsPanel = parent
        self.position = pos
        self.widget = widget 

        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.model = currentModel #raw json information
        self.clicked = False #variable to keep tracked of click
        self.setFixedWidth(500)
        self.setFixedHeight(110)
        self.setStyleSheet("""
            background-color: #464545;
            border-radius: 20;
        """)
        bold = QFont()
        bold.setBold(True)
        modelsVBox = QVBoxLayout()
        self.name = currentModel['model']
        self.base_url = currentModel['base_url']
        self.api_type = currentModel["api_type"]
        self.api_key = currentModel["api_key"]
        self.groq = currentModel["groq"]
        name = ""
        if self.groq:
            name = "[Groq] " + self.name
        else:
            name = "[Ollama] " + self.name
        self.nameLabel = QLabel(name)
        self.nameLabel.setFixedHeight(25)
        self.nameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.nameLabel.setFont(bold)

        self.status = QLabel("Status:") 
        # self.status.setStyleSheet("QLabel { padding-left: 70px; }")
        self.status.setFont(bold)
        self.connected = QLabel("CONNECTED")
        connected_color = QColor(36, 201, 53)  
        self.connected.setStyleSheet(f"color: {connected_color.name()};")
        self.connected.setFont(bold)
        self.connected.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.offline = QLabel("OFFLINE")
        offline_color = QColor(159, 159, 159)  
        self.offline.setStyleSheet(f"color: {offline_color.name()};")
        self.offline.setFont(bold)
        self.offline.setAlignment(Qt.AlignmentFlag.AlignCenter)

        statBox = QFrame()
        layout = QHBoxLayout()
        # layout.addWidget(self.status)
        # layout.setStretchFactor(self.status, 1)

        connected = True #add connected functionality
        if (connected):
            layout.addWidget(self.connected)
            layout.setStretchFactor(self.connected, 1)
        else:
            layout.addWidget(self.offline)
            layout.setStretchFactor(self.offline, 1)


        statBox.setLayout(layout)

        descriptionLine = QLabel()
        descriptionLine.setStyleSheet("""
            background-color: #5E5E5E;
            border-radius: 0;
        """)
        descriptionLine.setFixedHeight(2)
        descriptionLine.setWordWrap(True)

        modelsVBox.addWidget(self.nameLabel)
        modelsVBox.addWidget(descriptionLine)
        modelsVBox.addWidget(statBox)
        self.setLayout(modelsVBox)

    def mousePressEvent(self, event):
        print(self.model['model'] ,"Frame Clicked!")
        self.widget.modelsPanel.resetBorders(self) 
        self.clicked = not self.clicked
        if self.clicked:
            self.widget.editPanel.clickedModel = self
            self.widget.editPanel.currentModel = self.model 
            # self.widget.editPanel.setFields(self.model)    
            self.widget.editPanel.update() 
            # self.widget.editPanel.editLabel.setText("Edit Your Model")
            # self.widget.editPanel.createButton.setText("Edit Model")
            # self.widget.editPanel.deleteButton.show()
            # set clicked value in llm_config with passed-in api-key
            file = open('./data/models.json')
            data = json.load(file)
            selected_model = {
                "llm_config": {}
            }

            for model in data["models"]:
                if model["model"] == self.name:
                    selected_model["llm_config"] = model

            with open('./data/llm.json', 'w') as file:
                # Write the updated data back to the file
                json.dump(selected_model, file, indent=2)

            dialog = Alert("SUCCESS", "Model selected successfully.")
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
        else:
            self.widget.editPanel.currentModel = {
                "model": "",
                "base_url": "",
                "api_type": "",
                "api_key": ""
            }
            # self.widget.editPanel.setFields(self.widget.editPanel.currentModel)
            # self.widget.editPanel.editLabel.setText("Build Your Model")
            # self.widget.editPanel.createButton.setText("Create Model")
            # self.widget.editPanel.deleteButton.hide()
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
            painter.drawRoundedRect(1, 1, self.width() - 2, self.height() - 2, 20, 20)  

    def refreshFrame(self, obj):
        new_box = ClickableFrame(obj, self.widget, self.position, self.modelsPanel)
        self.modelsPanel.clickableModels[self.position] = new_box
        self.parent().layout().replaceWidget(self, new_box)
        self.deleteLater()

class ModelsValues(QFrame):
    def __init__(self, frame):
        super().__init__()
        
        self.modelsFrame = frame.modelsPanel 

        #Keep track of all skills checkboxes
        self.checkboxes = []
        self.clickedModel = QFrame()
        self.currentModel = {
            "model": "",
            "base_url": "",
            "api_type": "",
            "api_key": ""
        }

        self.editLabel = QLabel("Build Your Model")
        bold = QFont() #font for title
        bold.setBold(True)
        text_color = QColor(117, 219, 233)  # blue for field labels

        #lighter outer box
        # editFrame = QFrame()
        editLayout = QVBoxLayout()
        
        # self.editLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.editLabel.setFont(bold)
        # editFrame.setStyleSheet("background-color: #5E5E5E; border-radius: 20;")
        # editLayout.addWidget(self.editLabel)
        # editLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #darker box
        contentBox = QFrame()
        contentLayout = QVBoxLayout()
        contentBox.setStyleSheet("""
                background-color: #464545;
                border-radius: 10;
            """)

        #text fields
        # load api key
        file = open('./data/groq.json')
        data = json.load(file)
        key = data["groq_api_key"]
        self.groq_input = QLineEdit()
        self.groq_input.setFixedWidth(500)
        self.groq_input.setText(key)
        fieldLabel = self.setLabel("Add your groq API key (only for groq models):")
        self.groq_input.setStyleSheet("QLineEdit { background-color: #5E5E5E; border-radius: 10px; padding: 5px; }")
        

        self.createButton = QPushButton(
            text=" Add API Key", icon=QIcon('./assets/Sparkling.png')
        )
        self.createButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.createButton.setFixedWidth(150)
        self.createButton.setFixedHeight(40)
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

        self.bottomButtonBox.addWidget(fieldLabel)
        self.bottomButtonBox.addWidget(self.groq_input)
        self.bottomButtonBox.addWidget(self.createButton)
        self.bottomButtonFrame.setLayout(self.bottomButtonBox)

        contentLayout.addWidget(self.bottomButtonFrame, alignment=Qt.AlignmentFlag.AlignCenter)
        contentLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        contentBox.setLayout(contentLayout)

        editLayout.addWidget(contentBox)
        # editLayout.setStretchFactor(contentBox, 1)
        self.setLayout(editLayout)

    def setFields(self, model):
        return
        # self.name_input.setText(model['model'])
        # self.base_url_input.setText(model['base_url'])
        # self.api_type_input.setText(model['api_type'])
        # self.api_key_input.setText(model['api_key'])   

    def createClicked(self):
        # save API key
        # get api key input
        key = self.groq_input.text()
        data = {
            "groq_api_key": key
        }

        with open('./data/groq.json', 'w') as file:
                # Write the updated data back to the file
                json.dump(data, file, indent=2)
        
        dialog = Alert("SUCCESS", "API key saved successfully.")

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
            modelName = self.currentModel["model"]

            file = open('./data/models.json')
            data = json.load(file)
           
            updatedModels = []
            for model in data["models"]:
                if model["model"] != modelName:
                    updatedModels.append(model)
            data["models"] = updatedModels
            with open('./data/models.json', 'w') as file:
                # Write the updated data back to the file
                json.dump(data, file, indent=2)

            self.modelsFrame.refreshFrame()
            self.currentModel = {
                "model": "",
                "base_url": "",
                "api_type": "",
                "api_key": ""
            }
            self.setFields(self.currentModel)
            self.editLabel.setText("Build Your Model")
            self.createButton.setText("Create Model")
            self.deleteButton.hide()
            self.update()

            dialog = Alert("SUCCESS", "Model deleted successfully.")
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
  
    # def alignTextEditFields(self, label, fieldInput):
    #     fieldLabel = self.setLabel(label)
    #     box = self.align(fieldLabel, fieldInput)
    #     return box
    
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
        #fieldLabel.setFixedWidth(110)  # Set a fixed width for the label

        return fieldLabel