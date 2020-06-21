#include "Galvo.h"
#include <cantino.h>

Galvo::Galvo(GalvoMotor x, GalvoMotor y, Laser laser){
	this.x = x; 
	this.y = y;
	this.laser = laser;
}

void Galvo::write(int newPosX, int newPosY){
	if(!checkMinRot(newPosX) && !y.checkMinRot(newPosY)){
		if(!x.checkMaxRot(newPosX) && !y.checkMaxRot(newPosY)){
			x.write(newPosX);
			y.write(newPosY);
		}else{
			x.write(x.MAX_ROT);
			y.write(y.MAX_ROT);
		}
	}else if(!x.checkMaxRot(newPosX) && !y.checkMaxRot(newPosY)){
		if(!x.checkMinRot(newPosX) && !y.checkMinRot(newPosY)){
			x.write(newPosX);
			y.write(newPosY);
		}else{
			x.write(x.MIN_ROT);
			y.write(y.MIN_ROT);
		}		
	}	
}

int getCurrentPosX(){
	return x.current_position;
}

int getCurrentPosY(){
	return y.current_position;
}
