#include "Laser.h"
#include <cantino.h>
#include "Arduino.h"

Laser::Laser(int pin, int state){
	this.pin = pin;
	this.state = state;
	pinMode(pin, OUTPUT);
}

void Laser::changeState(int state){
	digitalWrite(pin, state);
}

int Laser::getCurrentLaserState(){
	return this.state;
}
