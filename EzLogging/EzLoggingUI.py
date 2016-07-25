import sys
import PySide.QtGui as _qt


class EzLoggingUI(_qt.QMainWindow):
    """Base UI class."""

    def __init__(self, *args):
        super(EzLoggingUI, self).__init__(*args)

        self.setWindowTitle('EzLogging')
        self._initialize()

    def _initialize(self):
        """
        """
        self._createMenus()

    def _createMenus(self):
        """
        """
        self._createSettingsMenu()

    def _createSettingsMenu(self):
        """
        """
        self.menuBar().addMenu('&Settings')
        self._createSettingsMenuActions()

    def _createSettingsMenuActions(self):
        """
        """

    def _createCentralWidget(self):
        """
        """
        self.setCentralWidget(_qt.QWidget())
        self.centralWidget().setLayout(_qt.QVBoxLayout())

        self._createLogs()

    def _createLogs(self):
        """
        """

    def createLogsWidget(self):
        """
        """
        self.QPlainTextEdit().setReadOnly(True)


def show():
    """Open up the UI."""
    app = _qt.QApplication(sys.argv)

    ui = EzLoggingUI()
    ui.show()

    app.exec_()
    sys.exit()

if __name__ == '__main__':
    show()
