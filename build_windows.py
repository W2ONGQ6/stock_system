#!/usr/bin/env python3
"""
服装库存管理系统 - Windows 打包脚本
在 Windows 上运行此脚本来生成 exe 文件

使用方法：
    python build_windows.py
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(cmd, description=""):
    """运行命令行指令"""
    if description:
        print(f"\n[*] {description}")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[!] 错误: {e}")
        if e.stderr:
            print(e.stderr)
        return False

def main():
    print("=" * 60)
    print("  服装库存管理系统 - Windows 打包工具")
    print("=" * 60)
    
    # 检查依赖
    print("\n[1/3] 检查并安装依赖...")
    if not run_command("pip install -q PyQt5 Pillow PyInstaller", "安装必要的 Python 包"):
        print("[!] 安装依赖失败")
        return False
    
    # 检查必要文件
    print("\n[2/3] 检查必要文件...")
    required_files = ['stock_system.py', '服装库存管理系统_windows.spec', 'app.ico']
    for file in required_files:
        if not os.path.exists(file):
            print(f"[!] 错误: 找不到文件 {file}")
            return False
        print(f"    ✓ {file}")
    
    # 清理旧的构建文件
    print("\n[3/3] 清理旧文件并打包...")
    cleanup_dirs = ['build', 'dist', '__pycache__']
    for dir_name in cleanup_dirs:
        if os.path.exists(dir_name):
            import shutil
            shutil.rmtree(dir_name)
            print(f"    ✓ 删除 {dir_name}/")
    
    # 运行 PyInstaller
    spec_file = "服装库存管理系统_windows.spec"
    if not run_command(f"pyinstaller {spec_file}", f"使用 PyInstaller 打包({spec_file})"):
        print("[!] 打包失败")
        return False
    
    # 成功
    print("\n" + "=" * 60)
    print("  ✓ 打包成功!")
    print("=" * 60)
    print("\n输出目录:")
    print("  • dist/服装库存管理系统/    (文件夹版)")
    print("    └─ 服装库存管理系统.exe   (可执行文件)")
    print("\n使用说明:")
    print("  1. 直接运行: dist/服装库存管理系统/服装库存管理系统.exe")
    print("  2. 分发方式: 将 dist/服装库存管理系统 文件夹复制给用户")
    print("  3. 创建快捷方式: 右键 exe 文件 -> 发送到 -> 桌面 (创建快捷方式)")
    print("\n注意:")
    print("  • 首次运行可能较慢 (解压依赖)")
    print("  • 需要 Python 3.7+ 和 PyQt5")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
