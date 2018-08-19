import sys
from PySide2.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QDialog, QDialogButtonBox
from PySide2.QtCore import QSize, Signal

# an empty/blank QWidget wrapper?
# TODO : validation
# TODO : clis should do something sensible on exception (e.g. loop)
# TODO some reset method to reset the value to default (so it doesn't maintain previous value)


class DuplicateKeyException(Exception):
    pass


class RunnerConfigDialog(QDialog):
    def __init__(self, dialog_title, widget):
        super().__init__(None)
        self.setWindowTitle(dialog_title)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(widget)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok
                                   | QDialogButtonBox.Cancel)
        self.layout().addWidget(buttons)


class Interface:
    def __init__(self, children):
        widget = QWidget()

        # check for duplicate keys

        # store children as a dictionary
        self.children = {}

        widget.setLayout(QVBoxLayout())

        for child in children:
            if child.key in self.children:
                raise DuplicateKeyException(
                    "duplicate entries for key '{}'".format(child.key))
            else:
                self.children[child.key] = child
                child.widget.setParent(widget)
                widget.layout().addWidget(child.widget)

        self.dialog = RunnerConfigDialog("Configure Run", widget)

    def show(self):
        # reset values
        [child.init() for child in self.children.values()]

        accepted = self.dialog.open()

        return accepted

    def data(self):
        data = {}
        for key, child in self.children.items():

            value = child.value()

            data[key] = value

        return data

    def invalid(self):
        return [child for child in self.children.values() if not child.valid()]


class TextInput:
    def __init__(self, key, label, default=None, remember=True):

        self.__default_value = default
        self.__remember = remember

        # public attributes
        self.key = key
        self.label = QLabel(label)
        self.widget = QLineEdit()

        # initialise with default value
        self.set_value(self.__default_value)

    def value(self):
        return self.widget.text()

    def set_value(self, value):
        return self.widget.setText(value)

    def init(self):
        if not self.__remember:
            self.set_value(self.__default_value)

    def cli(self):
        return input(self.label.text())

    def valid(self):
        return True
