import os
from PySide6 import QtWidgets
from EzLogging.ui.hotkeyPushButton import HotkeyPushButton
from EzLogging.core.config import config


class SettingsDialog(QtWidgets.QDialog):

    def __init__(self, parentUI, *args):
        super(SettingsDialog, self).__init__(*args)
        self.parentUI = parentUI
        self.setup_ui()

    def setup_ui(self):

        self.setWindowTitle('Settings')
        self.setMinimumSize(480, 300)
        self.setMaximumSize(480, 300)

        self.setModal(True)

        self.mainLayout = QtWidgets.QHBoxLayout()
        self.setLayout(self.mainLayout)

        self.settings_layout()
        self.fill_settings_ui()

        styleFile = os.path.join(os.path.dirname(__file__), "stylesheet.qss")
        with open(styleFile, "r") as f:
            self.setStyleSheet(f.read())

    def settings_layout(self):
        self.settingsLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(self.settingsLayout)

        self.video_path_layout()
        self.videoFormat_layout()
        self.hotkeys_layout()

        self.trim_settings()
        # self.csgo_layout()
        self.apply_settings_button()

    def video_path_layout(self):
        self.videoPathLayout = QtWidgets.QHBoxLayout()
        self.settingsLayout.addLayout(self.videoPathLayout)

        self.videoPathLabel = QtWidgets.QLabel('Recordings Location')
        self.videoPathLayout.addWidget(self.videoPathLabel)

        self.videoPathLineEdit = QtWidgets.QLineEdit()

        self.videoPathLayout.addWidget(self.videoPathLineEdit)

        self.videoPathBrowseButton = QtWidgets.QPushButton('Browse')
        self.videoPathBrowseButton.released.connect(self.browse_videos)
        self.videoPathLayout.addWidget(self.videoPathBrowseButton)

    def videoFormat_layout(self):
        self.videoFormatLayout = QtWidgets.QHBoxLayout()
        self.settingsLayout.addLayout(self.videoFormatLayout)

        self.videoPathLabel = QtWidgets.QLabel('Recordings Format')
        self.videoFormatLayout.addWidget(self.videoPathLabel)

        self.videoFormatLineEdit = QtWidgets.QLineEdit("mp4")

        self.videoFormatLayout.addWidget(self.videoFormatLineEdit)

    def hotkeys_layout(self):
        self.hotkeysLayout = QtWidgets.QHBoxLayout()
        self.settingsLayout.addLayout(self.hotkeysLayout)

        self.startRecordLabel = QtWidgets.QLabel('Start Recording')
        self.hotkeysLayout.addWidget(self.startRecordLabel)

        self.startRecordButton = HotkeyPushButton(str(config.start_record))
        self.hotkeysLayout.addWidget(self.startRecordButton)

        self.logTimeRecordLabel = QtWidgets.QLabel('Log Time')
        self.hotkeysLayout.addWidget(self.logTimeRecordLabel)
        self.logTimeButton = HotkeyPushButton(str(config.log_time))
        self.hotkeysLayout.addWidget(self.logTimeButton)

        self.stopRecordLabel = QtWidgets.QLabel('Stop Recording')
        self.hotkeysLayout.addWidget(self.stopRecordLabel)
        self.stopRecordButton = HotkeyPushButton(str(config.stop_record))
        self.hotkeysLayout.addWidget(self.stopRecordButton)

    def trim_settings(self):
        self.trimSettingsLayout = QtWidgets.QHBoxLayout()
        self.settingsLayout.addLayout(self.trimSettingsLayout)

        self.trimBeforeLabel = QtWidgets.QLabel("Time before timecode (s)")
        self.trimSettingsLayout.addWidget(self.trimBeforeLabel)

        self.trimBeforeSpinBox = QtWidgets.QSpinBox()
        self.trimBeforeSpinBox.setMinimum(0)
        self.trimSettingsLayout.addWidget(self.trimBeforeSpinBox)

        self.trimAfterLabel = QtWidgets.QLabel("Time after timecode (s)")
        self.trimSettingsLayout.addWidget(self.trimAfterLabel)

        self.trimAfterSpinBox = QtWidgets.QSpinBox()
        self.trimAfterSpinBox.setMinimum(0)
        self.trimSettingsLayout.addWidget(self.trimAfterSpinBox)

    def apply_settings_button(self):
        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.settingsLayout.addLayout(self.buttons_layout)

        self.apply_button = QtWidgets.QPushButton("Apply")
        self.apply_button.released.connect(self.apply_settings)

        self.ok_button = QtWidgets.QPushButton("Ok")
        self.ok_button.released.connect(self.apply_and_close)

        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.released.connect(self.close_dialog)

        self.buttons_layout.addWidget(self.ok_button)
        self.buttons_layout.addWidget(self.cancel_button)
        self.buttons_layout.addWidget(self.apply_button)

    def browse_videos(self):
        self.browseVideosFileDialog = QtWidgets.QFileDialog()
        self.browseVideosFileDialog.setModal(True)
        directory = self.browseVideosFileDialog.getExistingDirectory()
        self.videoPathLineEdit.setText(directory)


    # def browse_csgo_demos(self):
    #     self.browseVideosFileDialog = QtWidgets.QFileDialog()
    #     self.browseVideosFileDialog.setModal(True)
    #     directory = self.browseVideosFileDialog.getExistingDirectory()
    #     self.csgo_demos_path_line_edit.setText(directory)

    def fill_settings_ui(self):
        self.videoPathLineEdit.setText(str(config.video_path))
        self.videoFormatLineEdit.setText(str(config.video_format))

        self.startRecordButton.setText(str(config.start_record))
        self.stopRecordButton.setText(str(config.stop_record))
        self.logTimeButton.setText(str(config.log_time))


        cut_before = config.cut_before if config.cut_before else 0
        cut_after = config.cut_after if config.cut_after else 0
        self.trimBeforeSpinBox.setValue(float(cut_before))
        self.trimAfterSpinBox.setValue(float(cut_after))

        # self.csgo_manage_demos_checkbox.setChecked(bool(config.csgo_manage_demos))
        # self.csgo_demos_path_line_edit.setText(str(config.csgo_demos_path))
        # self.csgo_copy_demos_checkbox.setChecked(bool(config.csgo_copy_demos))

    def apply_settings(self):
        self.startRecordHotkey = self.startRecordButton.hotkey
        self.stopRecordHotkey = self.stopRecordButton.hotkey
        self.logTimeHotkey = self.logTimeButton.hotkey

        config.video_path  =  self.videoPathLineEdit.text()
        config.video_format = self.videoFormatLineEdit.text()
        config.cut_before = self.trimBeforeSpinBox.value()
        config.cut_after = self.trimAfterSpinBox.value()
        config.start_record = self.startRecordHotkey
        config.stop_record = self.stopRecordHotkey
        config.log_time = self.logTimeHotkey
        # config.csgo_manage_demos = self.csgo_manage_demos_checkbox.isChecked()
        # config.csgo_demos_path = self.csgo_demos_path_line_edit.text()
        # config.csgo_copy_demos = self.csgo_copy_demos_checkbox.isChecked()

    def apply_and_close(self):
        self.apply_settings()
        self.close_dialog()

    def close_dialog(self):
        self.close()

    # def csgo_layout(self):
    #     self.csgo_layout = QtWidgets.QVBoxLayout()
    #     self.settingsLayout.addLayout(self.csgo_layout)

    #     csgo_manage_demos_layout = QtWidgets.QHBoxLayout()
    #     self.csgo_layout.addLayout(csgo_manage_demos_layout)

    #     csgo_manage_demos_label = QtWidgets.QLabel('Manage CS:GO demos')
    #     self.csgo_manage_demos_checkbox = QtWidgets.QCheckBox()
    #     csgo_manage_demos_layout.addWidget(csgo_manage_demos_label)
    #     csgo_manage_demos_layout.addWidget(self.csgo_manage_demos_checkbox)

    #     csgo_demos_path_layout = QtWidgets.QHBoxLayout()
    #     self.csgo_layout.addLayout(csgo_demos_path_layout)

    #     csgo_demos_path_label = QtWidgets.QLabel('CS:GO demos path')
    #     csgo_demos_path_layout.addWidget(csgo_demos_path_label)

    #     self.csgo_demos_path_line_edit = QtWidgets.QLineEdit()
    #     csgo_demos_path_layout.addWidget(self.csgo_demos_path_line_edit)

    #     csgo_demos_path_browse_button = QtWidgets.QPushButton('Browse')
    #     csgo_demos_path_browse_button.released.connect(self.browse_csgo_demos)
    #     csgo_demos_path_layout.addWidget(csgo_demos_path_browse_button)

    #     csgo_copy_demos_layout = QtWidgets.QHBoxLayout()
    #     self.csgo_layout.addLayout(csgo_copy_demos_layout)
    #     csgo_copy_demos_label = QtWidgets.QLabel('Copy the demos next the videos')
    #     self.csgo_copy_demos_checkbox = QtWidgets.QCheckBox()
    #     csgo_copy_demos_layout.addWidget(csgo_copy_demos_label)
    #     csgo_copy_demos_layout.addWidget(self.csgo_copy_demos_checkbox)
