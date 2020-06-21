#ifndef ServoMotor_h
#ifdef __cplusplus
#define ServoMotor_h

#include "Arduino.h"
#include "Servo.h"

class ServoMotor : public Servo {
  
  private:
  	int MAX_ROT;
	int MIN_ROT;
	
  public:
	ServoMotor(int _MAX_ROT, int _MIN_ROT, int _pin);
	int current_position;
	int pin;
	void write(int newPos);
	void attach(int pinMotor);
  bool checkMaxRot(int posToCheck);
  bool checkMinRot(int posToCheck);
  int getCurrentPos();
};
#endif
#endif
