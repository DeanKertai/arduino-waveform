import json
from typing import List


class Capture:
	def __init__(self):
		self._duration = 0
		self._x_values = []
		self._y_values = []

	def set_duration(self, duration: int):
		self._duration = duration

	def get_duration(self) -> int:
		return self._duration

	def add_point(self, timestamp: int, value: int):
		self._x_values.append(timestamp)
		self._y_values.append(value)

	def get_x_values(self) -> List[int]:
		return self._x_values

	def get_y_values(self) -> List[int]:
		return self._y_values

	def serialize(self) -> str:
		return json.dumps({
			'x': self._x_values,
			'y': self._y_values
		})

	def deserialize(self, data: str):
		data = json.loads(data)
		self._x_values = data['x']
		self._y_values = data['y']
