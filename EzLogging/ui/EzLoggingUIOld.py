import sys
import threading
import os

# from pyhooked import Hook, KeyboardEvent
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore

# import Ezlogging
# import AutoLog
# import gameDetector
# from Config import Settings
# import settingsDialog
# import addGameDialog


class EzLoggingUI(QtGui.QMainWindow):
    """Base UI class."""

    def __init__(self, *args):
        super(EzLoggingUI, self).__init__(*args)

        # self.settings = Settings()
        self.currentGame = None

        # if os.path.isfile('Config.cfg'):
        #     self.settings.read_config()
        # else:
        #     self.launch_settings_dialog()
        self.setup_ui()

    def setup_ui(self):

        self.setWindowTitle('EzLogging')
        self.setMinimumSize(500, 500)

        self.create_menus()
        self.create_central_widget()
        # self.create_info_bar()
        # self.create_games_bar()
        self.create_log_output()
        # self.hotkeys()

    def create_menus(self):
        """
        """
        self.create_file_menu()

    def create_file_menu(self):
        """
        """
        self.menuBar = self.menuBar()
        self.fileMenu = self.menuBar.addMenu('&File')
        self.create_settings_menu_actions()
        self.create_autoLog_menu_actions()

    def create_settings_menu_actions(self):
        """
        """
        self.settingsAction = QtGui.QAction('&Settings', self)
        self.settingsAction.triggered.connect(self.launch_settings_dialog)

        self.fileMenu.addAction(self.settingsAction)

    def create_autoLog_menu_actions(self):
        """
        """
        self.autoLogAction = QtGui.QAction('&AutoLog', self)
        self.autoLogAction.triggered.connect(self.start_autolog)

        self.fileMenu.addAction(self.autoLogAction)

    def create_central_widget(self):
        """
        """
        self.setCentralWidget(QtGui.QWidget())
        self.centralWidget().setLayout(QtGui.QVBoxLayout())

    def create_info_bar(self):
        self.infoBarLayout = QtGui.QHBoxLayout()
        self.infoBarLayout.setAlignment(QtCore.Qt.AlignLeft)

        self.startRecordLabel = QtGui.QLabel("Start recording : {}".format(str(self.settings.startRecord)))
        self.startRecordLabel.setFont(self.labelsFont)
        self.infoBarLayout.addWidget(self.startRecordLabel)

        self.logTimeLabel = QtGui.QLabel("Log Time : {}".format(str(self.settings.logTime)))
        self.logTimeLabel.setFont(self.labelsFont)
        self.infoBarLayout.addWidget(self.logTimeLabel)

        self.stopRecordLabel = QtGui.QLabel("Stop recording : {}".format(str(self.settings.stopRecord)))
        self.stopRecordLabel.setFont(self.labelsFont)
        self.infoBarLayout.addWidget(self.stopRecordLabel)

    # def create_games_bar(self):
    #     # Games Bar Layout
    #     self.gamesBarLayout = QtGui.QHBoxLayout()

    #     # Running Games Layout
    #     self.gamesBarLayout = QtGui.QHBoxLayout()
    #     self.gamesBarLayout.setAlignment(QtCore.Qt.AlignLeft)

    #     # Font Stuff
    #     self.labelsFont = QtGui.QFont()
    #     self.labelsFont.setPointSize(10)

    #     # Running games Combo Box
    #     self.runningGamesComboBox = QtGui.QComboBox()
    #     self.gamesBarLayout.addWidget(self.runningGamesComboBox)

    #     self.refreshGamesButton = QtGui.QPushButton("Refresh")
    #     self.refreshGamesButton.released.connect(self.update_running_games)
    #     self.gamesBarLayout.addWidget(self.refreshGamesButton)
    #     self

    #     # Add Game Button
    #     self.addGameButton = QtGui.QPushButton("Add Game")
    #     self.addGameButton.released.connect(self.add_game)
    #     self.gamesBarLayout.addWidget(self.addGameButton)

    #     self.update_running_games()

    #     self.centralWidget().layout().addLayout(self.gamesBarLayout)

    def create_log_output(self):
        """The log output, where all the info are printed."""

        # the log output
        self.logOutput = QtGui.QTextEdit()
        self.logOutput.setReadOnly(True)

        # font stuff
        self.logOuputFont = QtGui.QFont()
        self.logOuputFont.setPointSize(14)
        self.logOutput.setCurrentFont(self.logOuputFont)

        # layout stuff
        self.logOutputLayout = QtGui.QHBoxLayout()
        self.logOutputLayout.addWidget(self.logOutput)
        self.centralWidget().layout().addLayout(self.logOutputLayout)

    def launch_settings_dialog(self):
        self.settingsDialog = settingsDialog.SettingsDialog(self.settings, self)
        self.settingsDialog.show()

    def start_autolog(self):
        autoLogThread = threading.Thread(target=AutoLog.main, args=(self.settings, self))
        autoLogThread.daemon = True
        autoLogThread.start()

    # def handle_events(self, args):
    #     """Global hotkeys actions"""
    #     if isinstance(args, KeyboardEvent):
    #         if args.current_key == self.settings.startRecord and args.event_type == 'key down':
    #             self.f.createfile(self)
    #         if args.current_key == self.settings.logTime and args.event_type == 'key down':
    #             self.f.writetime(self)
    #         if args.current_key == self.settings.stopRecord and args.event_type == 'key down':
    #             self.f.closefile(self)
    #     return

    # def hotkeys(self):
    #     """Global hotkeys setup."""
    #     self.f = Ezlogging.TextFile(self.settings)
    #     hk = Hook()
    #     hk.handler = self.handle_events
    #     hotkeyThread = threading.Thread(target=hk.hook)
    #     hotkeyThread.daemon = True
    #     hotkeyThread.start()

    def update_ui(self):
        self.settings.read_config()
        # self.startRecordLabel.setText("Start recording : {}".format(str(self.settings.startRecord)))

        # self.logTimeLabel.setText("Log Time : {}".format(str(self.settings.logTime)))

        # self.stopRecordLabel.setText("Stop recording : {}".format(str(self.settings.stopRecord)))

    # def update_running_games(self):
    #     games = gameDetector.running_games()
    #     print games

    #     self.runningGamesComboBox.clear()
    #     for game in games:
    #         self.runningGamesComboBox.addItem(game)
    #     if self.currentGame in games:
    #         index = self.runningGamesComboBox.findText(self.currentGame)
    #         self.runningGamesComboBox.setCurrentIndex(index)
    #     self.currentGame = self.runningGamesComboBox.currentText()

    # def add_game(self):
    #     self.addGameDialog = addGameDialog.AddGameDialog(self)
    #     self.addGameDialog.show()


def show():
    """Open up the UI."""
    app = QtGui.QApplication(sys.argv)

    ui = EzLoggingUI()
    ui.show()

    app.exec_()
    sys.exit()

if __name__ == '__main__':
    show()
