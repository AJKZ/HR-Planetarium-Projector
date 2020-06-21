/*
 * A child class derived from ServoMotor that controls the movement of a single SG90 Servo and returns rotational values
 */

#include "ServoMotor.h"
#include "GalvoMotor.h"
#include <cantino.h>

using namespace cantino;

GalvoMotor::GalvoMotor(int _MAX_ROT, int _MIN_ROT, int _pin) : ServoMotor(_MAX_ROT, _MIN_ROT, _pin){
};

void GalvoMotor::write(int newPos){
      ServoMotor::write(newPos);
      cout << pin;
      cout << endl;
}

void GalvoMotor::attach(int pinMotor){
      ServoMotor::attach(pinMotor);
}

bool GalvoMotor::checkMaxRot(int posToCheck){
      ServoMotor::checkMaxRot(posToCheck);
}

bool GalvoMotor::checkMinRot(int posToCheck){
      ServoMotor::checkMinRot(posToCheck);
}

int GalvoMotor::getCurrentPos(){
      ServoMotor::getCurrentPos();
}
