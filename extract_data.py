#!/usr/bin/env python3
"""
月薪猫动画数据提取工具

功能：从原始 STM32 项目的 OLED_Data.c 文件中提取 YueXinMao 动画数据
输出：生成适用于 ESP32-S3 的 yuexinmao_data.h 文件

使用方法：
    python extract_data.py <OLED_Data.c路径> [输出路径]

示例：
    python extract_data.py ~/月薪猫-OLED/Hardware/OLED_Data.c
    python extract_data.py OLED_Data.c -o yuexinmao_data.h
"""

import re
import sys
import argparse

def extract_array_data(content, array_name="YueXinMao"):
    """从C源码中提取数组数据"""
    # 查找数组定义
    pattern = rf'const\s+uint8_t\s+{array_name}\s*\[.*?\]\s*=\s*\{{(.*?)\}};'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        print(f"错误：未找到 {array_name} 数组定义")
        return None
    
    return match.group(1)

def parse_numbers(data_str):
    """解析数字数据"""
    # 提取所有十六进制或十进制数字
    numbers = re.findall(r'0[xX][0-9a-fA-F]+|\d+', data_str)
    return [int(n, 0) for n in numbers]

def generate_header(data, output_path="yuexinmao_data.h"):
    """生成ESP32-S3兼容的头文件"""
    header = '''/*
 * 月薪猫动画数据 - ESP32-S3 版本
 * 
 * 自动生成，请勿手动修改
 * 数据来源：原始 STM32 项目
 */

#ifndef YUEXINMAO_DATA_H
#define YUEXINMAO_DATA_H

#include <Arduino.h>

// 动画数据存储在 PROGMEM 中以节省 RAM
const uint8_t YueXinMao[22][8][128] PROGMEM = {
'''
    
    # 重塑数据为 [22][8][128]
    if len(data) != 22 * 8 * 128:
        print(f"警告：数据大小不匹配，期望 {22*8*128}，实际 {len(data)}")
        # 尝试填充或截断
        data = data[:22*8*128] + [0] * max(0, 22*8*128 - len(data))
    
    for frame in range(22):
        header += f'    // 第{frame}帧\n'
        header += '    {\n'
        for page in range(8):
            offset = (frame * 8 + page) * 128
            row_data = data[offset:offset + 128]
            hex_str = ', '.join(f'0x{b:02X}' for b in row_data)
            header += f'        {{{hex_str}}}'
            if page < 7:
                header += ','
            header += '\n'
        header += '    }'
        if frame < 21:
            header += ','
        header += '\n'
    
    header += '''};

#endif
'''
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(header)
    
    print(f"✓ 数据已保存到 {output_path}")
    print(f"  - 帧数: 22")
    print(f"  - 总字节: {len(data)}")

def main():
    parser = argparse.ArgumentParser(description='提取月薪猫动画数据')
    parser.add_argument('input', help='OLED_Data.c 文件路径')
    parser.add_argument('-o', '--output', default='yuexinmao_data.h', help='输出文件路径')
    args = parser.parse_args()
    
    print(f"读取文件: {args.input}")
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"错误：无法读取文件 - {e}")
        sys.exit(1)
    
    print("提取数组数据...")
    data_str = extract_array_data(content)
    if data_str is None:
        sys.exit(1)
    
    print("解析数字...")
    data = parse_numbers(data_str)
    print(f"找到 {len(data)} 个数据字节")
    
    print("生成头文件...")
    generate_header(data, args.output)
    
    print("完成!")

if __name__ == '__main__':
    main()
