from PyQt6.QtWidgets import QMainWindow, QWidget
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout
from lib.widgets.port_selector import PortSelector
from lib.widgets.raw_feedback_display import RawFeedbackDisplay
from lib.widgets.graph import GraphWidget
from lib.serial_thread import SerialThread
from lib.serial_message import Message, MessageType
from lib.capture import Capture


class MainWindow(QMainWindow):

	def __init__(self):
		super(MainWindow, self).__init__()

		# Start serial thread
		self.serial_thread = SerialThread()
		self.serial_thread.on_message.connect(self.handle_serial_incoming)
		self.serial_thread.start()

		self.setWindowTitle("Waveform Analyzer")

		outer_layout = QHBoxLayout()
		options_layout = QVBoxLayout()
		options_widget = QWidget()

		options_layout.setContentsMargins(0, 0, 0, 0)
		options_widget.setFixedWidth(200)
		options_widget.setLayout(options_layout)

		# Port Selector
		self.port_selector = PortSelector()
		self.port_selector.update_port.connect(self.handle_port_change)
		options_layout.addWidget(self.port_selector)

		# Feedback Display
		self.feedback_display = RawFeedbackDisplay()
		options_layout.addWidget(self.feedback_display)

		# Options bar
		options_layout.addStretch(1)  # Fill empty space (align items to top)
		outer_layout.addWidget(options_widget)

		# Content (graph area)
		self.graph_widget = GraphWidget()
		outer_layout.addWidget(self.graph_widget)

		# Set layout
		widget = QWidget()
		widget.setLayout(outer_layout)
		self.setCentralWidget(widget)

	def handle_port_change(self, port: str):
		self.serial_thread.set_port(port)

	def handle_serial_incoming(self, message: Message):
		if message.message_type == MessageType.FEEDBACK:
			self.feedback_display.handle_feedback(message)
		if message.message_type == MessageType.CAPTURE:
			capture_obj = Capture()
			capture_obj.deserialize(message.data)
			self.graph_widget.handle_capture(capture_obj)
