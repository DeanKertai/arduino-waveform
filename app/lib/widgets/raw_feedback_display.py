from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtWidgets import QLabel
from lib.serial_message import Message


class RawFeedbackDisplay(QWidget):
	def __init__(self):
		super().__init__()

		layout = QVBoxLayout()
		self.setLayout(layout)

		# Label
		self.label = QLabel("")
		layout.addWidget(self.label)

	def handle_feedback(self, message: Message):
		self.label.setText(message.data)
