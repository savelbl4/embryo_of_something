#include <FastLED.h>
#include <IRremote.h>

#define LED_PIN     5
#define LED_NUM     256
#define LED_WIDTH   16
#define LED_HEIGHT  16

#define IR_RECEIVE_PIN 2  // Подключи ИК-приемник сюда

CRGB leds[LED_NUM];

IRrecv irrecv(IR_RECEIVE_PIN);
decode_results results;

enum Direction {UP, DOWN, LEFT, RIGHT};
Direction dir = RIGHT;

int snake[256];     // Массив индексов (положение змейки)
int snakeLength = 4;
int headIndex = 0;

unsigned long lastMoveTime = 0;
const int moveDelay = 200; // скорость змейки

void setup() {
  FastLED.addLeds<WS2812, LED_PIN, GRB>(leds, LED_NUM);
  FastLED.setBrightness(50);

  irrecv.enableIRIn(); // запускаем прием

  // начальная позиция змейки
  snake[0] = XY(0, 0);
  snake[1] = XY(1, 0);
  snake[2] = XY(2, 0);
  snake[3] = XY(3, 0);
}

void loop() {
  // === Управление с пульта ===
  if (irrecv.decode(&results)) {
    switch (results.value) {
      case 0xFFA857: dir = UP; break;     // кнопка ↑
      case 0xFF629D: dir = DOWN; break;   // ↓
      case 0xFF22DD: dir = LEFT; break;   // ←
      case 0xFFC23D: dir = RIGHT; break;  // →
    }
    irrecv.resume(); // принимаем следующее
  }

  // === Движение змейки ===
  if (millis() - lastMoveTime > moveDelay) {
    moveSnake();
    lastMoveTime = millis();
  }
}

void moveSnake() {
  // вычисляем новое положение головы
  int x = headIndex % LED_WIDTH;
  int y = headIndex / LED_WIDTH;

  switch (dir) {
    case UP:    y--; break;
    case DOWN:  y++; break;
    case LEFT:  x--; break;
    case RIGHT: x++; break;
  }

  // выход за границы — конец игры или "отскок"
  if (x < 0 || x >= LED_WIDTH || y < 0 || y >= LED_HEIGHT) {
    // можно сбросить игру:
    x = constrain(x, 0, LED_WIDTH - 1);
    y = constrain(y, 0, LED_HEIGHT - 1);
    snakeLength = 4;
  }

  headIndex = XY(x, y);

  // сдвигаем тело
  for (int i = snakeLength - 1; i > 0; i--) {
    snake[i] = snake[i - 1];
  }
  snake[0] = headIndex;

  // отрисовка
  FastLED.clear();
  for (int i = 0; i < snakeLength; i++) {
    leds[snake[i]] = (i == 0) ? CRGB::Red : CRGB::Green;
  }
  FastLED.show();
}

// Преобразование XY в индекс (с учётом зигзага)
int XY(int x, int y) {
  if (y % 2 == 0) {
    return y * LED_WIDTH + x;
  } else {
    return y * LED_WIDTH + (LED_WIDTH - 1 - x);
  }
}
