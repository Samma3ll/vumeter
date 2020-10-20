#include "MCP4728.h"
#include <Wire.h>
#include <FastLED.h>

#define NUM_LEDS 4
#define DATA_PIN 3
CRGB leds [NUM_LEDS];

MCP4728 dac;
int ind1;
int ind2;
int ind3;
int ind4;
String readString, dial1, dial2, dial3, dial4;

void setup() {
  Serial.begin(115200);
  Serial.println("<Arduino is ready -->");
    
  Wire.begin();
  dac.attatch(Wire, 4);
  dac.readRegisters();

  dac.selectVref(MCP4728::VREF::VDD, MCP4728::VREF::VDD, MCP4728::VREF::VDD, MCP4728::VREF::VDD);
  dac.selectPowerDown(MCP4728::PWR_DOWN::GND_100KOHM, MCP4728::PWR_DOWN::GND_100KOHM, MCP4728::PWR_DOWN::GND_100KOHM, MCP4728::PWR_DOWN::GND_100KOHM);
  dac.selectGain(MCP4728::GAIN::X1, MCP4728::GAIN::X1, MCP4728::GAIN::X1, MCP4728::GAIN::X1);
  dac.analogWrite(MCP4728::DAC_CH::A, 400);
  dac.analogWrite(MCP4728::DAC_CH::B, 400);
  dac.analogWrite(MCP4728::DAC_CH::C, 400);
  dac.analogWrite(MCP4728::DAC_CH::D, 400);

  dac.enable(true);

  dac.readRegisters();
  FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);
  //printStatus();
  delay(1);
}
    

void loop() {
    //static int count = 0;
    //if (++count > 4000)  count = 0;
    //dac.analogWrite(MCP4728::DAC_CH::D, 3500);
    //dac.analogWrite(count, count, count, count);
  leds[0].setRGB(255, 255, 255);
  leds[1] = CRGB::White;
  leds[2] = CRGB::White;
  leds[3] = CRGB::White;
  FastLED.show();
  while (Serial.available()) {
    delay(5);
    if (Serial.available() >0) {
      char c = Serial.read();
      readString += c;
    }
  }

  if (readString.length() >0) {
    Serial.println(readString);
    ind1 = readString.indexOf(',');
    dial1 = readString.substring(0, ind1);
    ind2 = readString.indexOf(',', ind1+1 );
    dial2 = readString.substring(ind1+1, ind2+1);
    ind3 = readString.indexOf(',', ind2+1 );
    dial3 = readString.substring(ind2+1, ind3+1);
    ind4 = readString.indexOf(',', ind3+1 );
    dial4 = readString.substring(ind3+1);
    

    //Serial.println(dial1);
    //Serial.println(dial2);

    int n1;
    char carray1[6];
    dial1.toCharArray(carray1, sizeof(carray1));
    n1 = atoi(carray1);
    
    int n2;
    char carray2[6];
    dial2.toCharArray(carray2, sizeof(carray2));
    n2 = atoi(carray2);

    int n3;
    char carray3[6];
    dial3.toCharArray(carray3, sizeof(carray3));
    n3 = atoi(carray3);
    
    int n4;
    char carray4[6];
    dial4.toCharArray(carray4, sizeof(carray4));
    n4 = atoi(carray4);

    dac.analogWrite(MCP4728::DAC_CH::A, n1);
    dac.analogWrite(MCP4728::DAC_CH::B, n2);
    dac.analogWrite(MCP4728::DAC_CH::C, n3);
    dac.analogWrite(MCP4728::DAC_CH::D, n4);
  readString="";
  }
}
