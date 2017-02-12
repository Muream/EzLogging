import sys
import PySide.QtGui as QtGui
import keyboard
import threading

sys.path.append("/home/muream/github/EzLogging/EzLogging")

from core.timeLogger import TimeLogger
from utils import config


class EzLoggingUI(QtGui.QMainWindow):
    "Base UI Class"

    def __init__(self, *args):
        super(EzLoggingUI, self).__init__(*args)

        self.cfg = config.read_config()

        self.setup_ui()

    def setup_ui(self):

        self.setWindowTitle("EzLogging")
        self.setMinimumSize(500, 500)

        self.create_central_widget()
        self.create_log_output()
        self.listen_hotkeys()

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
        timeLogger = TimeLogger(self.cfg)

        keyboard.add_hotkey(self.cfg['log time'], timeLogger.log_time, args=[self])
        keyboard.add_hotkey(self.cfg['start record'], timeLogger.create_file, args=[self])
        keyboard.add_hotkey(self.cfg['stop record'], timeLogger.close_file, args=[self])
        keyboard.wait()

    def listen_hotkeys(self):
        hotkeyThread = threading.Thread(target=self.handle_events)
        hotkeyThread.daemon = True
        hotkeyThread.start()


def show():
    app = QtGui.QApplication(sys.argv)

    ui = EzLoggingUI()
    ui.show()

    app.exec_()
    sys.exit()


if __name__ == '__main__':
    show()
