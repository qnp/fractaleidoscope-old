#include <Servo.h>

// Using floats as the servo library can handle this and
// it makes for smoother progression through position
// values.

bool PIRstate = LOW;

int randompos1;
int randompos2;

int posmaxservo1 = 2300;
int posmaxservo2 = 2100;

int posminservo1 = 650;
int posminservo2 = 900;

int debatementmin2 = posminservo2+300;
int debatementmax2 = posmaxservo2;
int rangeservo2 = debatementmax2-debatementmin2;
int smallrange2 = rangeservo2/4;
int newposmin2, newposmax2;

int posmidservo1 = (posminservo1+posmaxservo1)/2+25;
int posmidservo2 = (posminservo2+posmaxservo2)/2-20;

int debatement1 = 120;

int minwait = 10000;
int maxwait = 20000;
int wait1 = 0;
int wait2 = 0;
int newwait1, newwait2;
int countmoves2 = 0;

float current_pos1;
float target_pos1;

float current_pos2;
float target_pos2;

// variable to control smoothing.
float easing1 = 0.0007;
float easing2 = 0.001;

float speed1 = 0.1;
float speed2 = 0.1;

bool adjust = false;


// Motors
Servo servo1; //axe vertical
Servo servo2; //axe cam

float diff1; // difference of position
float diff2; // difference of position
int randomspeed1;
int randomspeed2;
int travel1 = 0;
int travel2 = 0;
int completion1 = 0; //avance de la position courante sur le chemin. varie de 0 � travel1
int completion2 = 0;
int startpos1;
int startpos2;


void setup() {

  // servo pin def
  servo1.attach(4);
  servo2.attach(9);

  //go to min/max
  //servo1.writeMicroseconds(posmaxservo1);
  //servo2.writeMicroseconds(posmaxservo2);
  //delay(1000);
  //servo1.writeMicroseconds(posminservo1);
  //servo2.writeMicroseconds(posminservo2);
  //delay(1000);

  //goto mid
  servo1.writeMicroseconds(posmidservo1);
  servo2.writeMicroseconds(posmidservo2);
  current_pos1 = posmidservo1;
  current_pos2 = posmidservo2;
  delay(5000);

  /*servo1.writeMicroseconds(posmidservo1+debatement1-20);
  servo2.writeMicroseconds(debatementmin2+100);
  current_pos1 = posmidservo1+debatement1-20;
  current_pos2 = debatementmin2+100;*/

  //init
  randompos1 = map(random(1000), 0, 1000, posmidservo1-debatement1, posmidservo1+debatement1);
  newposmin2 = current_pos2-smallrange2;
  newposmax2 = current_pos2+smallrange2;
  if (newposmin2 < debatementmin2 || newposmax2 > debatementmax2) {
    newposmin2 = debatementmin2;
    newposmax2 = debatementmax2;
  }
  randompos2 = map(random(1000), 0, 1000, newposmin2, newposmax2);

  target_pos1 = (float)randompos1;
  target_pos2 = (float)randompos2;

  travel1 = abs(target_pos1 - current_pos1);
  travel2 = abs(target_pos2 - current_pos2);

  //target_pos1 = current_pos1+(float)randompos1;
  //target_pos2 = current_pos2+(float)randompos2;
  
  //travel1 = abs(target_pos1 - current_pos1);
  //travel2 = abs(target_pos2 - current_pos2);
 /*
  if (adjust) {

    int waitadj = 8000;

    for (int i=0; i<100; i++) {

      servo1.writeMicroseconds(posmidservo1-debatement1);
      servo2.writeMicroseconds(debatementmin2);
      delay(waitadj);

      servo2.writeMicroseconds(debatementmax2);
      delay(waitadj);

      servo1.writeMicroseconds(posmidservo1+debatement1);
      delay(waitadj);

      servo2.writeMicroseconds(debatementmin2);
      delay(waitadj);

    }
    
  }
 */
}


void loop() {

  if (!adjust) {
  
    PIRstate = digitalRead(2);
  
    //if no movement detected
    //if (PIRstate == LOW)
    //{
  
    //execute target sevro 1
    if (completion1 <= travel1)
    {
      //remaining travel
      diff1 = target_pos1 - current_pos1;
      // Avoid zero condition
      if (diff1 != 0.00)
      {
        if (completion1 >= (travel1 / 2.0))
        {
          if (startpos1 <= target_pos1)
          {
            current_pos1 += speed1 + diff1 * easing1; //smooth the end of movement
          }
          else
          {
            current_pos1 += -speed1 + diff1 * easing1;
          }
        }
        else
        {
          if (startpos1 <= target_pos1)
          {
            current_pos1 +=  speed1 + (travel1 - diff1) * easing1; //smooth the end of movement
          }
          else
          {
            current_pos1 += -speed1 + (-travel1 - diff1) * easing1;
          }
        }
      }
      servo1.writeMicroseconds((int) current_pos1);
      completion1 = abs(current_pos1 - startpos1);
  
    }
    //choose new target
    else
    {
      if (wait1 == 0) newwait1 = map(random(1000), 0, 1000, minwait, maxwait);
      wait1++;
      if (wait1 > newwait1) {
        wait1 = 0;
        startpos1 = current_pos1;
        randompos1 = map(random(1000), 0, 1000, posmidservo1-debatement1, posmidservo1+debatement1);
        if (randompos1 > posmidservo1+debatement1-50 && current_pos2 < debatementmin2+200 ) randompos1 = posmidservo1-debatement1;
        randomspeed1 = random(1, 1000);
        speed1 = (float)randomspeed1 / 5000;
        target_pos1 = (float)randompos1;
  
        travel1 = abs(target_pos1 - current_pos1);
  
        completion1 = 0;
      }
    }
  
    //execute target sevro 2
    if (completion2 <= travel2)
    {
      //remaining travel
      diff2 = target_pos2 - current_pos2;
      // Avoid zero condition
      if (diff2 != 0.00)
      {
        if (completion2 >= (travel2 / 2.0))
        {
          if (startpos2 <= target_pos2)
          {
            current_pos2 += speed2 + diff2 * easing2; //smooth the end of movement
          }
          else
          {
            current_pos2 += -speed2 + diff2 * easing2;
          }
        }
        else
        {
          if (startpos2 <= target_pos2)
          {
            current_pos2 += speed2 + (travel2 - diff2) * easing2; //smooth the end of movement
          }
          else
          {
            current_pos2 += -speed2 + (-travel2 - diff2) * easing2;
          }
        }
      }
      servo2.writeMicroseconds((int)current_pos2);
      completion2 = abs(current_pos2 - startpos2);
  
    }
    //choose new target and parameters
    else
    {
      if (wait2 == 0) newwait2 = map(random(1000), 0, 1000, minwait, maxwait);
      wait2++;
      if (wait2 > newwait2) {
        if (wait2 == newwait2+1) countmoves2++;
        wait2 = 0;
        startpos2 = current_pos2;
        newposmin2 = current_pos2-smallrange2;
        newposmax2 = current_pos2+smallrange2;
        if (newposmin2 < debatementmin2 || newposmax2 > debatementmax2 || countmoves2 == 20) {
          countmoves2 = 0;
          newposmin2 = debatementmin2;
          newposmax2 = debatementmax2;
        }
        randompos2 = map(random(1000), 0, 1000, newposmin2, newposmax2);
        if (randompos2 < debatementmin2+200 && current_pos1 < posmidservo1+debatement1-50 ) randompos2 = debatementmax2-200;
        randomspeed2 = random(1, 1000);
        speed2 = (float)randomspeed2 / 5000;
    
        target_pos2 = (float)randompos2;
    
        travel2 = abs(target_pos2 - current_pos2);
        completion2 = 0;
      }
    }
  
    //}

  }

  delay(1);
}
