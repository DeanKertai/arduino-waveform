import time
from typing import List
from serial.tools import list_ports
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PyQt6.QtWidgets import QLabel, QComboBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, pyqtSignal, QThread


class PortSelector(QWidget):
	update_port = pyqtSignal(str)

	def __init__(self, header_font: QFont, description_font: QFont):
		super().__init__()

		layout = QVBoxLayout()
		self.setLayout(layout)

		# Header
		header = QLabel("Port:")
		header.setFont(header_font)
		layout.addWidget(header)

		# Description
		description = QLabel(
			"Select the serial port that your device is connected to")
		description.setWordWrap(True)
		description.setSizePolicy(
			QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
		description.setAlignment(
			Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
		description.setFont(description_font)
		layout.addWidget(description)

		# Combo Box
		self.combo = QComboBox()
		self.combo.currentIndexChanged.connect(self.on_combo_change)
		layout.addWidget(self.combo)

		# Watch for changes to port list
		self.watcher = AvailableSerialPortWatcher()
		self.watcher.on_change.connect(self.on_port_list_change)
		self.watcher.start()

	def on_port_list_change(self):
		"""
		Called when the list of available serial ports changes.
		This will update the items in the combo box and try to
		automatically select the Arduino if it is connected. 
		"""
		self.combo.clear()
		selected_index = 0
		for index, port in enumerate(list_ports.comports()):
			self.combo.addItem(port.description, userData=port.device)
			if 'arduino' in port.description.lower():
				selected_index = index
		self.combo.setCurrentIndex(selected_index)

	def on_combo_change(self):
		"""
		Called when the user selects a different port from the combo box.
		Emit a signal with the new port device, so we can update the serial thread.
		"""
		self.update_port.emit(self.combo.currentData())


class AvailableSerialPortWatcher(QThread):
	"""
	This thread continually checks the available serial ports and emits a signal
	when the list changes. This is used to update the port selector combo box.
	"""
	on_change = pyqtSignal()

	def __init__(self):
		QThread.__init__(self)

	def run(self):
		current_device_list = []
		while True:
			time.sleep(1)
			new_devices = sorted([port.device for port in list_ports.comports()])
			if new_devices != current_device_list:
				current_device_list = new_devices
				self.on_change.emit()
