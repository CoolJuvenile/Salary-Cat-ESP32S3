/*
 * 月薪猫 OLED 动画 - ESP32-S3 版本
 * 
 * 硬件：ESP32-S3 N16R8 + 0.9寸 SSD1306 OLED (128x64)
 * 
 * 接线：
 *   OLED SCL -> ESP32-S3 GPIO18
 *   OLED SDA -> ESP32-S3 GPIO17
 *   OLED VCC -> 3.3V
 *   OLED GND -> GND
 * 
 * 库依赖：
 *   - Adafruit SSD1306
 *   - Adafruit GFX Library
 */

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// ============ 引脚配置 ============
#define SDA_PIN 17
#define SCL_PIN 18

// ============ OLED配置 ============
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
#define SCREEN_ADDRESS 0x3C

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// ============ 动画配置 ============
#define FRAME_COUNT 22
#define FRAME_DELAY 20

// ============ 动画数据 ============
#include "yuexinmao_data.h"

// ============ 全局变量 ============
int16_t x_offset = -SCREEN_WIDTH;

void setup() {
    Serial.begin(115200);
    Serial.println("月薪猫 OLED 动画 - ESP32-S3");
    
    Wire.begin(SDA_PIN, SCL_PIN);
    
    if (!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
        Serial.println("OLED 初始化失败!");
        for (;;);
    }
    
    display.clearDisplay();
    display.display();
    Serial.println("开始播放动画...");
}

void loop() {
    for (uint8_t frame = 0; frame < FRAME_COUNT; frame++) {
        display.clearDisplay();
        drawFrame(frame, x_offset);
        display.display();
        delay(FRAME_DELAY);
        
        x_offset++;
        if (x_offset > SCREEN_WIDTH) {
            x_offset = -SCREEN_WIDTH;
        }
    }
}

void drawFrame(uint8_t frame, int16_t x_off) {
    for (uint8_t page = 0; page < 8; page++) {
        for (uint8_t col = 0; col < 128; col++) {
            int16_t img_col = col - x_off;
            if (img_col >= 0 && img_col < 128) {
                uint8_t data = pgm_read_byte(&YueXinMao[frame][page][img_col]);
                for (uint8_t bit = 0; bit < 8; bit++) {
                    if (data & (1 << bit)) {
                        display.drawPixel(col, page * 8 + bit, SSD1306_WHITE);
                    }
                }
            }
        }
    }
}
