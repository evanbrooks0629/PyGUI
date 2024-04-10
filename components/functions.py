from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import json
import sys
import shutil
from pathlib import Path
import os

from PyQt6.QtWidgets import QWidget
from components.alert import Alert

class AddFunctionButton(QPushButton):
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
        """)
        self.setText("Add Function")
        self.setIcon(QIcon('./assets/AddFunctionIcon.png'))
        self.setIconSize(QSize(56, 28))

    def mousePressEvent(self, event):
        self.parent().parent().parent().parent().mainFrame.editPanel.currentFunction = {
            "id": "",
            "name": "",
            "filePath": "",
            "description": "",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
        self.parent().parent().parent().parent().mainFrame.editPanel.nameInput.setText("untitled")
        self.parent().parent().parent().parent().mainFrame.editPanel.descriptionInput.setPlainText("")
        self.parent().parent().parent().parent().mainFrame.editPanel.editor.setPlainText("")
        self.parent().parent().parent().parent().mainFrame.functionsPanel.resetBorders(self)
        self.parent().parent().parent().parent().mainFrame.editPanel.importButton.show()
        for param in self.parent().parent().parent().parent().mainFrame.paramPanel.parameters:
            param.deleteLater()
        self.parent().parent().parent().parent().mainFrame.paramPanel.parameters = []

class ImportButton(QPushButton):
    def __init__(self, getCurrentFunction, parent=None):
        super().__init__(parent)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.clicked = False
        self.getCurrentFunction = getCurrentFunction
        self.setStyleSheet("""
            QPushButton {
                color: #75DBE9;
                text-align: bottom;
                font-size: 11px;
                border: 2px solid #75DBE9;
                padding: 2px 4px;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #111111;
            }
        """)
        self.setText("Import")

    def mousePressEvent(self, event):
        # Filter to only show Python files
        filter = "Python Files (*.py)"
        response = QFileDialog.getOpenFileName(
            parent=self,
            caption="Open Python File",
            directory=os.path.expanduser('~'),
            filter=filter
        )
        
        # 'response' is a tuple where the first element is the file path,
        # and the second element is the filter used.
        # If a file is selected, the path will be printed to the console.
        sourceFilePath = response[0]
        if sourceFilePath:

            project_directory = os.path.join(os.getcwd(), 'functions')  # Using current working directory for simplicity

            # Extract the base filename from the selected file
            base_filename = os.path.basename(sourceFilePath)

            # Construct the save file path within the project directory
            saveFilePath = os.path.join(project_directory, base_filename)

            try:
                # Copy the file from source to destination
                shutil.copyfile(sourceFilePath, saveFilePath)

                functionName = sourceFilePath.split("/")[-1].split(".")[0]
                # update UI
                self.parent().parent().parent().nameInput.setText(functionName)
                
                file = open(f"./functions/{functionName}.py", "r")
                code = file.read()

                self.parent().parent().parent().editor.setPlainText(code)

                dialog = Alert("SUCCESS", "Function imported successfully.")
                
            except Exception as e:

                dialog = Alert("ERROR", "Function imported unsuccessfully.")
           
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



class ExportButton(QPushButton):
    def __init__(self, getCurrentFunction, parent=None):
        super().__init__(parent)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.clicked = False
        self.getCurrentFunction = getCurrentFunction
        self.setStyleSheet("""
            QPushButton {
                color: #75DBE9;
                text-align: bottom;
                font-size: 11px;
                border: 2px solid #75DBE9;
                padding: 2px 4px;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #111111;
            }
        """)
        self.setText("Export")

    def mousePressEvent(self, event):
        currentFunction = self.getCurrentFunction()
        source_path = currentFunction["filePath"]  # Adjust to your file's path
        downloads_path = str(Path.home() / 'Downloads')
        file_name = currentFunction["name"] + ".py"
        destination_path = os.path.join(downloads_path, file_name)  # Adjust filename as needed
        try:
            shutil.copyfile(source_path, destination_path)
            # Here you can add any post-copy success actions, like showing a success message to the user.

            dialog = Alert("SUCCESS", "Function downloaded successfully.")
        except Exception as e:
            # Handle errors, for example, showing an error message to the user.

            dialog = Alert("ERROR", "Function downloaded unsuccessfully.")
        
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

        

class SaveButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.clicked = False
        self.setStyleSheet("""
            QPushButton {
                color: #75DBE9;
                text-align: bottom;
                font-size: 11px;
                border: 2px solid #75DBE9;
                padding: 2px 4px;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #111111;
            }
        """)
        self.setText("Save")

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        functionName = self.parent().parent().parent().parent().nameInput.text()
        fileName = functionName + ".py"

        functionDescription = self.parent().parent().parent().parent().descriptionInput.toPlainText()

        # need to save file and its contents in functionName.py
        pythonCode = self.parent().parent().parent().parent().editor.toPlainText()
        filePath = f"./functions/{fileName}"
        file = open(filePath, "w")
        file.write(pythonCode)

        jsonFile = open('./data/functions.json')
        data = json.load(jsonFile)
        lastID = int(data["functions"][-1]["id"]) # for new function

        # get function parameters
        paramsObject = {
            "type": "object",
            "properties": {},
            "required": []
        }
        # "parameters": {
        #     "type": "object",
        #     "properties": {},
        #     "required": []
        # }
        functionParameters = self.parent().parent().parent().parent().parent().paramPanel.parameters
        for param in functionParameters:
            if param.name is not None and param.type is not None and param.description is not None:
                paramsObject["properties"][param.name] = {
                    "type": param.type,
                    "description": param.description
                }
                paramsObject["required"].append(param.name)
            # else:
                # open error dialog

        doesFunctionExist = False
        for f in data["functions"]:
            if self.parent().parent().parent().parent().currentFunction["id"] == f["id"]:
                doesFunctionExist = True
                f["name"] = functionName
                f["filePath"] = filePath
                f["description"] = functionDescription
                f["parameters"] = paramsObject

        if not doesFunctionExist:
            newFunctionObject = {
                "name": functionName,
                "id": str(lastID + 1),
                "filePath": filePath,
                "description": functionDescription,
                "parameters": paramsObject
            }
            data['functions'].append(newFunctionObject)

        with open('./data/functions.json', 'w') as newFile:
                # Write the updated data back to the file
            json.dump(data, newFile, indent=2)

        #update file path to match the text edit
        for current in self.parent().parent().parent().parent().parent().functionsPanel.clickableFunctions:
            if current.clicked:
                current.nameLabel.setText(functionName)

        self.parent().parent().parent().parent().parent().functionsPanel.refreshFrame() #not teamsFrame
        self.parent().parent().parent().parent().parent().functionsPanel.resetBorders(self)

        self.openDialog()
    
    def openDialog(self):

        dialog = Alert("SUCCESS", "Function saved successfully.")
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

class DeleteButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.clicked = False
        self.setStyleSheet("""
            QPushButton {
                color: #75DBE9;
                text-align: bottom;
                font-size: 11px;
                border: 2px solid #75DBE9;
                padding: 2px 4px;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #111111;
            }

            QPushButton:pressed {
                background-color: #5E5E5E;
            }
        """)
        self.setText("Delete")
    
    def mousePressEvent(self, event):
        dialog = DeleteDialog(self)
        screen = self.screen()  # Get the screen of the main window
        rect = screen.geometry()  # Get the geometry of this screen
        
        # Optional: Center the dialog within the screen
        dialog.move(
            rect.x() + (rect.width() - dialog.width()) // 2,
            rect.y() + (rect.height() - dialog.height()) // 2,
        )
        
        dialog.exec()
        willDelete = dialog.willDelete

        if willDelete:
            functionId = self.parent().parent().parent().parent().currentFunction["id"]

            file = open('./data/functions.json')
            data = json.load(file)
            updatedFunctions = []
            for function in data["functions"]:
                if function["id"] != functionId:
                    updatedFunctions.append(function)
            data["functions"] = updatedFunctions
            with open('./data/functions.json', 'w') as file:
                # Write the updated data back to the file
                json.dump(data, file, indent=2)

            self.parent().parent().parent().parent().parent().functionsPanel.refreshFrame() #not teamsFrame
            self.parent().parent().parent().parent().currentFunction = {
                "name": "",
                "id": "",
                "filePath": "",
                "description": "",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                } 
            }  
            self.parent().parent().parent().parent().nameInput.setText("untitled")
            self.parent().parent().parent().parent().descriptionInput.setPlainText("")
            self.parent().parent().parent().parent().editor.setPlainText("")
            self.parent().parent().parent().parent().parent().functionsPanel.resetBorders(self)

            for param in self.parent().parent().parent().parent().parent().paramPanel.parameters:
                param.deleteLater()
            self.parent().parent().parent().parent().parent().paramPanel.parameters = []

            dialog = Alert("SUCCESS", "Function deleted successfully.")
            dialog_width = 250
            dialog_height = 50

            main_window = self.parent().window()

            # Calculate the new position
            new_x = main_window.geometry().x() + main_window.geometry().width() - dialog_width - 100
            new_y = main_window.geometry().y() + main_window.geometry().height() - dialog_height - 50

            # Move the dialog to the bottom right corner of the main application window
            dialog.move(new_x, new_y)
            
            # Optional: Set dialog window flags, like making it frameless
            dialog.setWindowFlags(Qt.WindowType.FramelessWindowHint)
            
            dialog.exec()

class DeleteDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Are You Sure You Want to Delete?")
        self.setStyleSheet("background-color: #464545;") 
        self.resize(300, 150)
        # self.setGeometry(((QGuiApplication.primaryScreen().size().width()//2) - 150), ((QGuiApplication.primaryScreen().size().height()//2) - 75), 300, 150)
        layout = QVBoxLayout()
        label = QLabel("Delete this function?")
        label.setStyleSheet("""
            color: #ffffff;
            text-decoration: none;
            font-size: 12px;
        """)
        layout.addWidget(label)

        # Add a button to the dialog
        deleteButton = QPushButton("Yes, Delete")
        deleteButton.setStyleSheet("""
            background-color: transparent;
            text-decoration: underline;
            color: #ffffff;
            font-size: 12px;
            border: none;
        """)
        deleteButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        noButton = QPushButton("Cancel")
        noButton.setStyleSheet("""
            background-color: #5E5E5E;
            border-radius: 10px;
            text-align: center;
            line-height: 12px;
            color: #ffffff;
            text-decoration: none;
            font-size: 12px;
            border: none;
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


class ClickableFrame(QFrame):
    # acts as a button
    # note: we could implement multi-select functionality in the future for team creation?
    def __init__(self, currentFunction, widget, pos, parent=None):
        super().__init__(parent)
        self.functionsPanel = parent
        self.position = pos
        self.widget = widget # Keeps track of associated AgentsFrame class

        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # import any information needed from the agent for editing
        self.function = currentFunction #raw json information
        self.clicked = False #variable to keep tracked of click
        #self.setFixedWidth(190)
        self.setFixedHeight(50)
        self.setStyleSheet("""
            background-color: #464545;
            border-radius: 10;
        """)
        bold = QFont()
        bold.setBold(True)
        functionVBox = QVBoxLayout()
        self.name = currentFunction['name']
        self.nameLabel = QLabel(self.name)
        self.nameLabel.setFixedHeight(25)
        self.nameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.nameLabel.setFont(bold)
        
        functionVBox.addWidget(self.nameLabel)
        self.setLayout(functionVBox)

    def mousePressEvent(self, event):
        self.widget.functionsPanel.resetBorders(self) #unmark the borders of the previously clicked agent
        self.clicked = not self.clicked
        if self.clicked:
            self.widget.functionsPanel.clickedFunction = self
            self.widget.functionsPanel.parent().editPanel.currentFunction = self.function

            # get python code
            file = open(self.function["filePath"], "r")
            code = file.read()

            self.widget.functionsPanel.parent().editPanel.editor.setPlainText(code)
            self.widget.functionsPanel.parent().editPanel.nameInput.setText(self.function["name"])
            self.widget.functionsPanel.parent().editPanel.descriptionInput.setPlainText(self.function["description"])
            self.widget.functionsPanel.parent().editPanel.importButton.hide()
            self.widget.functionsPanel.update() 

            for param in self.widget.functionsPanel.parent().paramPanel.parameters:
                param.deleteLater()
            self.widget.functionsPanel.parent().paramPanel.parameters = []

            if hasattr(self.widget.functionsPanel.parent().paramPanel, 'spacerWidget') and self.widget.functionsPanel.parent().paramPanel.spacerWidget is not None:
                self.widget.functionsPanel.parent().paramPanel.paramBoxLayout.removeWidget(self.widget.functionsPanel.parent().paramPanel.spacerWidget)
                self.widget.functionsPanel.parent().paramPanel.spacerWidget.deleteLater()
            
            self.params = self.function["parameters"]["properties"]
            for key in self.params:
                newParamBox = ParamBox(self.params[key]["type"], key, self.params[key]["description"], self)
                self.widget.functionsPanel.parent().paramPanel.paramBoxLayout.addWidget(newParamBox)
                self.widget.functionsPanel.parent().paramPanel.parameters.append(newParamBox)
            self.widget.functionsPanel.parent().paramPanel.spacerWidget = QWidget()
            self.widget.functionsPanel.parent().paramPanel.spacerWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.widget.functionsPanel.parent().paramPanel.paramBoxLayout.addWidget(self.widget.functionsPanel.parent().paramPanel.spacerWidget)

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
        self.functionsPanel.clickableFunctions[self.position] = new_box
        self.parent().layout().replaceWidget(self, new_box)
        self.deleteLater()

class FunctionsPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Keep track of all agent boxes
        self.mainFrame = parent
        self.clickableFunctions = []
        self.setStyleSheet("background-color: #5E5E5E; border-radius: 20;")
        self.viewVBox = QVBoxLayout()
        self.functionsLabel = QLabel()
        bold = QFont()
        bold.setBold(True)
        self.functionsLabel = QLabel('Functions')
        self.functionsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.functionsLabel.setFont(bold)
        self.row = 1
        self.col = 0
        
        # Scroll section and add agent button
        self.functions = QFrame()
        self.functionsLayout = QGridLayout()

        self.functionsInfo = self.loadFunctions()
        self.functionBox(self.functionsInfo)
        self.functionScroll = QScrollArea()
        self.functionScroll.verticalScrollBar().setStyleSheet("""
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
        self.functionScroll.setWidgetResizable(True)
        self.functionScroll.setWidget(self.functions)

        # Embed scroll into view functions section
        self.viewVBox.addWidget(self.functionScroll)
        self.setLayout(self.viewVBox)

    def functionBox(self, list_of_agent_objects):
        self.functions.setStyleSheet("background-color: #5E5E5E; border-radius: 20;")
        self.functionsLayout.addWidget(self.functionsLabel, 0, 0, 1, 1)  

        addButton = AddFunctionButton()
        # addButton.setFixedSize(80, 40)
        self.functionsLayout.addWidget(addButton, 0, 1, 1, 1)

        ind = 0
        for currentFunction in list_of_agent_objects:
            obj = currentFunction
            functionBox = ClickableFrame(obj, self.mainFrame, ind, self)
            ind = ind + 1
            self.clickableFunctions.append(functionBox)
            self.functionsLayout.addWidget(functionBox, self.row, self.col)
            self.col += 1
            if self.col == 2:
                self.col = 0
                self.row += 1
        self.functionsLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.functions.setLayout(self.functionsLayout)

    def resetBorders(self, clicked_frame):
        # Reset borders of all clickable frames except the clicked frame
        for current in self.clickableFunctions:
            if current != clicked_frame:
                current.clicked = False
                current.update()

    def loadFunctions(self):
        file = open('./data/functions.json')
        data = json.load(file)
        functions = data['functions']
        return functions
        
    def refreshFrame(self):
        #not in use rn (bc of add_agent), but useful to keep around for retrieving a refreshed display of the json
        #for each clickable frame, delete (works without - may be redundant since clickable is child of panel so it deletes when panel deletes, but safer to delete than leave it hanging)
        for current in self.clickableFunctions:
            current.setParent(None)  # Remove from layout
            current.deleteLater()  # Delete widget

        new_frame = FunctionsPanel(parent=self.parent())
        # self.mainFrame.editPanel.agentFrame = new_frame
        self.mainFrame.functionsPanel = new_frame
        self.mainFrame.layout().replaceWidget(self, new_frame)
        self.deleteLater()

class PythonSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        super().__init__(parent)
        self.highlightingRules = []

        # should add as many rules as possible for best editing experience

        keywordFormat1 = QTextCharFormat()
        keywordFormat1.setForeground(QColor("light blue"))
        keywords1 = ["def", "class", "from", "import", "as", "return"]

        keywordFormat2 = QTextCharFormat()
        keywordFormat2.setForeground(QColor("orange"))
        keywords2 = [r"\(", r"\)", r"\:", r"\=", r"\>", r"\<", r"\/", r"\*"]

        keywordFormat3 = QTextCharFormat()
        keywordFormat3.setForeground(QColor("light green"))
        keywords3 = ["while", "for", "in", "break", "if", "else", "elif"]

        keywordFormat4 = QTextCharFormat()
        keywordFormat4.setForeground(QColor("#5E5E5E"))

        for keyword in keywords1:
            pattern = QRegularExpression("\\b" + keyword + "\\b")
            self.highlightingRules.append((pattern, keywordFormat1))

        for keyword in keywords2:
            pattern = QRegularExpression(keyword)
            self.highlightingRules.append((pattern, keywordFormat2))

        for keyword in keywords3:
            pattern = QRegularExpression("\\b" + keyword + "\\b")
            self.highlightingRules.append((pattern, keywordFormat3))

        pattern = QRegularExpression("#[^\n]*")
        self.highlightingRules.append((pattern, keywordFormat4))

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            iterator = pattern.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor
        self.setFixedWidth(40)

    def sizeHint(self):
        return QSize(self.codeEditor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)

class PythonCodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lineNumberArea = LineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.updateLineNumberAreaWidth(0)

    def lineNumberAreaWidth(self):
        digits = len(str(max(1, self.blockCount())))
        return 10 + self.fontMetrics().horizontalAdvance('9') * digits

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth()+30, 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        backgroundColor = QColor("#303030")
        painter.fillRect(event.rect(), backgroundColor)

        # Set the color for the right border
        borderColor = QColor("#464545")
        pen = QPen(borderColor)
        pen.setWidth(3)  # Set the pen width to 2 pixels
        painter.setPen(pen)

        # Draw the right border line
        rightBorderX = self.lineNumberArea.width() - 1  # Position for the right border
        topY = event.rect().top()
        bottomY = event.rect().bottom()
        
        # Draw a line from the top to the bottom of the currently visible area
        painter.drawLine(rightBorderX, topY, rightBorderX, bottomY)

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        # Iterate through all visible blocks
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1) + "   "
                painter.setPen(QColor("#ffffff"))
                painter.drawText(0, int(top), self.lineNumberArea.width(), self.fontMetrics().height(), Qt.AlignmentFlag.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor(QColor(255, 255, 255)).lighter(160)
            selection.format.setBackground(lineColor)
            # selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)

        self.setExtraSelections(extraSelections)

    def keyPressEvent(self, event):
        if event.key() in [Qt.Key.Key_Enter, Qt.Key.Key_Return]:
            cursor = self.textCursor()
            current_line_text = cursor.block().text()

            # Calculate current indentation level (count of leading spaces)
            indentation_level = len(current_line_text) - len(current_line_text.lstrip(' '))

            # Check if the current line ends with a colon
            additional_indent = 4 if current_line_text.rstrip().endswith(':') else 0

            super().keyPressEvent(event)  # Call the parent class method to handle the Enter key.

            # Apply the same indentation to the new line
            self.insertPlainText(' ' * (indentation_level + additional_indent))
            return
        super().keyPressEvent(event)

class CodePanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.currentFunction = {
            "name": "",
            "id": "",
            "filePath": "",
            "description": "",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }

        ### Top bar - function name, import / export buttons, save changes button (can implement auto save eventually)
        self.topBar = QFrame()
        self.topBar.setFixedHeight(170)
        self.topBarLayout = QHBoxLayout()
        

        self.inputBox = QFrame()
        self.inputBoxLayout = QVBoxLayout()
        self.inputBox.setLayout(self.inputBoxLayout)

        self.nameLabel = QLabel("Function Name:")
        self.nameInput = QLineEdit("untitled")
        self.nameInput.setStyleSheet("QLineEdit { background-color: #5E5E5E; border-radius: 10px; padding: 5px; }")

        self.buttonBox = QFrame()
        self.buttonBoxLayout = QHBoxLayout()
        self.buttonBoxLayout.setSpacing(5)
        self.buttonBox.setLayout(self.buttonBoxLayout)

        self.importButton = ImportButton(self.getCurrentFunction, self)
        self.exportButton = ExportButton(self.getCurrentFunction, self)
        self.saveButton = SaveButton()
        self.deleteButton = DeleteButton()

        self.buttonBoxLayout.addWidget(self.importButton)
        self.buttonBoxLayout.addWidget(self.exportButton)
        self.buttonBoxLayout.addWidget(self.saveButton)
        self.buttonBoxLayout.addWidget(self.deleteButton)

        self.inputBoxLayout.addWidget(self.nameLabel)
        self.inputBoxLayout.addWidget(self.nameInput)
        self.inputBoxLayout.addWidget(self.buttonBox, 1)

        self.topBarLayout.addWidget(self.inputBox, 1)

        self.descriptionBox = QFrame()
        self.descriptionBoxLayout = QVBoxLayout()
        self.descriptionLabel = QLabel("Function Description:")
        self.descriptionInput = QPlainTextEdit()
        self.descriptionInput.setStyleSheet("background-color: #5E5E5E; border-radius: 10px; padding: 5px;")
        self.descriptionBoxLayout.addWidget(self.descriptionLabel)
        self.descriptionBoxLayout.addWidget(self.descriptionInput)
        self.descriptionBox.setLayout(self.descriptionBoxLayout)


        self.topBarLayout.addWidget(self.descriptionBox, 1)
        self.topBar.setLayout(self.topBarLayout)
        
        # self.topBarLayout.addWidget(self.buttonBox)

        ### A basic Python code editor for writing functions
        self.editorLayout = QVBoxLayout()
        self.editor = PythonCodeEditor()
        font = QFont()

# Set the font family, size, and weight
        font.setFamily("Monospace")
        font.setPointSize(12)
        font.setStyleHint(QFont.StyleHint.Monospace)
        font.setFixedPitch(True)


        # Set the font of the QPlainTextEdit widget
        self.editor.setFont(font)
        self.editor.setStyleSheet("""
            background-color: #303030;
            color: #ffffff;
            padding: 20;
        """)
        self.editor.setTabStopDistance(QFontMetricsF(self.editor.font()).horizontalAdvance(' ') * 4)
        self.highlighter = PythonSyntaxHighlighter(self.editor.document())
        
        
        self.editorLayout.addWidget(self.topBar)
        self.editorLayout.addWidget(self.editor)

        self.setLayout(self.editorLayout)

    def saveFunction(self):
        functionName = self.nameInput.text()

    def getCurrentFunction(self):
        return self.currentFunction
    
class AddParameterButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Add Parameter")
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
        self.setIcon(QIcon('./assets/AddIcon.png'))
        self.setIconSize(QSize(56, 28))

class ParamBox(QFrame):
    def __init__(self, paramType=None, paramName=None, paramDescription=None, parent=None):
        super().__init__(parent)
        self.type = paramType
        self.name = paramName
        self.description = paramDescription
        self.setStyleSheet("""
            background-color: #5E5E5E;
        """)
        # self.setFixedHeight(230)
        self.paramLayout = QVBoxLayout()

        self.typeFrame = QFrame()
        self.typeFrame.setStyleSheet("""
            border-bottom: 2px solid #464545;
            border-radius: 0px;
        """)
        self.typeRow = QHBoxLayout()
        self.typeDropdown = QComboBox()
        self.typeDropdown.currentIndexChanged.connect(self.updateType)
        self.typeDropdown.setStyleSheet("QComboBox { background-color: #5E5E5E; padding: 5px; border: none; text-transform: italic; }")
        self.typeDropdown.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pythonTypes = ["string", "integer", "float", "complex", "list", "tuple", "dict", "set", "bool", "NoneType"]
        for type in self.pythonTypes:
            self.typeDropdown.addItem(type)
        
        if paramType is not None:
            paramTypeIndex = self.pythonTypes.index(paramType)
            self.typeDropdown.setCurrentIndex(paramTypeIndex)
        self.typeRow.addWidget(self.typeDropdown)

        self.deleteParameterButton = QPushButton()
        self.deleteParameterButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.deleteParameterButton.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 5px;
            }
                           
            QPushButton:hover {
                background-color: #111111;
            }
        """)
        self.deleteParameterButton.setFixedHeight(28)
        self.deleteParameterButton.setFixedWidth(28)
        self.deleteParameterButton.setIcon(QIcon('./assets/DelIcon.png'))
        self.deleteParameterButton.setIconSize(QSize(28, 28))
        self.deleteParameterButton.clicked.connect(self.deleteParamBox)
        self.typeRow.addWidget(self.deleteParameterButton)

        self.typeFrame.setLayout(self.typeRow)

        self.nameFrame = QFrame()
        self.nameFrame.setStyleSheet("""
            border-bottom: 2px solid #464545;
            border-radius: 0px;
        """)
        self.nameRow = QHBoxLayout()
        self.paramNameInput = QLineEdit(paramName)
        self.paramNameInput.textChanged.connect(self.updateName)
        self.paramNameInput.setPlaceholderText("name")
        self.paramNameInput.setStyleSheet("QLineEdit { background-color: #5E5E5E; padding: 5px; border: none; }")
        self.nameRow.addWidget(self.paramNameInput)
        self.nameFrame.setLayout(self.nameRow)

        self.descriptionFrame = QFrame()
        self.descriptionRow = QHBoxLayout()
        self.paramDescriptionInput = QLineEdit(paramDescription)
        self.paramDescriptionInput.textChanged.connect(self.updateDescription)
        self.paramDescriptionInput.setStyleSheet("QLineEdit { background-color: #5E5E5E; padding: 5px; border: none; }")
        self.paramDescriptionInput.setPlaceholderText("description")
        self.descriptionRow.addWidget(self.paramDescriptionInput)
        self.descriptionFrame.setLayout(self.descriptionRow)

        self.paramLayout.addWidget(self.typeFrame)
        self.paramLayout.addWidget(self.nameFrame)
        self.paramLayout.addWidget(self.descriptionFrame)
        self.setLayout(self.paramLayout)
    
    def deleteParamBox(self):
        parentLayout = self.parent().layout()
        if parentLayout:
            parentLayout.removeWidget(self)
            if self in self.parent().parent().parent().parent().parameters:
                # adjust json to delete specific parameter in current function
                
                self.parent().parent().parent().parent().parameters.remove(self)

    def updateType(self, index):
        self.type = self.pythonTypes[index]

    def updateName(self, text):
        self.name = text

    def updateDescription(self, text):
        self.description = text
    
class ParamPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.parameters = []

        self.setLayout(QVBoxLayout())
        self.scrollArea = QScrollArea(self)  # Create the scroll area
        self.scrollArea.setWidgetResizable(True)  # Make sure it's resizable
        self.scrollArea.verticalScrollBar().setStyleSheet("""
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
        
        self.scrollWidget = QWidget()  # This widget will hold everything that was directly in ParamPanel before
        self.paramBoxLayout = QVBoxLayout(self.scrollWidget)  # The layout is now applied to scrollWidget
        self.scrollArea.setWidget(self.scrollWidget)  # Set the scrollWidget as the widget of scrollArea
        
        self.layout().addWidget(self.scrollArea)  # Add the scrollArea to the main layout of ParamPanel

        self.verticalSpace = QFrame()
        self.paramLabel = QLabel("Function Parameters:")
        self.addParamButton = AddParameterButton(self)
        self.addParamButton.clicked.connect(self.addNewParameter)

        self.paramBoxLayout.addWidget(self.verticalSpace)
        self.paramBoxLayout.addWidget(self.paramLabel)
        self.paramBoxLayout.addWidget(self.addParamButton)

        for param in self.parameters:
            # paramBox = ParamBox(param["type"], param["name"], param["description"], self)
            self.paramBoxLayout.addWidget(param)
        self.spacerWidget = QWidget()
        self.spacerWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.paramBoxLayout.addWidget(self.spacerWidget)
        

    def addNewParameter(self):
        if hasattr(self, 'spacerWidget') and self.spacerWidget is not None:
            self.paramBoxLayout.removeWidget(self.spacerWidget)
            self.spacerWidget.deleteLater()

        newParamBox = ParamBox(None, None, None, self)
        self.paramBoxLayout.addWidget(newParamBox)
        self.parameters.append(newParamBox)
        self.spacerWidget = QWidget()
        
        self.spacerWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.paramBoxLayout.addWidget(self.spacerWidget)


class FunctionsFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__()
        self.mainFrame = parent

        # for agents display on left panel
        self.functionsPanel = FunctionsPanel(self)

        # for changing contents of right panel
        self.editPanel = CodePanel(self)

        # for editing function parameters
        self.paramPanel = ParamPanel(self)
        
        # Set tab style
        self.setStyleSheet("background-color: #464545; border-radius: 20;")
        self.mainhbox = QHBoxLayout()

        self.mainhbox.addWidget(self.functionsPanel)
        self.mainhbox.addWidget(self.editPanel)
        self.mainhbox.addWidget(self.paramPanel)

        self.mainhbox.setStretchFactor(self.functionsPanel, 3) # 3:5:2 width ratio
        self.mainhbox.setStretchFactor(self.editPanel, 5)
        self.mainhbox.setStretchFactor(self.paramPanel, 2)
        self.setLayout(self.mainhbox)
