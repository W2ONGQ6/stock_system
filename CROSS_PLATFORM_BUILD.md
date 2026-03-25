# Mac 上打包 Windows Exe 的方案

PyInstaller 本质上是平台特定的工具 - 在 Mac 上运行只能生成 Mac 应用。要在 Mac 上生成 Windows exe，有以下方案：

## 方案对比

| 方案 | 难度 | 可靠性 | 速度 | 推荐度 |
|------|------|--------|------|--------|
| **方案 1：GitHub Actions** | ⭐ | ⭐⭐⭐⭐⭐ | 中 | ⭐⭐⭐⭐⭐ |
| **方案 2：虚拟机 (Parallels/VMware)** | ⭐⭐ | ⭐⭐⭐⭐ | 慢 | ⭐⭐⭐⭐ |
| **方案 3：Docker + Wine** | ⭐⭐⭐ | ⭐⭐⭐ | 中 | ⭐⭐⭐ |
| **方案 4：Conda native-windows** | ⭐⭐⭐ | ⭐⭐ | 快 | ⭐⭐ |

---

## ✅ 方案 1：使用 GitHub Actions（最推荐）

完全免费，自动化，可靠性最高。

### 准备工作

1. 将代码推送到 GitHub
2. 创建 `.github/workflows/build.yml`

### 工作流配置

```yaml
name: Build Windows EXE

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: windows-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install PyQt5 Pillow PyInstaller
    
    - name: Build EXE
      run: |
        pyinstaller 服装库存管理系统_windows.spec
    
    - name: Upload artifact
      uses: actions/upload-artifact@v3
      with:
        name: 服装库存管理系统-windows
        path: dist/服装库存管理系统/
    
    - name: Create Release
      if: startsWith(github.ref, 'refs/tags/')
      uses: softprops/action-gh-release@v1
      with:
        files: dist/服装库存管理系统/**/*
```

### 使用流程

1. 代码有更新后 push 到 GitHub
2. GitHub Actions 自动在 Windows 上打包
3. 在 Actions 页面下载 artifacts (exe)
4. 或创建 Release tag 自动上传

### 优势
- ✓ 完全自动化
- ✓ 在真正的 Windows 环境运行
- ✓ 免费（GitHub 赠送分钟数）
- ✓ 可靠性高
- ✓ 无需本地虚拟机

---

## 🖥️ 方案 2：使用虚拟机

如果需要本地控制，可以用虚拟机方案。

### 选项 A：Parallels Desktop for Mac

```bash
# 1. 在 Parallels 中安装 Windows
# 2. 在 Windows 中安装 Python
# 3. 运行 build_windows.py

python build_windows.py
```

### 选项 B：Docker

```bash
# 这个方案比较复杂，不太推荐
```

---

## 🍷 方案 3：Wine（不推荐）

Wine 可以在 Mac 上运行 Windows 程序，但很容易出问题。

```bash
# 安装 Wine
brew install wine

# 在 Wine 中运行 Python（很复杂...）
```

**不推荐原因**：
- 需要 Windows Python
- 依赖可能无法正确加载
- PyQt5 GUI 可能有显示问题
- 经常出 bug

---

## 🔄 方案 4：Conda 跨平台编译（不推荐）

```bash
# 理论上可以用 conda-pack + Windows targets
conda install -c conda-forge mingw-w64
```

**不推荐原因**：
- 支持不完整
- PyQt5 兼容性问题
- 容易失败

---

## 我的建议

### 场景 1：只是偶尔打包一次
→ 使用 **虚拟机**（Parallels）或借一台 Windows 电脑

### 场景 2：经常需要打包，代码在 GitHub
→ 使用 **GitHub Actions**（强烈推荐！）

### 场景 3：需要在 Mac 本地打包
→ 用 **Parallels 虚拟机**

---

## GitHub Actions 详细步骤

### 1. 创建文件夹和文件

```
.github/
└── workflows/
    └── build.yml
```

### 2. 复制配置

见上面的 `build.yml` 完整代码

### 3. 提交到 GitHub

```bash
git add .github/workflows/build.yml
git commit -m "Add Windows build workflow"
git push
```

### 4. 首次配置权限（如果需要）

在 GitHub 仓库 Settings → Actions → General：
- 确保 "Allow all actions and reusable workflows" 选中
- 确保 Workflow 有读写权限

### 5. 查看构建结果

1. 进入仓库 → Actions 标签
2. 看到 "Build Windows EXE" workflow
3. 点击 → 等待完成（通常 3-5 分钟）
4. 下载 artifacts

### 6. 自动标签版本发布（增强版）

```bash
# 当你创建 git tag 时自动创建 Release
git tag v1.0.0
git push --tags
```

GitHub 会自动创建 Release 并上传 exe 文件。

---

## 快速测试 Action

想快速测试，可以创建简单版本：

```yaml
name: Test Build

on: [push]

jobs:
  test:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install PyQt5 Pillow PyInstaller
      - run: pyinstaller 服装库存管理系统_windows.spec
```

---

## 总结

| 需求 | 推荐方案 |
|------|---------|
| 代码在 GitHub，偶尔打包 | ✅ **GitHub Actions** |
| 需要本地控制 | ✅ **Parallels 虚拟机** |
| 想快速打包一次 | ✅ **借 Windows 电脑** |
| 尝试 Wine 或交叉编译 | ❌ **不推荐** |

**最终建议：使用 GitHub Actions，既自动化又可靠，完全免费。**
