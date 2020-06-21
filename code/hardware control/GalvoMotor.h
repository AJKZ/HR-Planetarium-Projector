#ifndef GalvoMotor_h
#ifdef __cplusplus
#define GalvoMotor_h

#include "Arduino.h"
#include "ServoMotor.h"

class GalvoMotor : public ServoMotor {
  
  public:
	GalvoMotor(int _MAX_ROT, int _MIN_ROT, int _pin);
	int current_position;
	void write(int newPos);
	void attach(int pinMotor);
	int getCurrentPos();
};
#endif
#endif
