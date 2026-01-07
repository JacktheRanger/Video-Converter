# 🎬 Universal Video (to H.265 MP4) Batch Converter

<img align="right" src="https://img.shields.io/github/downloads/JacktheRanger/Video-Converter/total.svg?label=Downloads" alt="Downloads" />

[English](#english) | [中文](#中文)

---

## English

A powerful batch video converter with GUI that converts your old video files to the most stable format with NVENC hardware acceleration support, and bilingual interface (English/Chinese).

### ✨ Features

- **Universal Format Support**: Convert any video format to H.265 MP4
- **Hardware Acceleration**: NVIDIA NVENC GPU encoding for blazing fast conversion
- **Smart Remux Mode**: Container-only conversion for H.264/H.265 videos (no re-encoding, no quality loss)
- **Batch Processing**: Convert multiple files concurrently
- **Auto Detection**: Automatically detects video/audio codecs and recommends optimal settings
- **Bilingual UI**: Full English and Chinese language support
- **All Streams Support**: Preserves video, audio, and subtitle tracks
- **Progress Tracking**: Real-time conversion progress with visual progress bars
- **Error Recovery**: Automatically cleans up incomplete files on failure
- **Advanced Mode**: Multiple output formats (.mp4/.mov/.mkv), encoder selection (HEVC/H.264/AV1), and custom input paths

### 📋 Supported Formats

| Format | Type | Recommendation |
|--------|------|----------------|
| `.mts`, `.m2ts`, `.m2t`, `.ts`, `.m4v` | Container | Remux Recommended (faster, more stable) |
| `.vob`, `.mpg`, `.mpeg`, `.avi`, `.wmv`, `.flv`, `.f4v`, `.3gp`, `.webm`, `.rmvb`, `.rm` | Legacy | Transcode + Remux |

### 🔧 System Requirements (Must Read)

- **OS**: Windows 10/11 (64-bit)
- **GPU**: NVIDIA GPU with NVENC support (GTX 10 series or newer recommended)
- **Python**: 3.8+ (3.12.10 recommended)

### 🚀 Installation

#### Option A: Download EXE (Recommended - Easiest)

1. **Install FFmpeg** (Required)
   - Using winget:
     ```powershell
     winget install FFmpeg
     ```
   - Or download manually from https://ffmpeg.org/download.html
   - ⚠️ **Important**: FFmpeg must be added to system PATH
   - Verify installation:
     ```powershell
     ffmpeg -version
     ```

2. **Download the EXE**
   - Go to [Releases](../../releases) page
   - Download `Vx.x.x.Universal.Video.Converter.exe`
   - That's it! No Python required.

#### Option B: Run from Source (For developers)

1. **Install FFmpeg** (same as above)

2. **Install Python** (3.8+, recommended 3.12.10)
   - Download from: https://www.python.org/downloads/
   - No additional pip packages required - uses only built-in modules

3. **Download the script**
   - Clone or download `Vx.x.x.Universal.Video.Converter.py`

### 📖 Usage

#### Using EXE Version

1. Place `Vx.x.x.Universal.Video.Converter.exe` in the folder containing videos (or its parent folder)
2. Double-click the EXE to run
3. Select language (English/Chinese)
4. Follow the interactive prompts

#### Using Python Script

1. Place the `.py` script in the folder containing videos
2. Double-click the script or run from terminal:
   ```powershell
   python "Vx.x.x.Universal.Video.Converter.py"
   ```
3. Select language and follow prompts

#### Workflow (Basic Mode)

```
┌─────────────────────────────────────────────────────┐
│  1. Splash Screen → Select Language → Select Mode   │
│  2. Scan → Find all supported video files           │
│  3. Configure → Choose conversion mode per file     │
│     • Remux only (fast, no quality loss)            │
│     • Transcode to H.265 (re-encode)                │
│  4. Settings → NVENC preset, quality, concurrency   │
│  5. Convert → Batch process with progress display   │
│  6. Summary → Show results and file size comparison │
└─────────────────────────────────────────────────────┘
```

#### Advanced Mode

Advanced Mode provides additional options for power users who need more control over the conversion process.

##### Additional Input Formats
| Format | Description |
|--------|-------------|
| `.mp4`, `.mov`, `.mkv` | Additional formats supported in Advanced Mode |

##### Workflow (Advanced Mode)
```
┌─────────────────────────────────────────────────────┐
│  1. Splash Screen → Select Language → Advanced Mode │
│  2. Custom Path → Optional: specify input directory │
│  3. Scan → Find all supported video files           │
│  4. Output Format → Select: .mp4 / .mov / .mkv      │
│  5. Encoder → Select: HEVC / H.264 / AV1            │
│  6. Configure → Smart remux recommendation per file │
│  7. Settings → NVENC preset, quality, concurrency   │
│  8. Convert → Batch process with progress display   │
│  9. Summary → Show results and file size comparison │
└─────────────────────────────────────────────────────┘
```

##### Output Format Options
| Format | Container | Best For |
|--------|-----------|----------|
| `.mp4` | MPEG-4 Part 14 | Universal compatibility |
| `.mov` | QuickTime | Apple devices, Final Cut Pro |
| `.mkv` | Matroska | Maximum feature support |

##### Encoder Options
| Encoder | Codec | NVENC Name | Compression | Compatibility |
|---------|-------|------------|-------------|---------------|
| HEVC/H.265 | HEVC | hevc_nvenc | Best | Modern devices |
| AVC/H.264 | AVC | h264_nvenc | Good | Universal |
| AV1 | AV1 | av1_nvenc | Best | Newest devices (RTX 40+) |

##### Smart Remux Recommendation
In Advanced Mode, the tool analyzes the source video codec and compares it to your selected target encoder:
- If the source codec matches the target encoder (e.g., source is H.265 and you selected HEVC), **remux is recommended** (faster, no quality loss)
- If the source codec differs, **transcoding is recommended**

#### Configuration Options

| Option | Range | Default | Description |
|--------|-------|---------|-------------|
| NVENC Preset | p1-p7 | p5 | Speed vs quality trade-off (p1=fastest, p7=best quality) |
| Quality (CQ) | 0-51 | 21 | Lower = higher quality, higher file size |
| Deinterlace | y/n | n | Enable yadif deinterlacing filter |
| Concurrent Files | 1-10 | 3 | Number of files to process simultaneously |

### ❓ FAQ

**Q: Why doesn't this tool support Constant Bitrate (CBR) mode?**

A: This tool uses **Constant Quality (CQ)** mode instead of CBR for several reasons:

| Aspect | Constant Quality (CQ) ✅ | Constant Bitrate (CBR) |
|--------|--------------------------|------------------------|
| **Quality Consistency** | Uniform quality throughout | Quality drops in complex scenes |
| **Efficiency** | Smart bitrate allocation | Wastes bits on simple scenes |
| **Best For** | Archiving, personal collections | Live streaming, strict bandwidth |

CQ mode lets the encoder automatically allocate bitrate based on scene complexity - using less for static scenes and more for action sequences. This produces better quality at smaller file sizes compared to CBR.

**Q: What CQ value should I use?**
- **18-21**: Near-lossless quality, larger files
- **23-25**: High quality (recommended for most users)
- **28-32**: Good quality, smaller files

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
<img width="1864" height="1841" alt="image" src="https://github.com/user-attachments/assets/85e29d79-b498-4f65-bbef-678b0bd26bd7" />




### ✨ 功能特点

- **通用格式支持**: 将任意视频格式转换为 H.265 MP4
- **硬件加速**: 支持 NVIDIA NVENC GPU 编码，转换速度极快
- **智能转容器模式**: 对 H.264/H.265 视频仅转换容器（无需重新编码，无质量损失）
- **批量处理**: 支持多文件并发转换
- **自动检测**: 自动识别视频/音频编码并推荐最佳设置
- **双语界面**: 完整的中英文语言支持
- **保留所有流**: 保留视频、音频和字幕轨道
- **进度追踪**: 实时显示转换进度条
- **错误恢复**: 失败时自动清理不完整文件
- **高级模式**: 多种输出格式 (.mp4/.mov/.mkv)、编码器选择 (HEVC/H.264/AV1)、自定义输入路径

### 📋 支持的格式

| 格式 | 类型 | 建议 |
|------|------|------|
| `.mts`, `.m2ts`, `.m2t`, `.ts`, `.m4v` | 容器格式 | 建议仅转容器（更快画质更好） |
| `.vob`, `.mpg`, `.mpeg`, `.avi`, `.wmv`, `.flv`, `.f4v`, `.3gp`, `.webm`, `.rmvb`, `.rm` | 老旧格式 | 转码+转容器 |

### 🔧 环境要求（很重要）

- **操作系统**: Windows 10/11 (64位)
- **显卡**: 支持 NVENC 的 NVIDIA 显卡（推荐 GTX 10 系列或更新）
- **Python**: 3.8+（建议使用3.12.10）

### 🚀 安装步骤

#### 方式 A：下载 EXE（推荐 - 最简单）

1. **安装 FFmpeg**（必需）
   - 使用 winget：
     ```powershell
     winget install FFmpeg
     ```
   - 或手动安装 https://ffmpeg.org/download.html
   - ⚠️ **重要**：FFmpeg 必须添加到系统 PATH 环境变量
   - 验证安装：
     ```powershell
     ffmpeg -version
     ```

2. **下载 EXE 文件**
   - 前往 [Releases](../../releases) 页面
   - 下载 `Vx.x.x.Universal.Video.Converter.exe`
   - 完成！无需安装 Python。

#### 方式 B：运行源代码（适合开发者）

1. **安装 FFmpeg**（同上）

2. **安装 Python**（3.8+，推荐 3.12.10）
   - 下载地址：https://www.python.org/downloads/
   - 无需安装额外的 pip 包 - 仅使用内置模块

3. **下载脚本**
   - 克隆或下载 `Vx.x.x.Universal.Video.Converter.py`

### 📖 使用方法

#### 使用 EXE 版本

1. 将 `Vx.x.x.Universal.Video.Converter.exe` 放置在包含视频的文件夹中
2. 双击 EXE 运行
3. 选择语言（中文/英文）
4. 按照提示操作

#### 使用 Python 脚本

1. 将 `.py` 脚本放置在包含视频的文件夹中
2. 双击脚本或从终端执行：
   ```powershell
   python "Vx.x.x.Universal.Video.Converter.py"
   ```
3. 选择语言并按提示操作

#### 工作流程（基础模式）

```
┌───────────────────────────────────────────────────────┐
│  1. 开屏动画 → 选择语言 → 选择模式                      │
│  2. 扫描 → 查找所有支持的视频文件                       │
│  3. 配置 → 为每个文件选择转换模式                       │
│     • 仅转容器（快速，无质量损失）                      │
│     • 转码为 H.265（重新编码）                         │
│  4. 设置 → NVENC 预设、质量、并发数                    │
│  5. 转换 → 批量处理并显示进度                          │
│  6. 汇总 → 显示结果和文件大小对比                      │
└──────────────────────────────────────────────────────┘
```

#### 高级模式

高级模式为需要更多控制的高级用户提供额外选项。

##### 额外支持的输入格式
| 格式 | 说明 |
|------|------|
| `.mp4`, `.mov`, `.mkv` | 高级模式额外支持的格式 |

##### 工作流程（高级模式）
```
┌─────────────────────────────────────────────────────┐
│  1. 开屏动画 → 选择语言 → 高级模式                    │
│  2. 自定义路径 → 可选：指定输入目录                   │
│  3. 扫描 → 查找所有支持的视频文件                     │
│  4. 输出格式 → 选择: .mp4 / .mov / .mkv              │
│  5. 编码器 → 选择: HEVC / H.264 / AV1                │
│  6. 配置 → 智能转容器推荐                             │
│  7. 设置 → NVENC 预设、质量、并发数                   │
│  8. 转换 → 批量处理并显示进度                         │
│  9. 汇总 → 显示结果和文件大小对比                     │
└─────────────────────────────────────────────────────┘
```

##### 输出格式选项
| 格式 | 容器 | 适用场景 |
|------|------|----------|
| `.mp4` | MPEG-4 Part 14 | 通用兼容性最好 |
| `.mov` | QuickTime | Apple 设备、Final Cut Pro |
| `.mkv` | Matroska | 功能支持最全面 |

##### 编码器选项
| 编码器 | 编码标准 | NVENC 名称 | 压缩率 | 兼容性 |
|--------|----------|------------|--------|--------|
| HEVC/H.265 | HEVC | hevc_nvenc | 最佳 | 现代设备 |
| AVC/H.264 | AVC | h264_nvenc | 良好 | 通用 |
| AV1 | AV1 | av1_nvenc | 最佳 | 最新设备 (RTX 40+) |

##### 智能转容器推荐
高级模式下，工具会自动分析源视频编码并与目标编码器比较：
- 如果源编码与目标编码器匹配（例如源是 H.265 且选择了 HEVC），**建议仅转容器**（更快，无质量损失）
- 如果源编码不同，**建议转码**

#### 配置选项

| 选项 | 范围 | 默认值 | 说明 |
|------|------|--------|------|
| NVENC 预设 | p1-p7 | p5 | 速度与质量权衡（p1=最快, p7=最佳质量） |
| 质量 (CQ) | 0-51 | 21 | 越小质量越高，文件越大 |
| 去隔行 | y/n | n | 启用 yadif 去隔行扫描滤镜 |
| 并发文件数 | 1-10 | 3 | 同时处理的文件数量 |

### ❓ 常见问题

**Q: 为什么不支持恒定码率 (CBR) 模式？**

A: 本工具使用**恒定质量 (CQ)** 模式而非 CBR，原因如下：

| 方面 | 恒定质量 (CQ) ✅ | 恒定码率 (CBR) |
|------|------------------|----------------|
| **画质一致性** | 全程画质均匀一致 | 复杂场景画质下降 |
| **编码效率** | 智能分配码率 | 简单场景浪费码率 |
| **适用场景** | 视频归档、个人收藏 | 直播推流、严格带宽限制 |

CQ 模式让编码器根据画面复杂度自动分配码率 - 静态场景自动降低码率节省空间，动态打斗场景自动提高码率保证质量。相比 CBR，CQ 能以更小的文件体积获得更好的画质。

**Q: CQ 质量参数应该设置多少？**
- **18-21**: 接近无损画质，文件较大
- **23-25**: 高画质（推荐大多数用户使用）
- **28-32**: 良好画质，文件较小

### ⚠️ 注意事项

- NVENC 编码需要支持硬件编码器的 NVIDIA 显卡
- 对于非 NVIDIA 系统，可能需要修改脚本以使用软件编码
- 默认保留原始文件；可选择转换成功后删除原文件
- 对于已是 H.264/H.265 格式的文件，建议使用仅转容器模式

### 📄 许可证

GNU GPL v3.0

### 👤 作者

**Jack Ji**


























