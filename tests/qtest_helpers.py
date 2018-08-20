import unittest
from PySide2.QtCore import QTimer
from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QPushButton

##################################################################
# QTestCase test base class                                      #
##################################################################


class QTestCase(unittest.TestCase):
    def __visibility(self, widgets):
        ''' Test the visibility of a widget or widgets. Returns a list of boolean values denoting visibility.'''
        try:
            return [widget.isVisible() for widget in widgets]
        except TypeError:
            return [widgets.isVisible()]

    def assertQVisible(self, widgets):
        '''assert that a list of Qt objects are all visible. Arguments are a list of QWidgets to test'''
        self.assertNotIn(False, self.__visibility(widgets))

    def assertNotQVisible(self, widgets):
        '''assert that a list of Qt objects are all not visible. Arguments are a list of QWidgets to test'''
        self.assertNotIn(True, self.__visibility(widgets))


##################################################################
# Helper functions                                               #
##################################################################


def get_button(button_box, button_text):

    buttons = [
        button for button in button_box.children() if
        type(button) is QPushButton and button_text in button.text().lower()
    ]
    button = buttons[0]

    return button


def button_callback(method, button):
    def callback():
        button.click()

    QTimer.singleShot(10, callback)

    method()


##################################################################
# QApplication                                                   #
##################################################################

# ensure app is instantiated only once (when package loaded initially)
app = QApplication()
