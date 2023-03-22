// file IMUClassify.ino
/*configsip: 0, SPIWP:0xee
clk_drv:0x00,q_drv:0x00,d_drv:0x00,cs0_drv:0x00,hd_drv:0x00,wp_drv:0x00
mode:DIO, clock div:1
load:0x3fff0030,len:1184
load:0x40078000,len:13132
load:0x40080400,len:3036
entry 0x400805e4
Adafruit MPU6050 test!
MPU6050 Found!
Accelerometer range set to: +-8G
Gyro range set to: +- 500 deg/s
Filter bandwidth set to: 21 Hz*/
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <string.h>
#include "Pipeline.h"
#include "Classifier.h"

Adafruit_MPU6050 mpu;

void setup() {
  Serial.begin(115200);
  Serial.println("Started");
  while (!Serial) {
      delay(10); // will pause Zero, Leonardo, etc until serial console opens
    }

    // Try to initialize!
    if (!mpu.begin()) {
      Serial.println("Failed to find MPU6050 chip");
      while (1) {
        delay(10);
      }
    }
    pinMode(LED_BUILTIN, OUTPUT);
    mpu.setAccelerometerRange(MPU6050_RANGE_16_G);
    mpu.setGyroRange(MPU6050_RANGE_250_DEG);
    mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
    Serial.println("");
    delay(100);
}

void loop() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  float features[] = {a.acceleration.x, a.acceleration.y, a.acceleration.z};
    
  if (!pipeline.transform(features))
    return;
  char target = forest.predictLabel(pipeline.X)[7];
  // perform classification
  Serial.print("Prediction:");
  Serial.print(target);
  if (target == '1'){
    digitalWrite(LED_BUILTIN, HIGH);  // turn the LED on (HIGH is the voltage level)
    delay(1000);                      // wait for a second
    digitalWrite(LED_BUILTIN, LOW);   // turn the LED off by making the voltage LOW 
  }
  //Serial.print(" (DSP: ");
  //Serial.print(pipeline.latencyInMicros());
  //Serial.print(" micros, Classifier: ");
  //Serial.print(forest.latencyInMicros());
  //Serial.println(" micros)");

  Serial.print(", AccelX:");
  Serial.print(a.acceleration.x);
  Serial.print(",");
  Serial.print("AccelY:");
  Serial.print(a.acceleration.y);
  Serial.print(",");
  Serial.print("AccelZ:");
  Serial.print(a.acceleration.z);
  Serial.println("");
}