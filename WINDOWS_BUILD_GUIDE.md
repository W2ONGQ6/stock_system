# 服装库存管理系统 - Windows 打包指南

## 快速开始

### 方式 1：使用 Python 脚本（推荐）

在 Windows 上用 Python 运行：

```bash
python build_windows.py
```

脚本会自动：
- ✓ 安装必要的依赖
- ✓ 检查所需文件
- ✓ 清理旧的构建文件
- ✓ 生成 Windows 可执行文件

### 方式 2：手动使用 PyInstaller

#### 1. 安装依赖
```bash
pip install PyQt5 Pillow PyInstaller
```

#### 2. 生成可执行文件
```bash
pyinstaller 服装库存管理系统_windows.spec
```

#### 3. 找到生成的文件
输出在 `dist/` 目录：
```
dist/
└── 服装库存管理系统/
    ├── 服装库存管理系统.exe  (可执行文件)
    ├── _internal/           (依赖库)
    └── app.ico             (应用图标)
```

## 文件说明

| 文件 | 说明 |
|------|------|
| `stock_system.py` | 主程序源代码 |
| `gen_app_ico.py` | 应用图标生成脚本 |
| `app.ico` | 应用图标文件 |
| `服装库存管理系统_windows.spec` | Windows 打包配置 |
| `build_windows.py` | 打包脚本（Python） |
| `build_windows.bat` | 打包脚本（Batch） |

## 打包输出

### dist/服装库存管理系统/ 模式（推荐分发）

**优点：**
- ✓ 启动速度快
- ✓ 易于维护和更新
- ✓ 支持 onefile 模式

**使用方式：**
1. 直接运行：`double-click dist/服装库存管理系统/服装库存管理系统.exe`
2. 复制整个文件夹分发给用户
3. 建议为用户创建快捷方式

### 进阶选项

如需单一 EXE 文件（不依赖 _internal 文件夹），编辑 spec 文件：

```python
exe = EXE(
    ...,
    onefile=True,  # 添加这一行
    ...
)
```

## 常见问题

### 1. "ModuleNotFoundError: No module named 'PyQt5'"
```bash
pip install PyQt5
```

### 2. "ModuleNotFoundError: No module named 'pymysql'" / "sqlite3"
编辑 `服装库存管理系统_windows.spec`，在 `hiddenimports` 中添加：
```python
hiddenimports=['PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets', 'sqlite3'],
```

### 3. 打包后 EXE 很大（200MB+）
这是正常的，包含了 Python 运行环境。可以用 UPX 压缩：
```bash
# 下载 UPX: https://upx.github.io/
pyinstaller 服装库存管理系统_windows.spec --upx-dir=<upx目录>
```

### 4. 首次运行速度慢
正常现象，程序在首次启动时会解压依赖库到临时目录。后续运行会更快。

## 分发建议

### 打包分发
1. 进入 `dist/服装库存管理系统/` 文件夹
2. 创建名为 `服装库存管理系统` 的文件夹
3. 将 `dist/服装库存管理系统/` 中的所有文件复制进去
4. 创建压缩包（.zip）分发

### 创建快捷方式
1. 右键点击 `服装库存管理系统.exe`
2. 选择 **发送到** → **桌面（创建快捷方式）**
3. 给用户发送快捷方式和应用文件夹

## 技术细节

### 打包配置详解

```python
# 源代码文件
a = Analysis(['stock_system.py'], ...)

# 隐藏的导入（PyQt5 插件等）
hiddenimports=['PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets']

# 应用程序设置
exe = EXE(
    ...,
    console=False,      # 不显示控制台窗口
    icon='app.ico',     # 应用图标
    ...
)

# 输出配置
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    ...
)
```

## 更新日志

### v1.0 (2026-03-25)
- ✓ 初始 Windows 打包支持
- ✓ 自动化打包脚本
- ✓ 应用图标集成

---

**需要帮助？**
1. 检查依赖是否完整
2. 确保 `stock_system.py` 和 `app.ico` 在同一目录
3. 查看打包日志寻找错误信息
