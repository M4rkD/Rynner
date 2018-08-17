import unittest
from unittest.mock import MagicMock as MM
from unittest.mock import patch
from PySide2.QtTest import QTest
from inputs import *
import inputs

app = QApplication(sys.argv)


class TestTextInput(unittest.TestCase):
    def setUp(self):
        pass

    def instance(self, **kwargs):
        self.input = TextInput('key', 'Label', **kwargs)

    def type_text(self, text):
        QTest.keyClicks(self.input.input, text)

    def test_instance(self):
        self.instance()

    def test_can_type_text(self):
        self.instance()
        self.type_text("some input")

    def test_value_method_return_text(self):
        self.instance()
        self.type_text("some input")
        self.assertEqual(self.input.value(), "some input")

    def test_show_qwidget(self):
        input = TextInput('key', 'label')
        input.init()

    def test_has_adds_widgets_as_child(self):

        input = TextInput('key', 'label')

        assert QLineEdit not in input.widget.children()
        assert QLabel not in input.widget.children()

    def test_sets_default_text_in_text_edit(self):
        input = TextInput('key', 'label', default='default string')
        self.assertEqual(input.value(), 'default string')

    def test_result_contains_children(self):
        input = TextInput('key', 'label')

        types = [type(child) for child in input.widget.children()]
        self.assertIn(QLineEdit, types)
        self.assertIn(QLabel, types)

    def test_label_contains_text(self):
        input = TextInput('key', 'My label')
        qlabel_text = next(child.text() for child in input.widget.children()
                           if type(child) == QLabel)

        self.assertEqual(qlabel_text, "My label")

    def test_input_added_to_layout(self):
        input = TextInput('key', 'My label')
        self.assertEqual(input.widget.layout().itemAt(1).widget(), input.input)

    def test_label_added_to_layout(self):
        input = TextInput('key', 'My label')

        self.assertEqual(
            type(input.widget.layout().itemAt(0).widget()), QLabel)

    def test_reset_leaves_value_by_default(self):
        input = TextInput('key', 'My label')
        input.init()

        QTest.keyClicks(input.input, "My Input Text")

        self.assertEqual(input.value(), "My Input Text")

        input.init()

        self.assertEqual(input.value(), "My Input Text")

    def test_uses_default_as_initial(self):
        input = TextInput('key', 'My label', default="default value")

        input.init()

        self.assertEqual(input.value(), "default value")

    def test_no_reset_as_default(self):
        input = TextInput('key', 'My label', default="default value")

        QTest.keyClicks(input.input, " and some more text")

        value = input.value()
        self.assertNotEqual(input.value(), "default value")

        input.init()

        # input value remains the same on calls to init
        self.assertEqual(input.value(), value)

    def test_resets_if_reset_true(self):
        input = TextInput(
            'key', 'My label', default="default value", remember=False)

        QTest.keyClicks(input.input, " and some more text")

        self.assertNotEqual(input.value(), "default value")

        input.init()

        self.assertEqual(input.value(), "default value")

    def test_stores_key(self):
        mock_key = MM()
        input = TextInput(mock_key, 'label')

        self.assertEqual(input.key(), mock_key)

    def test_cli_asks_for_input(self):
        input = TextInput('key', 'Test Label')

        input_data = "Test Input Data"

        with patch.object(
                inputs, "input", create=True, return_value=input_data):
            value = input.cli()
            self.assertEqual(value, input_data)

    @patch('inputs.input')
    def test_cli_correct_label(self, mock_input):
        input = TextInput('key', 'Test Label')

        value = input.cli()
        mock_input.assert_called_once_with('Test Label')
