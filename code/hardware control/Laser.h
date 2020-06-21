#ifndef Laser_h
#ifdef __cplusplus
#define Laser_h

#include "Arduino.h"

class Laser {
  
  private:
	int state;
	int pin;
  
  public:
	Laser(int pin, int state);
	void changeState(int state);
	int getCurrentLaserState();

};
#endif
#endif