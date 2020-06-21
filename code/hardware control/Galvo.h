#ifndef Galvo_h
#ifdef __cplusplus
#define Galvo_h

#include "GalvoMotor.h"
#include "Arduino.h"

class Galvo {
  
  private:
	GalvoMotor x;
	GalvoMotor y;
	Laser laser;
  
  public:
	GalvoMotor(GalvoMotor x, GalvoMotor y, Laser laser);
	void write(int newPosX, int newPosY);
	int getCurrentPosX();
	int getCurrentPosY();
	int writeLaser();
};
#endif
#endif