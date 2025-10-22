#include <FastLED.h>
#include <NecDecoder.h>

// === НАСТРОЙКИ ===
#define LED_PIN 5
#define LED_NUM 256
#define WIDTH 16
#define HEIGHT 16

#define IR_PIN 2
#define IR_INT 0  // interrupt 0 = pin 2 на Arduino Uno/Nano

// === КОМАНДЫ С ПУЛЬТА ===
#define IR_UP    0x18
#define IR_DOWN  0x4A
#define IR_LEFT  0x5A
#define IR_RIGHT 0x10

// === ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ ===
CRGB leds[LED_NUM];
NecDecoder ir;

struct Point {
  byte x, y;
};
Point snake[256];
int snakeLength = 3;
int dirX = 1, dirY = 0;
unsigned long lastMoveTime = 0;
int moveDelay = 200;

Point apple = {5, 5};

// === ИНИЦИАЛИЗАЦИЯ ===
void setup() {
  FastLED.addLeds<WS2812, LED_PIN, GRB>(leds, LED_NUM);
  FastLED.setBrightness(50);
  attachInterrupt(IR_INT, irIsr, FALLING);

  // начальная позиция змейки
  snake[0] = {2, 8};
  snake[1] = {1, 8};
  snake[2] = {0, 8};
  randomSeed(analogRead(0));
}

// === ПРЕРЫВАНИЕ ДЛЯ IR ===
void irIsr() {
  ir.tick();
}

// === ГЛАВНЫЙ ЦИКЛ ===
void loop() {
  handleIR();              // читаем пульт
  if (millis() - lastMoveTime >= moveDelay) {
    lastMoveTime = millis();
    moveSnake();
    draw();
  }
}

// === ОБРАБОТКА ПУЛЬТА ===
void handleIR() {
  if (ir.available()) {
    uint8_t code = ir.readCommand();
    switch (code) {
      case IR_UP:    if (dirY == 0) { dirX = 0; dirY = -1; } break;
      case IR_DOWN:  if (dirY == 0) { dirX = 0; dirY = 1; }  break;
      case IR_LEFT:  if (dirX == 0) { dirX = -1; dirY = 0; } break;
      case IR_RIGHT: if (dirX == 0) { dirX = 1; dirY = 0; }  break;
    }
  }
}

// === ДВИЖЕНИЕ ЗМЕЙКИ ===
void moveSnake() {
  Point head = {
    byte((snake[0].x + dirX + WIDTH) % WIDTH),
    byte((snake[0].y + dirY + HEIGHT) % HEIGHT)
  };

  // столкновение с собой
  for (int i = 0; i < snakeLength; i++) {
    if (snake[i].x == head.x && snake[i].y == head.y) {
      snakeLength = 3;
      snake[0] = {2, 8};
      snake[1] = {1, 8};
      snake[2] = {0, 8};
      dirX = 1; dirY = 0;
      return;
    }
  }

  for (int i = snakeLength; i > 0; i--) {
    snake[i] = snake[i - 1];
  }
  snake[0] = head;
  snakeLength++;

  if (head.x == apple.x && head.y == apple.y) {
    spawnApple();
  } else {
    snakeLength--;  // не растём
  }
}

// === НОВОЕ ЯБЛОКО ===
void spawnApple() {
  bool conflict;
  do {
    conflict = false;
    apple.x = random(WIDTH);
    apple.y = random(HEIGHT);
    for (int i = 0; i < snakeLength; i++) {
      if (snake[i].x == apple.x && snake[i].y == apple.y) {
        conflict = true;
        break;
      }
    }
  } while (conflict);
}

// === РИСОВАНИЕ ===
void draw() {
  FastLED.clear();
  leds[xyToIndex(apple.x, apple.y)] = CRGB::Red;
  for (int i = 0; i < snakeLength; i++) {
    leds[xyToIndex(snake[i].x, snake[i].y)] = (i == 0) ? CRGB::Green : CRGB::Blue;
  }
  FastLED.show();
}

// === КООРДИНАТЫ В ИНДЕКС ЛЕНТЫ ===
int xyToIndex(byte x, byte y) {
  // для зигзагообразной матрицы
  return (y % 2 == 0) ? (y * WIDTH + x) : (y * WIDTH + (WIDTH - 1 - x));
}
