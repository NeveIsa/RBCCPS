#include <SendOnlySoftwareSerial.h>

/*
  AnalogReadSerial

  Reads an analog input on pin 0, prints the result to the Serial Monitor.
  Graphical representation is available using Serial Plotter (Tools > Serial Plotter menu).
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.

  This example code is in the public domain.

  http://www.arduino.cc/en/Tutorial/AnalogReadSerial
*/

int LED = 1;

SendOnlySoftwareSerial mySerial (0);  // Tx pin


float getDistance()
{
  // read the input on analog pin 0:
  float voltage = (analogRead(1) * 5.0)/1024;  //read from p2
  
  float invDistance = 0.26 + (voltage - 3)/8.125; //refer 0A41SK datasheet graph for line equation.

  float distance = 1/invDistance;

  return distance;
}

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  mySerial.begin(9600);

  pinMode(LED,OUTPUT);

  //analogReference(DEFAULT);
  //analogReference(INTERNAL2V56);
}

// the loop routine runs over and over again forever:
void loop() {
  
  float distance;
  
  distance = getDistance();
  delay(10);
  distance += getDistance();
  delay(10);
  distance += getDistance();

  distance = distance/3; //average of 3 readings
  
  mySerial.println(distance);
  
  if(distance >0 && distance <25){
    digitalWrite(LED,HIGH);
    delay(100);        // delay in between reads for stability - debounce
  }
  else digitalWrite(LED,LOW);

  delay(20); // delay in between reads for stability

  
  
}
