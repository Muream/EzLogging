from PySide import QtGui, QtCore
import sys


class HotkeyPushButton(QtGui.QPushButton):

    def __init__(self, hotkey):
        super(HotkeyPushButton, self).__init__()
        self.changeHotkey = False
        self.hotkey = hotkey
        self.setText(str(self.hotkey))

        self.released.connect(self.get_hotkey)

    def get_hotkey(self):
        self.setText("press a key")
        self.changeHotkey = True

    def keyPressEvent(self, event):
        if event.type() == QtCore.QEvent.Type.KeyPress:
            if self.changeHotkey is True:
                self.hotkey = event.text()

                # check if the key is an Fkey
                if event.key() == QtCore.Qt.Key_F1:
                    self.hotkey = "F1"
                if event.key() == QtCore.Qt.Key_F2:
                    self.hotkey = "F2"
                if event.key() == QtCore.Qt.Key_F3:
                    self.hotkey = "F3"
                if event.key() == QtCore.Qt.Key_F4:
                    self.hotkey = "F4"
                if event.key() == QtCore.Qt.Key_F5:
                    self.hotkey = "F5"
                if event.key() == QtCore.Qt.Key_F6:
                    self.hotkey = "F6"
                if event.key() == QtCore.Qt.Key_F7:
                    self.hotkey = "F7"
                if event.key() == QtCore.Qt.Key_F8:
                    self.hotkey = "F8"
                if event.key() == QtCore.Qt.Key_F9:
                    self.hotkey = "F9"
                if event.key() == QtCore.Qt.Key_F10:
                    self.hotkey = "F10"
                if event.key() == QtCore.Qt.Key_F11:
                    self.hotkey = "F11"
                if event.key() == QtCore.Qt.Key_F12:
                    self.hotkey = "F12"

                self.setText(self.hotkey)
                self.changeHotkey = False
