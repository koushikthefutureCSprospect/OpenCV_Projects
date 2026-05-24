#include <Servo.h>

Servo myServo;
int val;
int finger_length;
void setup() {
  Serial.begin(230400);
  myServo.attach(13); // Servo signal wire on Pin 13
  myServo.write(0);  // Initialize at 0 degrees
}

void loop() {
  if (Serial.available() > 0) {
    // Read the incoming string until a newline or timeout
    String data = Serial.readString();
    
    // Convert the string to an integer
    finger_length = data.toInt();
    val = map(finger_length,50,300,0,180);

    // Constrain the angle to the servo's physical limits
    val = constrain(val, 0, 180);

    myServo.write(val);

  }
}
