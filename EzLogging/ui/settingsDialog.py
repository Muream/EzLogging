from PySide import QtGui
from hotkeyPushButton import HotkeyPushButton


class SettingsDialog(QtGui.QDialog):

    def __init__(self, cfg, parentUI, *args):
        super(SettingsDialog, self).__init__(*args)
        self.cfg = cfg
        self.parentUI = parentUI
        self.setup_ui()

    def setup_ui(self):

        self.setWindowTitle('Settings')
        self.setMinimumSize(480, 300)
        self.setMaximumSize(480, 300)

        self.setModal(True)

        self.mainLayout = QtGui.QHBoxLayout()
        self.setLayout(self.mainLayout)

        self.settings_layout()
        self.fill_settings_ui()

    def settings_layout(self):
        self.settingsLayout = QtGui.QVBoxLayout()
        self.mainLayout.addLayout(self.settingsLayout)

        self.video_path_layout()
        self.videoFormat_layout()
        self.hotkeys_layout()

        self.ffmpeg_path_layout()
        self.trim_settings()
        self.apply_settings_button()

    def video_path_layout(self):
        self.videoPathLayout = QtGui.QHBoxLayout()
        self.settingsLayout.addLayout(self.videoPathLayout)

        self.videoPathLabel = QtGui.QLabel('Recordings Location')
        self.videoPathLayout.addWidget(self.videoPathLabel)

        self.videoPathLineEdit = QtGui.QLineEdit()

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

        self.videoFormatLayout.addWidget(self.videoFormatComboBox)

    def hotkeys_layout(self):
        self.hotkeysLayout = QtGui.QHBoxLayout()
        self.settingsLayout.addLayout(self.hotkeysLayout)

        self.startRecordLabel = QtGui.QLabel('Start Recording')
        self.hotkeysLayout.addWidget(self.startRecordLabel)

        self.startRecordButton = HotkeyPushButton()
        self.hotkeysLayout.addWidget(self.startRecordButton)

        self.startRecordLabel = QtGui.QLabel('Log Time')
        self.hotkeysLayout.addWidget(self.startRecordLabel)
        self.logTimeButton = HotkeyPushButton()
        self.hotkeysLayout.addWidget(self.logTimeButton)

        self.startRecordLabel = QtGui.QLabel('Stop Recording')
        self.hotkeysLayout.addWidget(self.startRecordLabel)
        self.stopRecordButton = HotkeyPushButton()
        self.hotkeysLayout.addWidget(self.stopRecordButton)

    def ffmpeg_path_layout(self):
        self.ffmpegPathLayout = QtGui.QHBoxLayout()
        self.settingsLayout.addLayout(self.ffmpegPathLayout)

        self.ffmpegPathLabel = QtGui.QLabel('FFMPEG Location')
        self.ffmpegPathLayout.addWidget(self.ffmpegPathLabel)

        self.ffmpegPathLineEdit = QtGui.QLineEdit()
        self.ffmpegPathLayout.addWidget(self.ffmpegPathLineEdit)

        self.ffmpegPathBrowseButton = QtGui.QPushButton('Browse')
        self.ffmpegPathBrowseButton.released.connect(self.browse_ffmpeg)
        self.ffmpegPathLayout.addWidget(self.ffmpegPathBrowseButton)

    def trim_settings(self):
        self.trimSettingsLayout = QtGui.QHBoxLayout()
        self.settingsLayout.addLayout(self.trimSettingsLayout)

        self.trimBeforeLabel = QtGui.QLabel("Time before timecode (s)")
        self.trimSettingsLayout.addWidget(self.trimBeforeLabel)

        self.trimBeforeSpinBox = QtGui.QSpinBox()
        self.trimBeforeSpinBox.setMinimum(0)
        self.trimSettingsLayout.addWidget(self.trimBeforeSpinBox)

        self.trimAfterLabel = QtGui.QLabel("Time after timecode (s)")
        self.trimSettingsLayout.addWidget(self.trimAfterLabel)

        self.trimAfterSpinBox = QtGui.QSpinBox()
        self.trimAfterSpinBox.setMinimum(0)
        self.trimSettingsLayout.addWidget(self.trimAfterSpinBox)

    def apply_settings_button(self):
        self.applySettingsLayout = QtGui.QHBoxLayout()
        self.settingsLayout.addLayout(self.applySettingsLayout)

        self.applySettingsButton = QtGui.QPushButton("Apply")
        self.applySettingsButton.released.connect(self.apply_settings)

        self.applySettingsLayout.addWidget(self.applySettingsButton)

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

    def fill_settings_ui(self):
        self.videoPathLineEdit.setText(str(self.cfg.videoPath))
        index = self.videoFormatComboBox.findText(str(self.cfg.videoFormat))
        self.videoFormatComboBox.setCurrentIndex(index)

        self.startRecordButton.setText(str(self.cfg.startRecord))
        self.stopRecordButton.setText(str(self.cfg.stopRecord))
        self.logTimeButton.setText(str(self.cfg.logTime))

        self.ffmpegPathLineEdit.setText(str(self.cfg.ffmpegPath))

        self.trimBeforeSpinBox.setValue(float(self.cfg.cutBefore))
        self.trimAfterSpinBox.setValue(float(self.cfg.cutAfter))

    def apply_settings(self):
        self.startRecordHotkey = self.startRecordButton.hotkey
        self.stopRecordHotkey = self.stopRecordButton.hotkey
        self.logTimeHotkey = self.logTimeButton.hotkey

        self.cfg.set_config(
            videoPath=self.videoPathLineEdit.text(),
            videoFormat=self.videoFormatComboBox.currentText(),
            ffmpegPath=self.ffmpegPathLineEdit.text(),
            cutBefore=self.trimBeforeSpinBox.value(),
            cutAfter=self.trimAfterSpinBox.value(),
            startRecord=self.startRecordHotkey,
            stopRecord=self.stopRecordHotkey,
            logTime=self.logTimeHotkey
        )
        self.parentUI.update_ui()
