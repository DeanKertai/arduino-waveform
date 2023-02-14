from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFont


class HeadingLabel(QLabel):

	def __init__(self, text: str):
		super().__init__()
		font = QFont()
		font.setPointSize(12)
		font.setBold(True)
		self.setFont(font)
		self.setText(text)
