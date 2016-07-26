import sys
import PySide.QtGui as _qt
import Ezlogging


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
        self._createCentralWidget()

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

        self._createLogOutput()

    def _createLogOutput(self):
        """
        """
        self._logOutputLayout = _qt.QHBoxLayout()
        logOutput = _qt.QTextEdit()
        logOutput.setReadOnly(True)
        logOutput.setLineWrapMode(_qt.QTextEdit.NoWrap)

        font = logOutput.font()
        font.setFamily("Verdana")
        font.setPointSize(10)

        self._logOutputLayout.addWidget(logOutput)

        self.centralWidget().layout().addLayout(self._logOutputLayout)


def show():
    """Open up the UI."""
    app = _qt.QApplication(sys.argv)

    ui = EzLoggingUI()
    ui.show()

    Ezlogging.main()

    app.exec_()
    sys.exit()

if __name__ == '__main__':
    show()
