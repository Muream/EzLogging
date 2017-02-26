from ui.EzLoggingUI import EzLoggingUI
from PySide import QtGui
import sys


def show():
    app = QtGui.QApplication(sys.argv)

    ui = EzLoggingUI()
    ui.show()

    app.exec_()
    sys.exit()


if __name__ == '__main__':
    show()
