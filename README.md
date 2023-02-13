# Arduino Serial Waveform Plotter

This is a simple Python GUI for plotting waveforms using `analogRead()`.
Basically, it's a better version of the serial plotter that comes with the
Arduino IDE. I needed this for my drum module project, to be able to analyze
feedback from piezoelectric sensors on mesh drum heads.

The Arduino firmware located at `embedded/embedded.ino` modifies the Arduino's
ADC prescaler to allow for faster sampling (~18 microseconds per `analogRead()`). 
The code then simply reads the value on pin `A0` continuously, saving the value
to an internal array. When a certain threshold value is reached, the array is
sent to the Python GUI (`/app/app.py`) over serial for display.  

# How to use
1. Flash `embedded/embedded.ino` to your Arduino
1. Hook the sensor up to pin `A0`
1. Install Python dependencies
	```
	python3 -m pip install -r app/requirements.txt
	```
1. Run the client
	```
	python3 app/app.py
	```
