/*
 * A parent class to the GalvoMotor class, a child class derived from the Arduino class ServoMotor. Executes all movement functions and communicates rotational values
 */

#include <Servo.h>
#include "ServoMotor.h"

#include <cantino.h>

using namespace cantino;

ServoMotor::ServoMotor(int _MAX_ROT, int _MIN_ROT, int _pin) : Servo(){
      this->MAX_ROT = _MAX_ROT;
      this->MIN_ROT = _MIN_ROT;
      this->pin = _pin;
      this->current_position = 0;
}

void ServoMotor::write(int newPos){
      Servo::write(newPos);
      current_position = newPos;
      delay(10);
}

void ServoMotor::attach(int pinMotor){
      Servo::attach(pinMotor);
}

int ServoMotor::getCurrentPos(){
      return current_position;
}

bool ServoMotor::checkMaxRot(int posToCheck){
      if(posToCheck > MAX_ROT){
        return true;
      }else{
        return false;
      }
}

bool ServoMotor::checkMinRot(int posToCheck){
      if(posToCheck < MIN_ROT){
        return true;
      }else{
        return false;
      }
}
