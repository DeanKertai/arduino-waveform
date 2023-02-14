from typing import List
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtWidgets import QLabel
from lib.serial_message import Message
from pyqtgraph import PlotWidget, mkPen
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from lib.widgets.heading_label import HeadingLabel
from lib.widgets.text_box import TextBox

MAX_LENGTH = 100


class RawFeedbackDisplay(QWidget):
	def __init__(self):
		super().__init__()

		self.x_values = list(range(MAX_LENGTH))
		self.y_values = [0] * MAX_LENGTH

		layout = QVBoxLayout()
		self.setLayout(layout)

		# Heading and description
		layout.addWidget(HeadingLabel("Realtime Feedback"))
		layout.addWidget(TextBox(
			"Use the live sensor value to determine a trigger threshold"))

		self.graph = PlotWidget()
		self.graph.enableMouse(False)
		# self.graph.setYRange(-50, 300)
		pen = mkPen(color=(0, 255, 0))
		self.data_line =  self.graph.plot(
			self.x_values,
			self.y_values,
			pen=pen
		)

		# Set the max height
		self.graph.setMaximumHeight(100)

		layout.addWidget(self.graph)

		# Hide axis labels
		self.graph.getAxis("bottom").setTicks([])

		# Hide axis lines
		self.graph.getAxis("bottom").setPen(mkPen(color=(0, 0, 0, 0)))
		self.graph.getAxis("left").setPen(mkPen(color=(0, 0, 0, 0)))

		# Label
		self.label = QLabel("")
		layout.addWidget(self.label)

		# Align everything to the top
		layout.addStretch(1)

	def handle_feedback(self, message: Message):
		str_value = message.data
		int_value = int(str_value)
		self.label.setText(str_value)

		self.x_values = self.x_values[1:]  # Remove the first element
		self.x_values.append(self.x_values[-1] + 1)  # Add a n1 higher than last

		self.y_values = self.y_values[1:]  # Remove the first element
		self.y_values.append(int_value)

		self.data_line.setData(self.x_values, self.y_values)
