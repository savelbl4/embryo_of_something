#define LED_PIN 5     // пин
#define LED_NUM 256    // количество светодиодов

#include <FastLED.h>

CRGB leds[LED_NUM];

void setup() {
  FastLED.addLeds<WS2812, LED_PIN, GRB>(leds, LED_NUM);
  FastLED.setBrightness(50);
}
byte counter;
void loop() {
  FastLED.clear();
  leds[counter] = CRGB::Red;
  if (++counter >= LED_NUM) counter = 0;
  FastLED.show();
  delay(50);
}
