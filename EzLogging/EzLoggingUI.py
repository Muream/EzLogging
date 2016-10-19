import sys
import PySide.QtGui as QtGui
import Ezlogging
import threading
from pyhooked import Hook, KeyboardEvent
from Config import Settings


class EzLoggingUI(QtGui.QMainWindow):
    """Base UI class."""

    def __init__(self, *args):
        super(EzLoggingUI, self).__init__(*args)

        self.settings = Settings()

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

        self.startRecordLabel = QtGui.QLabel("Start record : {}".format(self.settings.startRecord))
        self.startRecordLabel.setFont(self.labelsFont)
        self.settingsInfoLayout.addWidget(self.startRecordLabel)

        self.logTimeLabel = QtGui.QLabel("Log Time : {}".format(self.settings.logTime))
        self.logTimeLabel.setFont(self.labelsFont)
        self.settingsInfoLayout.addWidget(self.logTimeLabel)

        self.stopRecordLabel = QtGui.QLabel("Stop record : {}".format(self.settings.stopRecord))
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
        self.settingsDialog = SettingsDialog()
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
        self.f = Ezlogging.TextFile()
        hk = Hook()
        hk.handler = self.handle_events
        thread = threading.Thread(target=hk.hook)
        thread.start()


class SettingsDialog(QtGui.QDialog):

    def __init__(self, *args):
        super(SettingsDialog, self).__init__(*args)
        self.settings = Settings()
        self.setupUI()

    def setupUI(self):

        self.setWindowTitle('Settings')
        self.setMinimumSize(480, 300)
        self.setMaximumSize(480, 300)

        self.setModal(True)

        self.mainLayout = QtGui.QHBoxLayout()
        self.setLayout(self.mainLayout)

        self.settings_layout()

    def settings_layout(self):
        self.settingsLayout = QtGui.QVBoxLayout()
        self.mainLayout.addLayout(self.settingsLayout)

        self.video_path_layout()
        self.videoFormat_layout()
        self.hotkeys_layout()
        self.ffmpeg_path_layout()

    def video_path_layout(self):
        self.videoPathLayout = QtGui.QHBoxLayout()
        self.settingsLayout.addLayout(self.videoPathLayout)

        self.videoPathLabel = QtGui.QLabel('Recordings Location')
        self.videoPathLayout.addWidget(self.videoPathLabel)

        self.videoPathLineEdit = QtGui.QLineEdit()
        self.videoPathLineEdit.setText(self.settings.videoPath)
        self.videoPathLayout.addWidget(self.videoPathLineEdit)

        self.videoPathBrowseButton = QtGui.QPushButton('Browse')
        self.videoPathBrowseButton.released.connect(self.browse_videos)
        self.videoPathLayout.addWidget(self.videoPathBrowseButton)

    def videoFormat_layout(self):
        self.videoFormatLayout = QtGui.QHBoxLayout()
        self.settingsLayout.addLayout(self.videoFormatLayout)

        self.videoPathLabel = QtGui.QLabel('Recordings Format')
        self.videoFormatLayout.addWidget(self.videoPathLabel)

        self.videoFormatComboBox = QtGui.QComboBox()
        self.videoFormatComboBox.addItem("mp4")
        self.videoFormatComboBox.addItem("mov")
        self.videoFormatComboBox.addItem("mkv")
        self.videoFormatComboBox.addItem("flv")
        index = self.videoFormatComboBox.findText(self.settings.videoFormat)
        self.videoFormatComboBox.setCurrentIndex(index)
        self.videoFormatLayout.addWidget(self.videoFormatComboBox)

    def hotkeys_layout(self):
        self.hotkeysLayout = QtGui.QHBoxLayout()
        self.settingsLayout.addLayout(self.hotkeysLayout)

        self.startRecordLabel = QtGui.QLabel('Start Recording')
        self.hotkeysLayout.addWidget(self.startRecordLabel)

        self.startRecordButton = QtGui.QPushButton(self.settings.startRecord)
        self.hotkeysLayout.addWidget(self.startRecordButton)

        self.startRecordLabel = QtGui.QLabel('Log Time')
        self.hotkeysLayout.addWidget(self.startRecordLabel)
        self.logTimeButton = QtGui.QPushButton(self.settings.logTime)
        self.hotkeysLayout.addWidget(self.logTimeButton)

        self.startRecordLabel = QtGui.QLabel('Stop Recording')
        self.hotkeysLayout.addWidget(self.startRecordLabel)
        self.stopRecordButton = QtGui.QPushButton(self.settings.stopRecord)
        self.hotkeysLayout.addWidget(self.stopRecordButton)

    def ffmpeg_path_layout(self):
        self.ffmpegPathLayout = QtGui.QHBoxLayout()
        self.settingsLayout.addLayout(self.ffmpegPathLayout)

        self.ffmpegPathLabel = QtGui.QLabel('FFMPEG Location')
        self.ffmpegPathLayout.addWidget(self.ffmpegPathLabel)

        self.ffmpegPathLineEdit = QtGui.QLineEdit()
        self.ffmpegPathLineEdit.setText(self.settings.ffmpeg)
        self.ffmpegPathLayout.addWidget(self.ffmpegPathLineEdit)

        self.ffmpegPathBrowseButton = QtGui.QPushButton('Browse')
        self.ffmpegPathBrowseButton.released.connect(self.browse_ffmpeg)
        self.ffmpegPathLayout.addWidget(self.ffmpegPathBrowseButton)

    def browse_videos(self):
        self.browseVideosFileDialog = QtGui.QFileDialog()
        self.browseVideosFileDialog.setModal(True)
        directory = self.browseVideosFileDialog.getExistingDirectory()
        self.videoPathLineEdit.setText(directory)

    def browse_ffmpeg(self):
        self.browseFfmpegFileDialog = QtGui.QFileDialog()
        self.browseFfmpegFileDialog.setModal(True)
        self.browseFfmpegFileDialog.setFileMode(QtGui.QFileDialog.ExistingFile)
        self.browseFfmpegFileDialog.setFilter("Executable (*.exe)")
        self.browseFfmpegFileDialog.exec_()
        filename = self.browseFfmpegFileDialog.selectedFiles()[0]
        self.ffmpegPathLineEdit.setText(filename)


def show():
    """Open up the UI."""
    app = QtGui.QApplication(sys.argv)

    ui = EzLoggingUI()
    ui.show()

    app.exec_()
    sys.exit()

if __name__ == '__main__':
    show()
