import sys
import PySide.QtGui as QtGui
# import keyboard
from pynput import keyboard
import threading

from EzLogging.core.timeLogger import TimeLogger
from EzLogging.core.clipLogger import clipLogger
from EzLogging.core.config import config
from EzLogging.ui.settingsDialog import SettingsDialog


class EzLoggingUI(QtGui.QMainWindow):
    "Base UI Class"

    def __init__(self, *args):
        super(EzLoggingUI, self).__init__(*args)

        if config._data == {}:
            self.launch_settings_dialog()

        self.setup_ui()
        self.time_logger = TimeLogger(ui=self)

    # def closeEvent(self, *args, **kwargs):
    #     self.listener.stop()

    def setup_ui(self):
        self.setWindowTitle("EzLogging")
        self.setMinimumSize(500, 500)

        self.create_menus()
        self.create_central_widget()
        self.create_log_output()
        self.listen_hotkeys()

    def launch_settings_dialog(self):
        self.settingsDialog = SettingsDialog(self)
        self.settingsDialog.show()

    def start_cliplogger(self):
        clipLogger(self)

    def create_menus(self):
        self.menuBar = self.menuBar()
        self.create_file_menu()

    def create_file_menu(self):
        self.fileMenu = self.menuBar.addMenu('&File')
        self.create_settings_menu_actions()
        self.create_cliplogger_menu_actions()

    def create_settings_menu_actions(self):
        self.settingsAction = QtGui.QAction('&Settings', self)
        self.settingsAction.triggered.connect(self.launch_settings_dialog)
        self.fileMenu.addAction(self.settingsAction)

    def create_cliplogger_menu_actions(self):
        self.clipLoggerAction = QtGui.QAction('&Log Clips', self)
        self.clipLoggerAction.triggered.connect(self.start_cliplogger)
        self.fileMenu.addAction(self.clipLoggerAction)

    def create_central_widget(self):
        self.setCentralWidget(QtGui.QWidget())
        self.centralWidget().setLayout(QtGui.QVBoxLayout())

    def create_log_output(self):
        # the log output
        self.logOutput = QtGui.QTextEdit()
        self.logOutput.setReadOnly(True)

        self.logOutputLayout = QtGui.QHBoxLayout()
        self.logOutputLayout.addWidget(self.logOutput)
        self.centralWidget().layout().addLayout(self.logOutputLayout)

    def print_log_output(self, text):
        self.logOutput.append(text)
        self.logOutput.ensureCursorVisible()

    def handle_events(self):
        with keyboard.Listener(on_release=self.on_release) as listener:
            listener.join()

    def listen_hotkeys(self):
        hotkeyThread = threading.Thread(target=self.handle_events)
        hotkeyThread.daemon = True
        hotkeyThread.start()

    def on_release(self, key):
        if key == str_to_keycode[config.start_record]:
            self.time_logger.create_file()
        elif key == str_to_keycode[config.stop_record]:
            self.time_logger.close_file()
        elif key == str_to_keycode[config.log_time]:
            self.time_logger.log_time()


def show():
    app = QtGui.QApplication(sys.argv)

    ui = EzLoggingUI()
    ui.show()

    app.exec_()
    sys.exit()


str_to_keycode = {
    'f1': keyboard.Key.f1,
    'f2': keyboard.Key.f2,
    'f3': keyboard.Key.f3,
    'f4': keyboard.Key.f4,
    'f5': keyboard.Key.f5,
    'f6': keyboard.Key.f6,
    'f7': keyboard.Key.f7,
    'f8': keyboard.Key.f8,
    'f9': keyboard.Key.f9,
    'f10': keyboard.Key.f10,
    'f11': keyboard.Key.f11,
    'f12': keyboard.Key.f12,
    'f13': keyboard.Key.f13,
    'f14': keyboard.Key.f14,
    'f15': keyboard.Key.f15,
    'f16': keyboard.Key.f16,
    'f17': keyboard.Key.f17,
    'f18': keyboard.Key.f18,
    'f19': keyboard.Key.f19,
    'f20': keyboard.Key.f20,
    'f20': keyboard.Key.f20,
    'F1': keyboard.Key.f1,
    'F2': keyboard.Key.f2,
    'F3': keyboard.Key.f3,
    'F4': keyboard.Key.f4,
    'F5': keyboard.Key.f5,
    'F6': keyboard.Key.f6,
    'F7': keyboard.Key.f7,
    'F8': keyboard.Key.f8,
    'F9': keyboard.Key.f9,
    'F10': keyboard.Key.f10,
    'F11': keyboard.Key.f11,
    'F12': keyboard.Key.f12,
    'F13': keyboard.Key.f13,
    'F14': keyboard.Key.f14,
    'F15': keyboard.Key.f15,
    'F16': keyboard.Key.f16,
    'F17': keyboard.Key.f17,
    'F18': keyboard.Key.f18,
    'F19': keyboard.Key.f19,
    'F20': keyboard.Key.f20,
    'F20': keyboard.Key.f20,
}

if __name__ == '__main__':
    show()
