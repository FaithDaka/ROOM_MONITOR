#include <Adafruit_FONA.h>
#include <SoftwareSerial.h>
#include<avr/interrupt.h>
#include<avr/io.h>

#define RX 11
#define TX 12
#define SIM_RST 7

void Sensor_Entrance();
void Sensor_Exit();

SoftwareSerial GSM = SoftwareSerial(RX, TX);
Adafruit_FONA SIM = Adafruit_FONA(SIM_RST);
int led1 = 8;
int led2 = 9;
int led3 = 10;
int PIR_1 = 2;
int PIR_2 = 3;
int waitTime = 0;
int startTime = 0;
int writingTimer = 0;
int Person_In = 0;

void setup() 
{

boolean gprsOn = false;
boolean tcpOn = false;
int network;

pinMode(led1, OUTPUT);
pinMode(led2, OUTPUT);
pinMode(led3, OUTPUT);
pinMode(PIR_1, INPUT);
pinMode(PIR_2, INPUT);
Serial.begin(9600);
GSM.begin(9600);
attachInterrupt(digitalPinToInterrupt(PIR_1), Sensor_Entrance, FALLING);
attachInterrupt(digitalPinToInterrupt(PIR_2), Sensor_Exit, FALLING);

if(!SIM.begin(GSM))
{
  Serial.println("Sim module undetected!");
  while(1);
}

Serial.println("GSM is okay");
delay(1000);
Serial.println("Registering to network...");

network = SIM.getNetworkStatus();

while(network != 1)
{
  network = SIM.getNetworkStatus();
  delay(1500);
}

Serial.println("Simcard is registered!");
Serial.println("Turning gprs service on...");
delay(1500);

while(!gprsOn)
{
  if(SIM.enableGPRS(true))
  {
    Serial.println("GPRS UNDETECTED, PLEASE WAIT...");
    delay(1500);
    gprsOn = false;
  }
  else
  {
    Serial.println("GPRS turned on successfully");
    delay(1500);
    gprsOn = true;
  }
}
}

void loop()
{
digitalWrite(led1, LOW);
digitalWrite(led2, LOW);
digitalWrite(led3, LOW);
Serial.println("SENSOR NOW AVAILABLE FOR MOTION");
goto OFF;

ON:
{
Serial.println("MOTION DETECTED");
digitalWrite(led1, HIGH);
digitalWrite(led2, HIGH);
digitalWrite(led3, HIGH);
if(digitalRead(PIR_1))
{
  digitalWrite(led1, LOW);
  digitalWrite(led2, LOW);
  digitalWrite(led3, LOW);
  delay(10000);
  timing();
  goto OFF;
}
else
{
  goto ON;
}

if(digitalRead(PIR_2))
{
  Serial.println("Person has exited.");
  delay(5000);
  goto OFF;
}
}

OFF:
{
  digitalWrite(led1, LOW);
  digitalWrite(led2, LOW);
  digitalWrite(led3, LOW);
  
  if(digitalRead(PIR_1))
  {
    digitalWrite(led1, HIGH);
    digitalWrite(led2, HIGH);
    digitalWrite(led3, HIGH);
    Serial.println("SENSOR IS RESETTING, PLEASE WAIT!");
    delay(10000);
    goto ON;
  }
  else
  {
    goto OFF;
  }

    if(digitalRead(PIR_2))
  {
    Serial.println("Person has exited!");
    delay(3000);
  }
}
}

void Sensor_Entrance()
{
  Person_In++;
  Serial.println();
  Serial.print("Motion detected ");
  Serial.print(Person_In);
  Serial.print(" times.");
  Serial.println();
}

void Sensor_Exit()
{
  while(Person_In != 0)
  {
    Person_In--;
    Serial.println(Person_In);
    Serial.print(" people left inside.");
    Serial.println();
  }
}

void sendToThingSpeak()
{
  GSM.println(" AT+CIPSTART=\"TCP\",\"184.106.153.149\",\"80\" ");
  /*Serial.println("Set cipStart:");
  String protocol = Serial.readString();
  */
  GSM.print("GET /update?key=7NCC2BFYKT79TN0X&field1=");
  GSM.print(Person_In);
  GSM.print("\r\n");
  updateGSM();
  GSM.print("GET /update?key=7NCC2BFYKT79TN0X&field2=3.3\r\n");
  updateGSM();
}

void updateGSM()
{
  delay(500);
while (Serial.available())
{
GSM.write(Serial.read());
}
while(GSM.available())
{
Serial.write(GSM.read());
}
}

void timing()
{
    waitTime = millis()-startTime;
  if(waitTime > (writingTimer*1000))
  {
    sendToThingSpeak();
    startTime = millis();
  }
}
