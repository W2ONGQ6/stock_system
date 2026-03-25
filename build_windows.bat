@echo off
REM 服装库存管理系统 - Windows 打包脚本
REM 使用方法：在 Windows 上运行此脚本

echo 正在打包服装库存管理系统为 Windows 可执行文件...
echo.

REM 确保已安装必要的依赖
echo [1/3] 检查依赖...
pip install PyQt5 Pillow -q

REM 生成可执行文件
echo [2/3] 编译打包中...
pyinstaller 服装库存管理系统_windows.spec

REM 完成
echo [3/3] 打包完成！
echo.
echo 输出目录：
echo   - dist\服装库存管理系统 - 单一文件夹（可直接运行）
echo   - dist\服装库存管理系统.exe - 独立可执行文件
echo.
echo 你可以：
echo   1. 运行 dist\服装库存管理系统\服装库存管理系统.exe
echo   2. 或将 dist\服装库存管理系统 文件夹分发给他人
echo   3. 建议创建快捷方式指向 exe 文件
echo.
pause
