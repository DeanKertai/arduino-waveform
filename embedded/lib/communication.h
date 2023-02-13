#include <Arduino.h>

namespace comm {

	unsigned char size_buffer[4];

	enum MessageType {
		RawValueFeedback = 1,
		CaptureStart = 10,
		CaptureComplete = 11,
		CaptureDuration = 12,
		CaptureData = 13,
	};

	/**
	 * Send the message type and size
	*/
	void send_message_header(MessageType type, unsigned int size) {
		Serial.write((unsigned char)type);
		Serial.write((size >> 8) & 0xFF);
		Serial.write(size & 0xFF);
	}

	/**
	 * Send a message with no payload
	 */
	void send_flag(MessageType type) {
		send_message_header(type, 0);
	}

	/**
	 * Send a message with a payload
	 */
	void send_message(MessageType type, unsigned char data[], unsigned int size) {
		send_message_header(type, size);
		unsigned int i;
		for (i = 0; i < size; i++) {
			Serial.write(data[i]);
		}
	}
}
