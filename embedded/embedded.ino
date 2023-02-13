#include <Arduino.h>
#include "lib/byte_buffer.h"
#include "lib/mode.h"
#include "lib/communication.h"

#define CAPTURE_BUFFER_SIZE 1800

// Defines for setting and clearing register bits
// Required for adjusting the ADC prescaler
#ifndef cbi
#define cbi(sfr, bit) (_SFR_BYTE(sfr) &= ~_BV(bit))
#endif
#ifndef sbi
#define sbi(sfr, bit) (_SFR_BYTE(sfr) |= _BV(bit))
#endif


mode::Mode current_mode = mode::WaitForTrigger;
unsigned int raw_input_value = 0;
unsigned char compressed_value = 0;

unsigned int trigger_threshold = 100;
unsigned long trigger_start_time = 0;

unsigned int capture_max_value = 0;  // highest value recorded during each sample
unsigned int capture_interval = 60;  // microseconds
unsigned long capture_sample_time = 0;  // When the last capture sample was taken
unsigned int capture_sample_index = 0;
unsigned char capture_buffer[CAPTURE_BUFFER_SIZE];
unsigned int capture_duration = 0;

/**
 * Realtime feedback data.
 * We send the highest recorded raw value since the last transmission.
 * This is used to help set the threshold value
*/
unsigned int raw_value_feedback_last_time = 0;
unsigned int raw_value_feedback_interval = 20;  // ms
unsigned int raw_value_feedback_highest_value = 0;

void setup() {
	// Change the ADC prescaler to 16
	// This allows for faster sampling, but reduces the resolution
	sbi(ADCSRA,ADPS2) ;
	cbi(ADCSRA,ADPS1) ;
	cbi(ADCSRA,ADPS0) ;

	Serial.begin(115200);
}

void loop() {
	/*
	 * Wait For Trigger Mode 
	 */
	if (current_mode == mode::WaitForTrigger) {
		raw_input_value = analogRead(A0);

		if (raw_input_value > trigger_threshold) {
			current_mode = mode::Capturing;
			trigger_start_time = millis();
			capture_sample_index = 0;
			comm::send_flag(comm::CaptureStart);
			return;
		}
		
		if (raw_input_value > raw_value_feedback_highest_value) {
			raw_value_feedback_highest_value = raw_input_value;
		}

		if (millis() - raw_value_feedback_last_time > raw_value_feedback_interval) {
			byte_buffer::from_u_int(raw_value_feedback_highest_value);
			comm::send_message(
				comm::RawValueFeedback,
				byte_buffer::buffer,
				4
			);
			raw_value_feedback_last_time = millis();
			raw_value_feedback_highest_value = 0;
		}
	}

	/**
	 * Capturing Mode
	 */
	if (current_mode == mode::Capturing) {
		raw_input_value = analogRead(A0);
		if (raw_input_value > capture_max_value) {
			capture_max_value = raw_input_value;
		}
		if (micros() - capture_sample_time < capture_interval) {
			return;
		}
		capture_sample_time = micros();
		compressed_value = (unsigned char)(capture_max_value >> 2);
		capture_max_value = 0;
		if (capture_sample_index < CAPTURE_BUFFER_SIZE) {
			capture_buffer[capture_sample_index] = compressed_value;
			capture_sample_index++;
		} else {
			capture_duration = millis() - trigger_start_time;
			current_mode = mode::SendingCapture;
			return;
		}
	}

	/**
	 * Sending Capture Mode
	 */
	if (current_mode == mode::SendingCapture) {
		comm::send_flag(comm::CaptureComplete);
		byte_buffer::from_u_int(capture_duration);
		comm::send_message(
			comm::CaptureDuration,
			byte_buffer::buffer,
			4
		);
		unsigned int i;
		comm::send_message(
			comm::CaptureData,
			capture_buffer,
			CAPTURE_BUFFER_SIZE
		);
		delay(100);
		current_mode = mode::WaitForTrigger;
		return;
	}
}
