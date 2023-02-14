from PyQt6.QtWidgets import QLabel, QSizePolicy
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class TextBox(QLabel):

	def __init__(self, text: str):
		super().__init__()
		font = QFont()
		font.setPointSize(9)
		self.setFont(font)
		self.setText(text)

		self.setWordWrap(True)
		self.setSizePolicy(
			QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
		self.setAlignment(
			Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
