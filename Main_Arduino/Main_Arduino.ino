#include <Servo.h>

Servo servo_x;  // Servo controls X axis tilt
Servo servo_y;  // Servo controls Y axis tilt

int x = 90;
int y = 90;

int x_offset = 5;
int y_offset = 5;

void setup() {
  Serial.begin(115200);
  servo_x.attach(6);
  servo_y.attach(7);
}

void loop() {
    
    if(Serial.available() > 0) {
      char c = Serial.read();
      if (c == 'S'){  // Servo Position Data
        updateAngles();
      }else if(c == 'C'){ // Calibration routine
        calibrate();
      }
    }
}

// Used to update servo positions
void updateAngles() {
  char x1 = Serial.read();
  char x2 = Serial.read();
  char x3 = Serial.read();
  
  x = 100 * int(x1) + 10 * int(x2) + int(x3) - 111 * '0';

  char y1 = Serial.read();
  char y2 = Serial.read();
  char y3 = Serial.read();
  
  y = 100 * int(y1) + 10 * int(y2) + int(y3) - 111 * '0';

  servo_x.write(180 - (x-5));
  servo_y.write(180 - (y-5));
//  Serial.println("X: " + String(x) + "\tY: " + String(y));
}

// Used to calibrate tilt
void calibrate(){
  Serial.println("Calibrate");
}
