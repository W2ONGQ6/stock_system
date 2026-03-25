# 🚀 快速指南：在 Mac 上用 GitHub Actions 打包 Windows EXE

## 推荐方案：GitHub Actions 自动打包

唯一能在 Mac 上**可靠地**打包 Windows exe 的方法是使用 GitHub Actions。以下是快速步骤：

---

## ⚡ 5 分钟快速开始

### 第 1 步：初始化 Git 仓库

```bash
cd ~/Documents/algorithm/stock_system

# 如果还没有 git 仓库
git init
git add .
git commit -m "Initial commit: stock system project"
```

### 第 2 步：创建 GitHub 仓库

1. 登录 [github.com](https://github.com)
2. 点击 **Create a new repository**
3. 仓库名：`stock_system`（或任意名称）
4. **不要勾选** "Initialize with README"（用现有代码）
5. 点击 **Create repository**

### 第 3 步：推送代码到 GitHub

```bash
git branch -M main
git remote add origin https://github.com/你的用户名/stock_system.git
git push -u origin main
```

> 💡 **提示**：如果 `git push` 失败，用 GitHub Desktop 或 Web UI 上传代码也可以。

### 第 4 步：自动打包

#### 选项 A：自动触发
只需正常开发即可，每次 push 时自动打包：
1. 进入 GitHub 仓库
2. 点击 **Actions** 标签
3. 看到 "Build Windows EXE" workflow（可能需要等 1-2 分钟首次显示）
4. 点击进入查看构建进度

#### 选项 B：手动触发
1. 进入 **Actions** 标签
2. 左侧选择 "Build Windows EXE"
3. 点击 **Run workflow**
4. 等待完成（3-5 分钟）

### 第 5 步：下载 EXE

构建完成后：

1. **方法 1：从 Artifacts 下载**
   - 点击最新的 workflow run
   - 找到 "Artifacts" 部分
   - 下载 `服装库存管理系统-windows-zip.zip`
   - 解压即可使用

2. **方法 2：创建 Release 版本（推荐）**
   ```bash
   git tag v1.0.0
   git push --tags
   ```
   - GitHub 自动创建 Release
   - 自动上传 exe 文件
   - 用户可直接下载使用

---

## 📋 文件清单

我已为你准备好所有文件，位置如下：

```
stock_system/
├── .github/workflows/
│   └── build-windows.yml         ← GitHub Actions 配置
├── stock_system.py               ← 主程序
├── gen_app_ico.py                ← 图标生成
├── app.ico                       ← 应用图标
├── 服装库存管理系统_windows.spec  ← Windows 打包配置
├── requirements.txt              ← Python 依赖列表
├── build_windows.py              ← 本地打包脚本
├── build_windows.bat             ← Batch 打包脚本
├── WINDOWS_BUILD_GUIDE.md        ← 详细打包指南
├── CROSS_PLATFORM_BUILD.md       ← 跨平台方案说明
└── README.md                     ← 项目说明
```

---

## 🎯 工作流程详解

```
你在 Mac 上开发
    ↓
git push 到 GitHub
    ↓
GitHub Actions 自动触发
    ↓
在 Windows 云服务器上运行 PyInstaller
    ↓
生成 EXE 文件
    ↓
上传到 Artifacts 供下载
    ↓
（可选）创建 Release 版本
    ↓
用户下载 EXE 直接运行
```

---

## ✅ 检查清单

- [ ] 代码已推送到 GitHub
- [ ] 进入 Actions 标签可以看到 "Build Windows EXE"
- [ ] workflow 成功运行（绿色 ✓）
- [ ] 可以下载 artifacts 或 Release

---

## 🔧 常见问题

### Q1: 看不到 workflow？
**A:** GitHub Actions 首次显示可能需要 1-2 分钟。刷新页面或等待。

### Q2: workflow 报错？
**A:** 通常是依赖问题。检查：
1. `requirements.txt` 中的包是否正确
2. `gen_app_ico.py` 是否依赖其他文件
3. `app.ico` 是否存在

### Q3: 下载的 EXE 能在 Windows 上运行吗？
**A:** 可以！这是在真正的 Windows 环境打包的。但首次运行会慢（解压依赖）。

### Q4: 如何分发给用户？
**A:** 两种方式：
- 方式 1：分享 Release 链接（GitHub 自动托管）
- 方式 2：把 EXE 文件夹压缩后上传到云盘（阿里云盘、百度网盘等）

### Q5: 改了代码后需要重新打包吗？
**A:** 是的，每次改代码后重新 push 即可自动打包。

---

## 📊 成本/资源

- **GitHub Actions 分钟数**：免费 2000 分钟/月
- **每次打包耗时**：3-5 分钟
- **成本**：完全免费？

---

## 🎓 进阶用法

### 1. 规划版本管理

```bash
# 开发版本
git push origin main  # 自动构建到 artifacts

# 发布稳定版
git tag v1.0.0
git push --tags  # 自动创建 Release 并上传 EXE
```

### 2. 多分支构建

编辑 `.github/workflows/build-windows.yml`，改这部分：
```yaml
on:
  push:
    branches: [ main, master, develop, release/* ]
```

### 3. 定时构建

每周自动打包一次：
```yaml
on:
  schedule:
    - cron: '0 2 * * 0'  # 每周日凌晨 2 点
```

---

## 🚨 重要提示

1. ✅ **第一次设置后基本不用管**
   - 后续只需正常开发
   - 自动打包、自动上传

2. ✅ **GitHub 完全安全**
   - 代码是你的
   - GitHub Actions 是沙箱环境
   - 不会泄露私密信息

3. ⚠️ **私有仓库有分钟数限制**
   - 公开仓库：无限制
   - 私有仓库：2000 分钟/月 (免费)
   - 够用（2000 分钟 = 400+ 次构建）

---

## 📞 需要帮助？

### 本地打包（作为备选）
```bash
# 在 Windows 上或虚拟机中
python build_windows.py
```

### 手动打包
```bash
pip install PyQt5 Pillow PyInstaller
pyinstaller 服装库存管理系统_windows.spec
# 输出：dist/服装库存管理系统/服装库存管理系统.exe
```

---

## 总结

| 步骤 | 耗时 | 操作 |
|------|------|------|
| 1. 初始化 | 1 min | `git init && git add .` |
| 2. 创建 GitHub | 2 min | Web UI 创建仓库 |
| 3. 推送代码 | 1 min | `git push origin main` |
| 4. 查看结果 | 3 min | Actions 标签里等待 |
| **总计** | **10 min** | **一次性设置** |

**之后每次开发：**
- Mac 上正常开发
- `git push` 
- GitHub 自动打包
- 下载 EXE 使用

**就这么简单。** 🎉
