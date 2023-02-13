import time
import serial
import struct
from PyQt6.QtCore import QThread, pyqtSignal
from lib.serial_message import Message, MessageType
from lib.capture import Capture

BAUD_RATE = 115200


class SerialThread(QThread):
	on_message = pyqtSignal(Message)

	def __init__(self):
		QThread.__init__(self)
		self._serial = serial.Serial()
		self._serial.timeout = 0.25
		self._serial.baudrate = BAUD_RATE
		self._port = ''
		self._capture: Capture = None

	def set_port(self, port: str):
		print('Setting serial port', port)
		self._port = port

	def run(self):
		print('Starting serial thread')
		while True:
			try:
				if self._port != self._serial.port or not self._serial.is_open:
					print(f'Opening serial port {self._port}')
					self._serial.close()
					self._serial.port = self._port
					try:
						self._serial.open()
					except serial.SerialException:
						print('Failed to open serial port')
						time.sleep(1)
						continue

				if not self._serial.is_open:
					time.sleep(1)
					continue

				raw_message_type = self._serial.read(1)
				if raw_message_type == b'':
					continue

				raw_message_size = self._serial.read(2)

				message_type = struct.unpack('B', raw_message_type)[0]
				message_size = struct.unpack('>H', raw_message_size)[0]
				message_data = self._serial.read(message_size) if message_size > 0 else b''

				if message_type == 1:
					raw_value_feedback = struct.unpack('>I', message_data)[0]
					msg = Message(MessageType.FEEDBACK, str(raw_value_feedback))
					self.on_message.emit(msg)

				if message_type == 10:
					print('Capture started')
					self._capture = Capture()

				if message_type == 11:
					print('Capture completed')

				if message_type == 12:
					capture_duration_ms = struct.unpack('>I', message_data)[0]
					if self._capture is None:
						raise Exception('Received capture duration message before capture start')
					self._capture.set_duration(capture_duration_ms)
					print(f'Capture duration: {self._capture.get_duration()}')

				if message_type == 13:
					if self._capture is None:
						raise Exception('Received capture data message before capture start')
					capture_duration_ms = self._capture.get_duration()
					if capture_duration_ms == 0:
						raise Exception('Capture duration cannot be 0')
					ms_per_point = float(capture_duration_ms / message_size)
					for i in range(0, message_size):
						point_ms = i * ms_per_point
						self._capture.add_point(point_ms, message_data[i])
					msg = Message(MessageType.CAPTURE, self._capture.serialize())
					self.on_message.emit(msg)

			except Exception as e:
				print('Error', repr(e))
				self._serial.close()
				time.sleep(1)
