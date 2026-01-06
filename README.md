# 🎬 Universal Video to H.265 MP4 Batch Converter

[English](#english) | [中文](#中文)

---

## English

A powerful batch video converter with GUI that converts your old video files to the most stable format with NVENC hardware acceleration support, and bilingual interface (English/Chinese).

<img width="1823" height="1548" alt="image" src="https://github.com/user-attachments/assets/6e3ffbd8-a23b-4919-8731-cfaf17cfcba4" />

### ✨ Features

- **Universal Format Support**: Convert any video format to H.265 MP4
- **Hardware Acceleration**: NVIDIA NVENC GPU encoding for blazing fast conversion
- **Smart Remux Mode**: Container-only conversion for H.264/H.265 videos (no re-encoding, no quality loss)
- **Batch Processing**: Convert multiple files concurrently
- **Auto Detection**: Automatically detects video/audio codecs and recommends optimal settings
- **Cool Splash Screen**: Animated ASCII art intro with system hardware detection
- **Bilingual UI**: Full English and Chinese language support
- **All Streams Support**: Preserves video, audio, and subtitle tracks
- **Progress Tracking**: Real-time conversion progress with visual progress bars
- **Error Recovery**: Automatically cleans up incomplete files on failure

### 📋 Supported Formats

| Format | Type | Recommendation |
|--------|------|----------------|
| `.mts`, `.m2ts`, `.m2t`, `.ts`, `.m4v` | Container | Remux Recommended (faster, more stable) |
| `.vob`, `.mpg`, `.avi`, `.wmv`, `.flv`, `.3gp` | Legacy | Transcode + Remux |

### 🔧 System Requirements (Must Read)

- **OS**: Windows 10/11 (64-bit)
- **GPU**: NVIDIA GPU with NVENC support (GTX 10 series or newer recommended)
- **Python**: 3.8+ (3.12.10 recommended)

### 🚀 Installation

1. **Install FFmpeg** (Required)
   - Option A: Using winget
     ```powershell
     winget install FFmpeg
     ```
   - Option B: Manual installation from https://ffmpeg.org/download.html
   - ⚠️ **Important**: FFmpeg must be added to system PATH
   - Verify installation:
     ```powershell
     ffmpeg -version
     ```

2. **Install Python** (3.8+, recommended 3.12.10)
   - Download from: https://www.python.org/downloads/
   - No additional pip packages required - uses only built-in modules

3. **Download the script**
   - Download or clone the script to your desired location

### 📖 Usage

#### Basic Usage

1. Place the script in the folder containing videos (or its parent folder)
2. Double-click the script (recommended) or run it from terminal:
   ```powershell
   python "(Vx.xx) Python .any to .mp4 Video Converter.py"
   ```
3. Select language (English/Chinese)
4. Follow the interactive prompts

#### Workflow

```
┌─────────────────────────────────────────────────────┐
│  1. Splash Screen → Select Language                 │
│  2. Scan → Find all supported video files           │
│  3. Configure → Choose conversion mode per file     │
│     • Remux only (fast, no quality loss)            │
│     • Transcode to H.265 (re-encode)                │
│  4. Settings → NVENC preset, quality, concurrency   │
│  5. Convert → Batch process with progress display   │
│  6. Summary → Show results and file size comparison │
└─────────────────────────────────────────────────────┘
```

#### Configuration Options

| Option | Range | Default | Description |
|--------|-------|---------|-------------|
| NVENC Preset | p1-p7 | p5 | Speed vs quality trade-off (p1=fastest, p7=best quality) |
| Quality (CQ) | 0-51 | 21 | Lower = higher quality, higher file size |
| Deinterlace | y/n | n | Enable yadif deinterlacing filter |
| Concurrent Files | 1-10 | 3 | Number of files to process simultaneously |

### 📸 Screenshots

The converter features a cool ASCII art splash screen that displays:
- Animated "VIDEO CONVERTER" banner
- System hardware info (CPU, GPU, RAM)
- NVENC encoder/decoder count

### ⚠️ Notes

- NVENC encoding requires an NVIDIA GPU with hardware encoder support
- For non-NVIDIA systems, the script may need modification to use software encoding
- Original files are preserved by default; optional delete-after-conversion is available
- Remux mode is recommended for files already in H.264/H.265 format

### 📄 License

GNU GPL v3.0

### 👤 Author

**Jack Ji**

---

## 中文

一款功能强大的批量视频GUI转换工具， 将您的老视频文件转换最稳定的格式。

### ✨ 功能特点

- **通用格式支持**: 将任意视频格式转换为 H.265 MP4
- **硬件加速**: 支持 NVIDIA NVENC GPU 编码，转换速度极快
- **智能转容器模式**: 对 H.264/H.265 视频仅转换容器（无需重新编码，无质量损失）
- **批量处理**: 支持多文件并发转换
- **自动检测**: 自动识别视频/音频编码并推荐最佳设置
- **炫酷开屏**: ASCII 艺术动画开屏，显示系统硬件信息
- **双语界面**: 完整的中英文语言支持
- **保留所有流**: 保留视频、音频和字幕轨道
- **进度追踪**: 实时显示转换进度条
- **错误恢复**: 失败时自动清理不完整文件

### 📋 支持的格式

| 格式 | 类型 | 建议 |
|------|------|------|
| `.mts`, `.m2ts`, `.m2t`, `.ts`, `.m4v` | 容器格式 | 建议仅转容器（更快画质更好） |
| `.vob`, `.mpg`, `.avi`, `.wmv`, `.flv`, `.3gp` | 老旧格式 | 转码+转容器 |

### 🔧 环境要求（很重要）

- **操作系统**: Windows 10/11 (64位)
- **显卡**: 支持 NVENC 的 NVIDIA 显卡（推荐 GTX 10 系列或更新）
- **Python**: 3.8+（建议3.12.10）

### 🚀 安装步骤

1. **安装 FFmpeg**（必需）
   - 方式 A：使用 winget
     ```powershell
     winget install FFmpeg
     ```
   - 方式 B：手动安装 https://ffmpeg.org/download.html
   - ⚠️ **重要**：FFmpeg 必须添加到系统 PATH 环境变量
   - 验证安装：
     ```powershell
     ffmpeg -version
     ```

2. **安装 Python**（3.8+，推荐 3.12.10）
   - 下载地址：https://www.python.org/downloads/
   - 无需安装额外的 pip 包 - 仅使用内置模块

3. **下载脚本**
   - 下载或克隆脚本到目标位置

### 📖 使用方法

#### 基本用法

1. 将脚本放置在包含视频的文件夹中（或其父文件夹）
2. 双击脚本运行（推荐）或从终端执行:
   ```powershell
   python "(Vx.xx) Python .any to .mp4 Video Converter.py"
   ```
3. 选择语言（英文/中文）
4. 按照交互式提示操作

#### 工作流程

```
┌─────────────────────────────────────────────────────┐
│  1. 开屏动画 → 选择语言                              │
│  2. 扫描 → 查找所有支持的视频文件                     │
│  3. 配置 → 为每个文件选择转换模式                     │
│     • 仅转容器（快速，无质量损失）                    │
│     • 转码为 H.265（重新编码）                       │
│  4. 设置 → NVENC 预设、质量、并发数                  │
│  5. 转换 → 批量处理并显示进度                        │
│  6. 汇总 → 显示结果和文件大小对比                     │
└─────────────────────────────────────────────────────┘
```

#### 配置选项

| 选项 | 范围 | 默认值 | 说明 |
|------|------|--------|------|
| NVENC 预设 | p1-p7 | p5 | 速度与质量权衡（p1=最快, p7=最佳质量） |
| 质量 (CQ) | 0-51 | 21 | 越小质量越高，文件越大 |
| 去隔行 | y/n | n | 启用 yadif 去隔行扫描滤镜 |
| 并发文件数 | 1-10 | 3 | 同时处理的文件数量 |

### 📸 界面截图

转换器具有炫酷的 ASCII 艺术开屏动画，显示:
- 动画 "VIDEO CONVERTER" 横幅
- 系统硬件信息（CPU、GPU、内存）
- NVENC 编码器/解码器数量

### ⚠️ 注意事项

- NVENC 编码需要支持硬件编码器的 NVIDIA 显卡
- 对于非 NVIDIA 系统，可能需要修改脚本以使用软件编码
- 默认保留原始文件；可选择转换成功后删除原文件
- 对于已是 H.264/H.265 格式的文件，建议使用仅转容器模式

### 📄 许可证

GNU GPL v3.0

### 👤 作者

**Jack Ji**





