import sys
import threading
import os

from pyhooked import Hook, KeyboardEvent
import PySide.QtGui as QtGui

import Ezlogging
from Config import Settings
import settingsDialog


class EzLoggingUI(QtGui.QMainWindow):
    """Base UI class."""

    def __init__(self, *args):
        super(EzLoggingUI, self).__init__(*args)

        self.settings = Settings()

        if os.path.isfile('Config.cfg'):
            self.settings.read_config()
        else:
            self.launch_settings_dialog()

        self.setup_ui()

    def setup_ui(self):

        self.setWindowTitle('EzLogging')
        self.setMinimumSize(500, 500)

        self.create_menus()
        self.create_central_widget()
        self.create_settings_info()
        self.create_log_output()
        self.hotkeys()

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

    def create_settings_menu_actions(self):
        """
        """
        self.settingsAction = QtGui.QAction('&Settings', self)
        self.settingsAction.triggered.connect(self.launch_settings_dialog)

        self.fileMenu.addAction(self.settingsAction)

    def create_central_widget(self):
        """
        """
        self.setCentralWidget(QtGui.QWidget())
        self.centralWidget().setLayout(QtGui.QVBoxLayout())

    def create_settings_info(self):
        self.settingsInfoLayout = QtGui.QVBoxLayout()

        self.labelsFont = QtGui.QFont()
        self.labelsFont.setPointSize(10)

        self.startRecordLabel = QtGui.QLabel("Start recording : {}".format(str(self.settings.startRecord)))
        self.startRecordLabel.setFont(self.labelsFont)
        self.settingsInfoLayout.addWidget(self.startRecordLabel)

        self.logTimeLabel = QtGui.QLabel("Log Time : {}".format(str(self.settings.logTime)))
        self.logTimeLabel.setFont(self.labelsFont)
        self.settingsInfoLayout.addWidget(self.logTimeLabel)

        self.stopRecordLabel = QtGui.QLabel("Stop recording : {}".format(str(self.settings.stopRecord)))
        self.stopRecordLabel.setFont(self.labelsFont)
        self.settingsInfoLayout.addWidget(self.stopRecordLabel)

        self.centralWidget().layout().addLayout(self.settingsInfoLayout)

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

    def handle_events(self, args):
        """Global hotkeys actions"""
        if isinstance(args, KeyboardEvent):
            if args.current_key == self.settings.startRecord and args.event_type == 'key down':

                self.f.createfile(self)
            if args.current_key == self.settings.logTime and args.event_type == 'key down':
                self.f.writetime(self)
            if args.current_key == self.settings.stopRecord and args.event_type == 'key down':
                self.f.closefile(self)

    def hotkeys(self):
        """Global hotkeys setup."""
        self.f = Ezlogging.TextFile(self.settings)
        hk = Hook()
        hk.handler = self.handle_events
        thread = threading.Thread(target=hk.hook)
        thread.start()

    def update_ui(self):
        self.startRecordLabel.setText("Start recording : {}".format(str(self.settings.startRecord)))

        self.logTimeLabel.setText("Log Time : {}".format(str(self.settings.logTime)))

        self.stopRecordLabel.setText("Stop recording : {}".format(str(self.settings.stopRecord)))


def show():
    """Open up the UI."""
    app = QtGui.QApplication(sys.argv)

    ui = EzLoggingUI()
    ui.show()

    app.exec_()
    sys.exit()

if __name__ == '__main__':
    show()
