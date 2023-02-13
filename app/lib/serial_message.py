from enum import IntEnum


class MessageType(IntEnum):
	FEEDBACK = 1,
	CAPTURE = 2,


class Message:
	def __init__(self, message_type: MessageType, data: str):
		self.message_type = message_type
		self.data = data
