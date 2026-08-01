# 月薪猫 OLED 动画 - ESP32-S3 版本

将原始 STM32 月薪猫动画项目适配到 ESP32-S3 + 0.9寸 OLED 显示屏。

## 硬件需求

| 组件 | 型号 |
|------|------|
| 开发板 | ESP32-S3 N16R8 |
| 显示屏 | 0.9寸 SSD1306 OLED (128×64, I2C) |

## 接线方式

```
OLED       ESP32-S3
─────      ────────
VCC   →    3.3V
GND   →    GND
SCL   →    GPIO18
SDA   →    GPIO17
```

> 如需修改引脚，请更改 `月薪猫-ESP32S3.ino` 中的 `SDA_PIN` 和 `SCL_PIN` 定义。

## 项目结构

```
月薪猫-ESP32S3/
├── 月薪猫-ESP32S3.ino   # 主程序
├── yuexinmao_data.h      # 动画数据（需生成）
├── extract_data.py       # 数据提取工具
└── README.md             # 本文件
```

## 使用步骤

### 1. 安装 Arduino 库

在 Arduino IDE 中安装以下库：

```
工具 → 管理库 → 搜索并安装：
- Adafruit SSD1306
- Adafruit GFX Library
```

### 2. 配置 Arduino IDE

```
工具 → 开发板 → ESP32S3 Dev Module
工具 → Flash Size → 16MB (128Mb)
工具 → PSRAM → OPI PSRAM
```

### 3. 提取动画数据

在电脑上运行数据提取脚本：

```bash
python extract_data.py /path/to/月薪猫-OLED/Hardware/OLED_Data.c -o yuexinmao_data.h
```

然后将生成的 `yuexinmao_data.h` 复制到项目目录。

### 4. 上传程序

1. 用 USB 连接 ESP32-S3
2. 选择正确的串口
3. 点击"上传"按钮

## 参数调整

在 `月薪猫-ESP32S3.ino` 中可调整：

```cpp
#define FRAME_DELAY 20    // 帧延时(ms)，越小动画越快
#define SCREEN_ADDRESS 0x3C  // OLED I2C地址，部分屏幕为0x3D
```

## 常见问题

### OLED 不亮
- 检查接线是否正确
- 尝试将 `SCREEN_ADDRESS` 改为 `0x3D`
- 确认 OLED 供电正常

### 编译错误
- 确保安装了所需的库
- 确认开发板选择正确

### 动画显示异常
- 确保 `yuexinmao_data.h` 已正确生成
- 检查数据是否完整（应为 22×8×128 = 22528 字节）

## 原始项目

本项目基于 [江协科技](https://jiangxiekeji.com) 的 OLED 模版程序改编。

原始项目路径：`月薪猫-OLED/`

## 许可证

MIT License
