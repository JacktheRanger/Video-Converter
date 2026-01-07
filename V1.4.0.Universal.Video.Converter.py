import os
import subprocess
import sys
import re
import time
import shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from collections import OrderedDict
import random

# ================================
# 国际化语言字典
# ================================
LANG = {
    'en': {
        # Main interface
        'title': 'Universal Video to H.265 MP4 Batch Converter',
        'supported_formats': 'Supported formats:',
        'remux_recommended': 'Recommended for remux only',
        'transcode_recommended': 'Recommended for transcode + remux',
        'current_path': 'Current path',
        'searching_files': 'Searching for video files...',
        'no_files_found': 'No supported video files found',
        'supported_formats_list': 'Supported formats',
        'press_enter_exit': 'Press Enter to exit...',
        'found_files': 'Found {count} video files:',
        'files_count': '{count} file(s)',
        
        # Existing files
        'existing_files_found': 'Found {count} existing MP4 files',
        'overwrite_prompt': 'Overwrite existing files? [y/n, default n]: ',
        'will_overwrite': '✓ Will overwrite existing files',
        'will_skip': '✓ Will skip existing files',
        
        # Conversion mode
        'select_mode': 'Select Conversion Mode',
        'batch_mode_prompt': 'Apply same settings to all files of the same format? [y/n, default n]: ',
        'batch_mode_enabled': '✓ Batch mode: will use unified settings for each format',
        'format_info': 'Format {ext} ({count} file(s)):',
        'remux_only_recommended': '  Remux only recommended',
        'transcode_recommended_msg': '  Transcode + remux recommended',
        'remux_prompt_y': '  Convert container to .mp4 only? [y/n, default y]: ',
        'remux_prompt_n': '  Convert container to .mp4 only? [y/n, default n]: ',
        'transcode_audio_prompt': '  Transcode non-AAC audio to AAC? [y/n, default y]: ',
        'mode_remux_only': 'remux only',
        'mode_transcode_h265': 'transcode to H.265',
        'audio_transcode_aac': 'transcode to AAC',
        'audio_copy': 'copy audio',
        
        # File by file
        'video_codec': 'Video codec',
        'audio_codec': 'Audio codec',
        'format_remux_recommended': 'Format {ext} - remux only recommended',
        'format_transcode_recommended': 'Format {ext} - transcode + remux recommended',
        'remux_prompt_detail': '  Convert container to .mp4 only (faster, no quality loss)? [y/n, default {default}]: ',
        'will_remux': '  ✓ Will remux only (container change)',
        'will_transcode': '  ✓ Will re-encode to H.265',
        'audio_incompatible': '  ⚠ Audio {codec} is not compatible with MP4, will transcode to AAC',
        'audio_transcode_prompt': '  Audio is {codec}, transcode to AAC? [y/n, default y]: ',
        'audio_aac_transcode_prompt': '  Audio is already AAC, still transcode to AAC? [y/n, default n]: ',
        'will_transcode_audio': '  ✓ Will transcode audio to AAC',
        'will_copy_audio': '  ✓ Will copy audio stream',
        'audio_already_aac': '  ✓ Audio is already AAC, will copy',
        
        # Summary
        'selection_summary': 'Selection summary: {remux} file(s) remux only, {transcode} file(s) re-encode',
        
        # Original file handling
        'original_file_handling': 'Original File Handling',
        'delete_original_prompt': 'Delete original files after successful conversion? [y/n, default n]: ',
        'will_delete_original': '⚠ Will delete original files after successful conversion',
        'will_keep_original': '✓ Will keep original files',
        
        # Start conversion
        'start_conversion_prompt': 'Start converting {count} file(s)? [y/n, default y]: ',
        'cancel_conversion': 'Conversion cancelled',
        
        # Encoding settings
        'encoding_settings': 'Encoding settings (for re-encoding files only):',
        'nvenc_preset_prompt': 'NVENC preset [p1-p7, default p5]: ',
        'quality_prompt': 'Quality parameter [0-51, default 21, lower = higher quality]: ',
        'deinterlace_prompt': 'Enable deinterlacing? [y/n, default n]: ',
        'deinterlace_enabled': '✓ Deinterlacing enabled (yadif)',
        'concurrent_prompt': 'Concurrent files [1-10, default 3]: ',
        'concurrent_warning': 'Note: More than 10 concurrent files may cause resource issues, limited to 10',
        'invalid_input_default': 'Invalid input, using default value 3',
        'will_process_concurrent': '✓ Will process {count} file(s) concurrently',
        
        # Progress
        'total_size': 'Total file size',
        'estimated_time_remux': 'Estimated time: Remux mode only, usually very fast',
        'estimated_time_transcode': 'Estimated time: Depends on video length and complexity, transcoding may take longer',
        'start_batch_conversion': 'Starting batch conversion',
        'start_batch_concurrent': 'Starting batch conversion ({count} files concurrently)',
        'conversion_progress': 'Conversion Progress',
        
        # Results
        'conversion_complete': 'Conversion Complete',
        'success': 'Success',
        'failed': 'Failed',
        'total': 'Total',
        'total_time': 'Total time',
        'size_comparison': 'File Size Comparison:',
        'space_saved': 'Space saved',
        'space_increased': 'Space increased',
        
        # Errors and warnings
        'warning_path_not_exist': 'Warning: Path does not exist - {path}',
        'warning_get_duration': 'Warning: Cannot get video duration - {error}',
        'warning_get_codec': 'Warning: Cannot get video codec - {error}',
        'warning_get_audio_codec': 'Warning: Cannot get audio codec - {error}',
        'error_ffmpeg_not_found': 'Error: FFmpeg not found, please ensure FFmpeg is installed and added to system PATH',
        'error_file': 'Error: {filename} - {error}',
        'warning_delete_failed': 'Warning: Cannot delete original file {filename} - {error}',
        'file_exists_skip': 'File exists, skipping: {filename}',
        'task_exception': 'Task exception: {error}',
        
        # Codec detection
        'detecting_codecs': 'Detecting video codecs...',
        'nvenc_unknown': 'Unknown (GPU model not listed)',
        'nvenc_none': 'No NVIDIA GPU',
        
        # Time formatting
        'time_seconds': '{seconds}s',
        'time_minutes': '{minutes}m {seconds}s',
        'time_hours': '{hours}h {minutes}m',
        'time_unknown': 'Unknown',
        
        # Mode selection
        'mode_selection': 'Mode Selection / 模式选择:',
        'basic_mode': 'Basic Mode (default)',
        'advanced_mode': 'Advanced Mode',
        'press_mode': 'Press 1 or 2 or "Enter": ',
        'mode_basic_selected': '✓ Basic Mode selected',
        'mode_advanced_selected': '✓ Advanced Mode selected',
        
        # Advanced mode options
        'custom_path_prompt': 'Enter custom input path (leave empty for current directory): ',
        'invalid_path': 'Invalid path, using current directory',
        'using_path': 'Using path: {path}',
        'advanced_input_formats': 'Additional input formats in Advanced Mode: .mp4, .mov, .mkv, .webm',
        'output_format_prompt': 'Select output format:',
        'output_format_1': '[1] .mp4 (default)',
        'output_format_2': '[2] .mov',
        'output_format_3': '[3] .mkv',
        'press_output_format': 'Press 1, 2, 3 or "Enter": ',
        'output_format_selected': 'Output format: {format}',
        'encoder_prompt': 'Select video encoder:',
        'encoder_1': '[1] HEVC/H.265 (default)',
        'encoder_2': '[2] AVC/H.264',
        'encoder_3': '[3] AV1',
        'press_encoder': 'Press 1, 2, 3 or "Enter": ',
        'encoder_selected': 'Encoder: {encoder}',
        
        # NVENC detection
        'nvenc_available': '✓ NVENC hardware encoder available',
        'nvenc_not_available': '⚠ NVENC not available, using CPU encoder (slower)',
        'cpu_preset_prompt': 'CPU preset [ultrafast/superfast/veryfast/faster/fast/medium/slow/slower/veryslow, default medium]: ',
        'using_nvenc': 'Using NVENC hardware encoder',
        'using_cpu_encoder': 'Using CPU software encoder',
    },
    'zh': {
        # Main interface
        'title': '通用视频转 H.265 MP4 批量转换工具',
        'supported_formats': '支持的格式:',
        'remux_recommended': '建议只转容器',
        'transcode_recommended': '建议转码+转容器',
        'current_path': '当前路径',
        'searching_files': '正在搜索视频文件...',
        'no_files_found': '未找到任何支持的视频文件',
        'supported_formats_list': '支持的格式',
        'press_enter_exit': '按回车键退出...',
        'found_files': '找到 {count} 个视频文件:',
        'files_count': '{count} 个',
        
        # Existing files
        'existing_files_found': '发现 {count} 个已存在的MP4文件',
        'overwrite_prompt': '是否覆盖已存在的文件? [y/n, 默认n]: ',
        'will_overwrite': '✓ 将覆盖已存在的文件',
        'will_skip': '✓ 将跳过已存在的文件',
        
        # Conversion mode
        'select_mode': '选择转换模式',
        'batch_mode_prompt': '是否对同格式的所有文件应用相同设置? [y/n, 默认n]: ',
        'batch_mode_enabled': '✓ 批量模式: 将为每种格式统一设置',
        'format_info': '格式 {ext} ({count} 个文件):',
        'remux_only_recommended': '  建议只转容器',
        'transcode_recommended_msg': '  建议转码+转容器',
        'remux_prompt_y': '  是否只转换容器至.mp4? [y/n, 默认y]: ',
        'remux_prompt_n': '  是否只转换容器至.mp4? [y/n, 默认n]: ',
        'transcode_audio_prompt': '  是否将非AAC音频转码为AAC? [y/n, 默认y]: ',
        'mode_remux_only': '只转容器',
        'mode_transcode_h265': '转码为H.265',
        'audio_transcode_aac': '转AAC',
        'audio_copy': '复制音频',
        
        # File by file
        'video_codec': '视频编码',
        'audio_codec': '音频编码',
        'format_remux_recommended': '格式 {ext} 建议只转容器',
        'format_transcode_recommended': '格式 {ext} 建议转码+转容器',
        'remux_prompt_detail': '  是否只转换容器至.mp4而不重新编码? (速度更快,无质量损失) [y/n, 默认{default}]: ',
        'will_remux': '  ✓ 将只转换容器 (remux)',
        'will_transcode': '  ✓ 将重新编码为H.265',
        'audio_incompatible': '  ⚠ 音频 {codec} 不兼容MP4容器，将自动转码为AAC',
        'audio_transcode_prompt': '  音频为{codec}，是否转码为AAC? [y/n, 默认y]: ',
        'audio_aac_transcode_prompt': '  原音频为AAC，是否转码为AAC? [y/n, 默认n]: ',
        'will_transcode_audio': '  ✓ 将音频转码为AAC',
        'will_copy_audio': '  ✓ 将直接复制音频流',
        'audio_already_aac': '  ✓ 音频已为AAC，将直接复制',
        
        # Summary
        'selection_summary': '选择汇总: {remux} 个文件只转容器, {transcode} 个文件重新编码',
        
        # Original file handling
        'original_file_handling': '原始文件处理',
        'delete_original_prompt': '转换成功后是否删除原始文件? [y/n, 默认n]: ',
        'will_delete_original': '⚠ 转换成功后将删除原始文件',
        'will_keep_original': '✓ 将保留原始文件',
        
        # Start conversion
        'start_conversion_prompt': '是否开始转换这 {count} 个文件? [y/n, 默认y]: ',
        'cancel_conversion': '取消转换',
        
        # Encoding settings
        'encoding_settings': '转换设置 (仅用于重新编码的文件):',
        'nvenc_preset_prompt': 'NVENC预设 [p1-p7, 默认p5]: ',
        'quality_prompt': '质量参数 [0-51, 默认21, 越小质量越高]: ',
        'deinterlace_prompt': '是否去隔行扫描? [y/n, 默认n]: ',
        'deinterlace_enabled': '✓ 已启用去隔行扫描 (yadif)',
        'concurrent_prompt': '同时处理文件数 [1-10, 默认3]: ',
        'concurrent_warning': '注意: 并发数超过10可能会导致系统资源不足，已限制为10',
        'invalid_input_default': '输入无效，使用默认值3',
        'will_process_concurrent': '✓ 将同时处理 {count} 个文件',
        
        # Progress
        'total_size': '总文件大小',
        'estimated_time_remux': '预估时间: 仅remux模式，通常非常快速',
        'estimated_time_transcode': '预估时间: 取决于视频长度和复杂度，转码可能需要较长时间',
        'start_batch_conversion': '开始批量转换',
        'start_batch_concurrent': '开始批量转换（同时处理 {count} 个文件）',
        'conversion_progress': '转换进度',
        
        # Results
        'conversion_complete': '转换完成',
        'success': '成功',
        'failed': '失败',
        'total': '总计',
        'total_time': '总耗时',
        'size_comparison': '文件大小对比:',
        'space_saved': '节省空间',
        'space_increased': '增加空间',
        
        # Errors and warnings
        'warning_path_not_exist': '警告: 路径不存在 - {path}',
        'warning_get_duration': '警告: 无法获取视频时长 - {error}',
        'warning_get_codec': '警告: 无法获取视频编码 - {error}',
        'warning_get_audio_codec': '警告: 无法获取音频编码 - {error}',
        'error_ffmpeg_not_found': '错误: 找不到FFmpeg，请确保FFmpeg已安装并添加到系统PATH',
        'error_file': '错误: {filename} - {error}',
        'warning_delete_failed': '警告: 无法删除原始文件 {filename} - {error}',
        'file_exists_skip': '文件已存在，跳过: {filename}',
        'task_exception': '任务异常: {error}',
        
        # Codec detection
        'detecting_codecs': '正在检测视频编码格式...',
        'nvenc_unknown': '未知 (GPU型号未收录)',
        'nvenc_none': '无NVIDIA GPU',
        
        # Time formatting
        'time_seconds': '{seconds}秒',
        'time_minutes': '{minutes}分{seconds}秒',
        'time_hours': '{hours}时{minutes}分',
        'time_unknown': '未知',
        
        # Mode selection
        'mode_selection': 'Mode Selection / 模式选择:',
        'basic_mode': '基础模式 (默认)',
        'advanced_mode': '高级模式',
        'press_mode': '按 1 或 2 或 "Enter": ',
        'mode_basic_selected': '✓ 已选择基础模式',
        'mode_advanced_selected': '✓ 已选择高级模式',
        
        # Advanced mode options
        'custom_path_prompt': '输入自定义输入路径 (留空使用当前目录): ',
        'invalid_path': '路径无效，使用当前目录',
        'using_path': '使用路径: {path}',
        'advanced_input_formats': '高级模式额外支持的输入格式: .mp4, .mov, .mkv, .webm',
        'output_format_prompt': '选择输出格式:',
        'output_format_1': '[1] .mp4 (默认)',
        'output_format_2': '[2] .mov',
        'output_format_3': '[3] .mkv',
        'press_output_format': '按 1, 2, 3 或 "Enter": ',
        'output_format_selected': '输出格式: {format}',
        'encoder_prompt': '选择视频编码器:',
        'encoder_1': '[1] HEVC/H.265 (默认)',
        'encoder_2': '[2] AVC/H.264',
        'encoder_3': '[3] AV1',
        'press_encoder': '按 1, 2, 3 或 "Enter": ',
        'encoder_selected': '编码器: {encoder}',
        
        # NVENC detection
        'nvenc_available': '✓ NVENC硬件编码器可用',
        'nvenc_not_available': '⚠ NVENC不可用，将使用CPU编码器（速度较慢）',
        'cpu_preset_prompt': 'CPU预设 [ultrafast/superfast/veryfast/faster/fast/medium/slow/slower/veryslow, 默认medium]: ',
        'using_nvenc': '使用NVENC硬件编码器',
        'using_cpu_encoder': '使用CPU软件编码器',
    }
}

# 全局语言变量
current_lang = 'en'

# 全局变量：是否使用NVENC硬件编码
use_nvenc = True

def t(key, **kwargs):
    """获取翻译文本"""
    text = LANG.get(current_lang, LANG['en']).get(key, key)
    if kwargs:
        return text.format(**kwargs)
    return text

def check_nvenc_available():
    """检测NVENC是否可用"""
    try:
        result = subprocess.run(
            ['ffmpeg', '-hide_banner', '-encoders'],
            capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=10,
            creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
        )
        # 检查是否有hevc_nvenc编码器
        return 'hevc_nvenc' in result.stdout
    except:
        return False

# ================================
# 炫酷开屏动画
# ================================

# 预定义的ASCII艺术标题 (更炫酷的3D风格)
BANNER_VIDEO = [
    "██╗   ██╗██╗██████╗ ███████╗ ██████╗ ",
    "██║   ██║██║██╔══██╗██╔════╝██╔═══██╗",
    "██║   ██║██║██║  ██║█████╗  ██║   ██║",
    "╚██╗ ██╔╝██║██║  ██║██╔══╝  ██║   ██║",
    " ╚████╔╝ ██║██████╔╝███████╗╚██████╔╝",
    "  ╚═══╝  ╚═╝╚═════╝ ╚══════╝ ╚═════╝ ",
]

BANNER_CONVERTER = [
    " ██████╗ ██████╗ ███╗   ██╗██╗   ██╗███████╗██████╗ ████████╗███████╗██████╗ ",
    "██╔════╝██╔═══██╗████╗  ██║██║   ██║██╔════╝██╔══██╗╚══██╔══╝██╔════╝██╔══██╗",
    "██║     ██║   ██║██╔██╗ ██║██║   ██║█████╗  ██████╔╝   ██║   █████╗  ██████╔╝",
    "██║     ██║   ██║██║╚██╗██║╚██╗ ██╔╝██╔══╝  ██╔══██╗   ██║   ██╔══╝  ██╔══██╗",
    "╚██████╗╚██████╔╝██║ ╚████║ ╚████╔╝ ███████╗██║  ██║   ██║   ███████╗██║  ██║",
    " ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝",
]

def get_system_info():
    """获取系统硬件信息"""
    info = {
        'cpu': None,
        'gpu': None,
        'nvenc_count': 0,
        'nvdec_count': 0,
        'ram': None
    }
    
    # 获取CPU信息 (PowerShell)
    try:
        result = subprocess.run(
            ['powershell', '-Command', '(Get-WmiObject Win32_Processor).Name'],
            capture_output=True, text=True, encoding='utf-8', errors='ignore', 
            timeout=5, creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
        )
        if result.stdout.strip():
            cpu_name = result.stdout.strip()
            # 简化CPU名称
            cpu_name = cpu_name.replace('(R)', '').replace('(TM)', '').replace('CPU ', '')
            cpu_name = re.sub(r'\s+', ' ', cpu_name).strip()
            if cpu_name and 'error' not in cpu_name.lower():
                info['cpu'] = cpu_name
    except:
        pass
    
    # 获取GPU信息 (PowerShell)
    try:
        result = subprocess.run(
            ['powershell', '-Command', '(Get-WmiObject Win32_VideoController).Name'],
            capture_output=True, text=True, encoding='utf-8', errors='ignore',
            timeout=5, creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
        )
        if result.stdout.strip():
            lines = [l.strip() for l in result.stdout.strip().split('\n') if l.strip()]
            if lines:
                # 优先选择NVIDIA GPU
                nvidia_gpus = [g for g in lines if 'NVIDIA' in g.upper()]
                if nvidia_gpus:
                    info['gpu'] = nvidia_gpus[0]
                else:
                    info['gpu'] = lines[0]
    except:
        pass
    
    # 根据GPU型号获取物理NVENC/NVDEC单元数量
    gpu_name = (info['gpu'] or '').upper()
    nvenc_count = 0
    nvdec_count = 0
    nvenc_status = 'none'  # 'none', 'unknown', 'detected'
    
    # NVIDIA GPU 物理编解码器数量表 (基于官方规格)
    # RTX 50系列 (Blackwell)
    if any(x in gpu_name for x in ['RTX 5090', 'RTX 5080']):
        nvenc_count, nvdec_count = 3, 2
        nvenc_status = 'detected'
    elif 'RTX 50' in gpu_name:
        nvenc_count, nvdec_count = 2, 2
        nvenc_status = 'detected'
    # RTX 40系列 (Ada Lovelace)
    elif any(x in gpu_name for x in ['RTX 4090', 'RTX 4080']):
        nvenc_count, nvdec_count = 2, 2
        nvenc_status = 'detected'
    elif 'RTX 40' in gpu_name:
        nvenc_count, nvdec_count = 1, 2
        nvenc_status = 'detected'
    # RTX 30系列 (Ampere)
    elif any(x in gpu_name for x in ['RTX 3090', 'RTX 3080', 'RTX 3070']):
        nvenc_count, nvdec_count = 1, 1
        nvenc_status = 'detected'
    elif 'RTX 30' in gpu_name:
        nvenc_count, nvdec_count = 1, 1
        nvenc_status = 'detected'
    # RTX 20系列 (Turing)
    elif 'RTX 20' in gpu_name:
        nvenc_count, nvdec_count = 1, 1
        nvenc_status = 'detected'
    # GTX 16系列 (Turing)
    elif 'GTX 16' in gpu_name:
        nvenc_count, nvdec_count = 1, 1
        nvenc_status = 'detected'
    # GTX 10系列 (Pascal)
    elif 'GTX 10' in gpu_name:
        nvenc_count, nvdec_count = 1, 1
        nvenc_status = 'detected'
    # Quadro/专业卡
    elif 'A6000' in gpu_name or 'A5000' in gpu_name:
        nvenc_count, nvdec_count = 1, 1
        nvenc_status = 'detected'
    elif 'A4000' in gpu_name:
        nvenc_count, nvdec_count = 1, 1
        nvenc_status = 'detected'
    elif 'QUADRO' in gpu_name:
        nvenc_count, nvdec_count = 1, 1
        nvenc_status = 'detected'
    # 检测是否有NVIDIA GPU但未匹配到具体型号
    elif 'NVIDIA' in gpu_name or 'GEFORCE' in gpu_name:
        nvenc_status = 'unknown'
    # 没有NVIDIA GPU
    else:
        nvenc_status = 'none'
    
    info['nvenc_count'] = nvenc_count
    info['nvdec_count'] = nvdec_count
    info['nvenc_status'] = nvenc_status
    
    # 获取RAM信息 (PowerShell)
    try:
        result = subprocess.run(
            ['powershell', '-Command', '[math]::Round((Get-WmiObject Win32_ComputerSystem).TotalPhysicalMemory / 1GB)'],
            capture_output=True, text=True, encoding='utf-8', errors='ignore',
            timeout=5, creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
        )
        if result.stdout.strip():
            ram_gb = result.stdout.strip()
            if ram_gb.isdigit():
                info['ram'] = f"{ram_gb} GB"
    except:
        pass
    
    return info

def show_splash_animation():
    """显示炫酷的开屏动画"""
    import threading
    
    # 在后台线程获取系统信息，这样动画期间就在检测
    sys_info_result = [None]
    def fetch_sys_info():
        sys_info_result[0] = get_system_info()
    
    info_thread = threading.Thread(target=fetch_sys_info)
    info_thread.start()
    
    # 清屏
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # 计算最大宽度
    max_width = max(len(line) for line in BANNER_CONVERTER)
    box_width = max_width + 4
    
    # 渐显动画
    reveal_stages = [
        ('░', '░'),
        ('▒', '░'),
        ('▓', '▒'),
        ('█', '▓'),
        ('█', '█'),
    ]
    
    for stage_v, stage_c in reveal_stages:
        sys.stdout.write('\033[H')
        print("\n")
        
        # 边框顶部
        print("  ╔" + "═" * box_width + "╗")
        print("  ║" + " " * box_width + "║")
        
        # VIDEO - 居中显示
        for line in BANNER_VIDEO:
            displayed_line = line.replace('█', stage_v).replace('╔', stage_v).replace('╗', stage_v).replace('║', stage_v).replace('╚', stage_v).replace('╝', stage_v).replace('═', stage_v)
            padding_left = (box_width - len(line)) // 2
            padding_right = box_width - len(line) - padding_left
            print(f"  ║{' ' * padding_left}{displayed_line}{' ' * padding_right}║")
        
        print("  ║" + " " * box_width + "║")
        
        # CONVERTER - 居中显示
        for line in BANNER_CONVERTER:
            displayed_line = line.replace('█', stage_c).replace('╔', stage_c).replace('╗', stage_c).replace('║', stage_c).replace('╚', stage_c).replace('╝', stage_c).replace('═', stage_c)
            padding_left = (box_width - len(line)) // 2
            padding_right = box_width - len(line) - padding_left
            print(f"  ║{' ' * padding_left}{displayed_line}{' ' * padding_right}║")
        
        print("  ║" + " " * box_width + "║")
        print("  ╚" + "═" * box_width + "╝")
        
        time.sleep(0.05)

    
    # 等待系统信息获取完成
    info_thread.join()
    sys_info = sys_info_result[0]
    
    # 最终显示版本信息和Credit
    sys.stdout.write('\033[H')
    print("\n")
    
    print("  ╔" + "═" * box_width + "╗")
    print("  ║" + " " * box_width + "║")
    
    for line in BANNER_VIDEO:
        padding_left = (box_width - len(line)) // 2
        padding_right = box_width - len(line) - padding_left
        print(f"  ║{' ' * padding_left}{line}{' ' * padding_right}║")
    
    print("  ║" + " " * box_width + "║")
    
    for line in BANNER_CONVERTER:
        padding_left = (box_width - len(line)) // 2
        padding_right = box_width - len(line) - padding_left
        print(f"  ║{' ' * padding_left}{line}{' ' * padding_right}║")
    
    print("  ║" + " " * box_width + "║")
    print("  ╠" + "═" * box_width + "╣")
    
    # 显示系统信息
    def print_info_line(label, value):
        line = f"◆ {label}: {value}"
        if len(line) > box_width - 2:
            line = line[:box_width - 5] + "..."
        padding_left = (box_width - len(line)) // 2
        padding_right = box_width - len(line) - padding_left
        print(f"  ║{' ' * padding_left}{line}{' ' * padding_right}║")
    
    # 只显示成功检测到的信息
    if sys_info['cpu']:
        print_info_line("CPU", sys_info['cpu'])
    if sys_info['gpu']:
        print_info_line("GPU", sys_info['gpu'])
    if sys_info['nvenc_status'] == 'detected':
        print_info_line("NVENC/NVDEC", f"{sys_info['nvenc_count']} encoder(s), {sys_info['nvdec_count']} decoder(s)")
    elif sys_info['nvenc_status'] == 'unknown':
        print_info_line("NVENC/NVDEC", "未知 (GPU型号未收录)")
    else:
        print_info_line("NVENC/NVDEC", "无NVIDIA GPU")
    if sys_info['ram']:
        print_info_line("RAM", sys_info['ram'])
    
    print("  ║" + " " * box_width + "║")
    
    # Credit 闪烁效果
    credit_line = "✧ Created by: Jack Ji    GPL-3.0 license ✧"
    
    for _ in range(3):
        sys.stdout.write('\033[F')  # 上移一行
        padding_left = (box_width - len(credit_line)) // 2
        padding_right = box_width - len(credit_line) - padding_left
        print(f"  ║{' ' * padding_left}{credit_line}{' ' * padding_right}║")
        sys.stdout.flush()
        time.sleep(0.15)
        sys.stdout.write('\033[F')
        print(f"  ║{' ' * box_width}║")
        sys.stdout.flush()
        time.sleep(0.1)
    
    # 最终显示Credit
    sys.stdout.write('\033[F')
    padding_left = (box_width - len(credit_line)) // 2
    padding_right = box_width - len(credit_line) - padding_left
    print(f"  ║{' ' * padding_left}{credit_line}{' ' * padding_right}║")
    
    print("  ║" + " " * box_width + "║")
    print("  ╚" + "═" * box_width + "╝")
    
    # 语言选择 - 单键检测
    print()
    print("  Language:")
    print("  [1] English (default)")
    print("  [2] 中文")
    print("  Press 1 or 2 or \"Enter\": ", end='', flush=True)
    
    # 使用 msvcrt 实现单键检测 (Windows)
    import msvcrt
    while True:
        key = msvcrt.getch()
        # 处理按键
        if key == b'2':
            print('2')  # 显示按下的键
            selected_lang = 'zh'
            break
        elif key == b'1' or key == b'\r' or key == b'\n':  # 1 或 Enter
            print('1' if key == b'1' else '')  # 显示按下的键
            selected_lang = 'en'
            break
    
    # 模式选择 - 单键检测 (根据已选语言显示)
    print()
    if selected_lang == 'zh':
        print("  模式选择:")
        print("  [1] 基础模式 (默认)")
        print("  [2] 高级模式")
        print("  按 1 或 2 或 \"Enter\": ", end='', flush=True)
    else:
        print("  Mode Selection:")
        print("  [1] Basic Mode (default)")
        print("  [2] Advanced Mode")
        print("  Press 1 or 2 or \"Enter\": ", end='', flush=True)
    
    while True:
        key = msvcrt.getch()
        # 处理按键
        if key == b'2':
            print('2')  # 显示按下的键
            selected_mode = 'advanced'
            break
        elif key == b'1' or key == b'\r' or key == b'\n':  # 1 或 Enter
            print('1' if key == b'1' else '')  # 显示按下的键
            selected_mode = 'basic'
            break
    
    return selected_lang, selected_mode


# 用于线程安全的打印
print_lock = Lock()
# 存储每个文件的进度
progress_dict = OrderedDict()
# 存储转换结果（用于显示文件大小对比）
conversion_results = OrderedDict()

# 支持的视频格式分类
# 建议只转容器的格式（通常已是H.264/H.265编码）
REMUX_RECOMMENDED_FORMATS = ['.mts', '.m2ts', '.m2t', '.ts', '.m4v']
# 建议转码+转容器的格式（通常是老格式或非标准编码）
TRANSCODE_RECOMMENDED_FORMATS = ['.vob', '.mpg', '.mpeg', '.avi', '.wmv', '.flv', '.f4v', '.3gp', '.webm', '.rmvb', '.rm']
# 所有支持的格式
ALL_SUPPORTED_FORMATS = REMUX_RECOMMENDED_FORMATS + TRANSCODE_RECOMMENDED_FORMATS

def get_file_size(file_path):
    """获取文件大小（字节）"""
    try:
        return Path(file_path).stat().st_size
    except:
        return 0

def format_size(size_bytes):
    """将字节转换为人类可读的格式"""
    if size_bytes == 0:
        return "0 B"
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    unit_index = 0
    size = float(size_bytes)
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    return f"{size:.2f} {units[unit_index]}"

def format_time(seconds):
    """将秒数转换为人类可读的时间格式"""
    if seconds is None or seconds <= 0:
        return t('time_unknown')
    if seconds < 60:
        return t('time_seconds', seconds=int(seconds))
    elif seconds < 3600:
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return t('time_minutes', minutes=mins, seconds=secs)
    else:
        hours = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        return t('time_hours', hours=hours, minutes=mins)


def find_video_files(root_paths, supported_formats=None):
    """递归查找所有支持的视频文件"""
    if supported_formats is None:
        supported_formats = ALL_SUPPORTED_FORMATS
    video_files = []
    for root_path in root_paths:
        root = Path(root_path)
        if not root.exists():
            print(f"警告: 路径不存在 - {root_path}")
            continue
        
        # 搜索所有支持的格式（大小写不敏感）
        for video_file in root.rglob("*"):
            if video_file.suffix.lower() in supported_formats:
                video_files.append(video_file)
    
    return video_files

def get_video_duration(input_file):
    """获取视频时长（秒）"""
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        str(input_file)
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=10)
        if result.stdout.strip():
            duration = float(result.stdout.strip())
            return duration
        return None
    except Exception as e:
        print(f"警告: 无法获取视频时长 - {e}")
        return None

def get_video_codec(input_file):
    """获取视频编码格式"""
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=codec_name',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        str(input_file)
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=10)
        if result.stdout.strip():
            # 只取第一行，移除所有空白字符
            lines = result.stdout.strip().split('\n')
            codec = lines[0].strip().replace('\r', '').lower()
            return codec
        return None
    except Exception as e:
        print(f"警告: 无法获取视频编码 - {e}")
        return None

def get_audio_codec(input_file):
    """获取音频编码格式"""
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'a:0',
        '-show_entries', 'stream=codec_name',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        str(input_file)
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=10)
        if result.stdout.strip():
            # 只取第一行，移除所有空白字符
            lines = result.stdout.strip().split('\n')
            codec = lines[0].strip().replace('\r', '').lower()
            return codec
        return None
    except Exception as e:
        print(f"警告: 无法获取音频编码 - {e}")
        return None

def check_all_files_codec(mts_files):
    """检查所有文件的编码格式，返回是否全部为H.264或H.265"""
    h264_h265_codecs = ['h264', 'avc', 'h265', 'hevc']
    all_compatible = True
    codec_info = []
    
    print("\n正在检测视频编码格式...")
    for f in mts_files:
        codec = get_video_codec(f)
        codec_info.append((f, codec))
        if codec not in h264_h265_codecs:
            all_compatible = False
    
    return all_compatible, codec_info

def parse_ffmpeg_progress(line, duration):
    """从FFmpeg输出解析进度"""
    if not duration or duration <= 0:
        # 如果没有时长信息，尝试从帧数估算
        frame_match = re.search(r'frame=\s*(\d+)', line)
        if frame_match:
            # 假设30fps，粗略估算（不准确但至少有反馈）
            return min(99, int(frame_match.group(1)) / 100)
        return None
    
    # 匹配time=00:01:23.45格式
    time_match = re.search(r'time=(\d+):(\d+):(\d+\.\d+)', line)
    if time_match:
        hours = int(time_match.group(1))
        minutes = int(time_match.group(2))
        seconds = float(time_match.group(3))
        current_time = hours * 3600 + minutes * 60 + seconds
        progress = min(100, (current_time / duration) * 100)
        return progress
    return None

def update_progress_display():
    """更新所有进度条的显示"""
    try:
        with print_lock:
            # 使用\r回到行首，清空屏幕后重新打印所有进度
            sys.stdout.write('\033[2J\033[H')  # 清屏并移到左上角
            sys.stdout.write("=" * 60 + "\n")
            sys.stdout.write(t('conversion_progress') + "\n")
            sys.stdout.write("=" * 60 + "\n")
            
            # 显示所有进度
            for key, info in progress_dict.items():
                index, total, name, progress, status = info
                bar_length = 30
                filled = int(bar_length * progress / 100)
                bar = '█' * filled + '░' * (bar_length - filled)
                status_symbol = '✓' if status == 'done' else '✗' if status == 'failed' else ''
                # 截断文件名避免换行
                display_name = name if len(name) <= 30 else name[:27] + "..."
                sys.stdout.write(f"[{index}/{total}] {display_name}: [{bar}] {progress:.1f}% {status_symbol}\n")
            
            sys.stdout.flush()
    except Exception as e:
        pass  # 忽略显示错误

# 需要转码音频的格式（.ts/.m2ts/.mts 且音频为PCM或TrueHD时）
TS_FORMATS = ['.ts', '.m2ts', '.mts', '.m2t']
# 需要转码为AAC的音频编码
AUDIO_NEEDS_TRANSCODE = ['pcm_s16le', 'pcm_s24le', 'pcm_s32le', 'pcm_s16be', 'pcm_s24be', 'pcm_s32be', 
                          'pcm_f32le', 'pcm_f64le', 'pcm_bluray', 'pcm_dvd',
                          'truehd', 'mlp']  # Dolby TrueHD 的编码名称

def remux_to_mp4(input_file, index=0, total=0, overwrite=False, transcode_audio=False, keep_original=True, delete_on_success=False, output_format='.mp4'):
    """
    只转换容器而不重新编码（remux）
    
    参数:
    - input_file: 输入文件路径
    - index: 当前文件索引
    - total: 总文件数
    - overwrite: 是否覆盖已存在文件
    - transcode_audio: 是否将音频转码为AAC
    - keep_original: 是否保留原始文件（转换成功后）
    - delete_on_success: 转换成功后是否删除原始文件
    - output_format: 输出文件格式 (默认.mp4)
    """
    input_path = Path(input_file)
    file_ext = input_path.suffix.lower()
    # 如果源文件和目标文件扩展名相同，添加后缀避免覆盖
    if file_ext == output_format:
        output_path = input_path.with_stem(input_path.stem + '_converted').with_suffix(output_format)
    else:
        output_path = input_path.with_suffix(output_format)
    file_key = str(input_path)
    start_time = time.time()
    
    # 获取原始文件大小
    original_size = get_file_size(input_path)
    
    # 如果输出文件已存在且不覆盖，跳过
    if output_path.exists() and not overwrite:
        with print_lock:
            print(f"[{index}/{total}] 文件已存在，跳过: {output_path.name}")
        return False, None
    
    # 初始化进度
    progress_dict[file_key] = (index, total, input_path.name, 0.0, 'processing')
    update_progress_display()
    
    # 获取视频时长用于计算进度
    duration = get_video_duration(input_path)
    
    # 检测音频编码，判断是否需要强制转码音频（PCM/TrueHD不兼容MP4）
    audio_codec = get_audio_codec(input_path)
    need_audio_transcode = transcode_audio  # 使用用户选择
    
    # 对于TS格式，PCM和TrueHD必须转码（不兼容MP4容器）
    if file_ext in TS_FORMATS and audio_codec:
        if audio_codec in AUDIO_NEEDS_TRANSCODE or audio_codec.startswith('pcm'):
            need_audio_transcode = True
    
    # FFmpeg命令 - 只复制流，不重新编码
    cmd = ['ffmpeg']
    
    if overwrite or not output_path.exists():
        cmd.append('-y')
    
    cmd.extend([
        '-i', str(input_path),
        '-progress', 'pipe:2',
        '-map', '0',              # 映射所有流（视频、音频、字幕）
        '-c:v', 'copy',           # 视频流直接复制
    ])
    
    # 根据音频编码决定是否转码
    if need_audio_transcode:
        cmd.extend([
            '-c:a', 'aac',        # 音频编码为AAC
            '-b:a', '192k',
        ])
    else:
        cmd.extend([
            '-c:a', 'copy',       # 音频流直接复制
        ])
    
    # 字幕处理（MP4兼容的字幕格式）
    cmd.extend([
        '-c:s', 'mov_text',       # 字幕转换为MP4兼容格式
        '-movflags', '+faststart',
        str(output_path)
    ])
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        last_progress = 0
        line_count = 0
        while True:
            line = process.stderr.readline()
            if not line and process.poll() is not None:
                break
            if not line:
                continue
            
            line_count += 1
            progress = parse_ffmpeg_progress(line, duration)
            if progress is not None and (progress - last_progress >= 3 or line_count % 100 == 0):
                progress_dict[file_key] = (index, total, input_path.name, progress, 'processing')
                update_progress_display()
                last_progress = progress
        
        process.wait()
        elapsed_time = time.time() - start_time
        
        if process.returncode == 0:
            output_size = get_file_size(output_path)
            progress_dict[file_key] = (index, total, input_path.name, 100.0, 'done')
            update_progress_display()
            
            # 存储转换结果
            conversion_results[file_key] = {
                'input': input_path.name,
                'output': output_path.name,
                'original_size': original_size,
                'output_size': output_size,
                'elapsed_time': elapsed_time,
                'success': True
            }
            
            # 处理原始文件
            if delete_on_success:
                try:
                    input_path.unlink()
                except Exception as e:
                    with print_lock:
                        print(f"\n警告: 无法删除原始文件 {input_path.name} - {e}")
            
            return True, conversion_results[file_key]
        else:
            progress_dict[file_key] = (index, total, input_path.name, last_progress, 'failed')
            update_progress_display()
            
            # 错误恢复：删除不完整的输出文件
            if output_path.exists():
                try:
                    output_path.unlink()
                except:
                    pass
            
            return False, None
            
    except FileNotFoundError:
        print("\n错误: 找不到FFmpeg，请确保FFmpeg已安装并添加到系统PATH")
        # 删除可能的不完整文件
        if output_path.exists():
            try:
                output_path.unlink()
            except:
                pass
        return False, None
    except Exception as e:
        progress_dict[file_key] = (index, total, input_path.name, 0.0, 'failed')
        update_progress_display()
        with print_lock:
            print(f"\n错误: {input_path.name} - {str(e)}")
        # 删除可能的不完整文件
        if output_path.exists():
            try:
                output_path.unlink()
            except:
                pass
        return False, None


def convert_to_h265(input_file, preset="p5", crf=23, deinterlace=False, index=0, total=0, overwrite=False, delete_on_success=False, output_format='.mp4', encoder='hevc'):
    """
    使用FFmpeg和NVENC转换视频
    
    参数:
    - input_file: 输入文件路径
    - preset: NVENC预设 (p1-p7, p5为默认)
    - crf: 质量参数 (0-51, 23为默认, 数值越小质量越高)
    - deinterlace: 是否去隔行扫描
    - index: 当前文件索引
    - total: 总文件数
    - overwrite: 是否覆盖已存在文件
    - delete_on_success: 转换成功后是否删除原始文件
    - output_format: 输出文件格式 (默认.mp4)
    - encoder: 视频编码器 ('hevc', 'h264', 'av1', 默认hevc)
    """
    input_path = Path(input_file)
    file_ext = input_path.suffix.lower()
    # 如果源文件和目标文件扩展名相同，添加后缀避免覆盖
    if file_ext == output_format:
        # 根据编码器添加更有意义的后缀
        encoder_suffix = {'hevc': '_h265', 'h264': '_h264', 'av1': '_av1'}.get(encoder, '_converted')
        output_path = input_path.with_stem(input_path.stem + encoder_suffix).with_suffix(output_format)
    else:
        output_path = input_path.with_suffix(output_format)
    file_key = str(input_path)
    start_time = time.time()
    
    # 获取原始文件大小
    original_size = get_file_size(input_path)
    
    # 如果输出文件已存在且不覆盖，跳过
    if output_path.exists() and not overwrite:
        with print_lock:
            print(f"[{index}/{total}] 文件已存在，跳过: {output_path.name}")
        return False, None
    
    # 初始化进度
    progress_dict[file_key] = (index, total, input_path.name, 0.0, 'processing')
    update_progress_display()
    
    # 获取视频时长用于计算进度
    duration = get_video_duration(input_path)
    
    # 根据encoder和use_nvenc选择编码器
    global use_nvenc
    if use_nvenc:
        encoder_map = {
            'hevc': 'hevc_nvenc',
            'h264': 'h264_nvenc',
            'av1': 'av1_nvenc'
        }
        video_codec = encoder_map.get(encoder, 'hevc_nvenc')
    else:
        encoder_map = {
            'hevc': 'libx265',
            'h264': 'libx264',
            'av1': 'libaom-av1'
        }
        video_codec = encoder_map.get(encoder, 'libx265')
    
    # 根据输出格式选择字幕编码
    subtitle_codec_map = {
        '.mp4': 'mov_text',
        '.mov': 'mov_text',
        '.mkv': 'srt'  # MKV更适合使用SRT或保留原字幕
    }
    subtitle_codec = subtitle_codec_map.get(output_format, 'mov_text')
    
    # FFmpeg命令
    cmd = [
        'ffmpeg'
    ]
    
    # 如果需要覆盖，添加-y参数
    if overwrite or not output_path.exists():
        cmd.append('-y')
    
    cmd.extend([
        '-i', str(input_path),
        '-progress', 'pipe:2',  # 输出进度到stderr
        '-map', '0',            # 映射所有流
    ])
    
    # 如果启用去隔行扫描，添加视频滤镜
    if deinterlace:
        cmd.extend(['-vf', 'yadif=1'])  # yadif=1: 输出一帧对应一帧
    
    # 视频编码器和参数
    cmd.extend(['-c:v', video_codec])
    
    if use_nvenc:
        # NVENC硬件编码器参数
        cmd.extend([
            '-preset', preset,      # NVENC预设 (p1-p7)
            '-cq', str(crf),        # 恒定质量模式
        ])
    else:
        # CPU软件编码器参数
        cmd.extend([
            '-preset', preset,      # CPU预设 (ultrafast/medium/slow等)
            '-crf', str(crf),       # 恒定质量因子
        ])
    
    # 音频和字幕参数
    cmd.extend([
        '-c:a', 'aac',          # 音频编码为AAC
        '-b:a', '192k',         # 音频比特率
        '-c:s', subtitle_codec, # 字幕格式
    ])
    
    # MP4和MOV需要faststart优化
    if output_format in ['.mp4', '.mov']:
        cmd.extend(['-movflags', '+faststart'])
    
    cmd.append(str(output_path))
    
    try:
        # 使用Popen实时读取输出
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        last_progress = 0
        line_count = 0
        while True:
            line = process.stderr.readline()
            if not line and process.poll() is not None:
                break
            if not line:
                continue
            
            line_count += 1
            
            # 解析进度
            progress = parse_ffmpeg_progress(line, duration)
            if progress is not None and (progress - last_progress >= 3 or line_count % 100 == 0):
                progress_dict[file_key] = (index, total, input_path.name, progress, 'processing')
                update_progress_display()
                last_progress = progress
        
        process.wait()
        elapsed_time = time.time() - start_time
        
        if process.returncode == 0:
            output_size = get_file_size(output_path)
            progress_dict[file_key] = (index, total, input_path.name, 100.0, 'done')
            update_progress_display()
            
            # 存储转换结果
            conversion_results[file_key] = {
                'input': input_path.name,
                'output': output_path.name,
                'original_size': original_size,
                'output_size': output_size,
                'elapsed_time': elapsed_time,
                'success': True
            }
            
            # 处理原始文件
            if delete_on_success:
                try:
                    input_path.unlink()
                except Exception as e:
                    with print_lock:
                        print(f"\n警告: 无法删除原始文件 {input_path.name} - {e}")
            
            return True, conversion_results[file_key]
        else:
            progress_dict[file_key] = (index, total, input_path.name, last_progress, 'failed')
            update_progress_display()
            
            # 错误恢复：删除不完整的输出文件
            if output_path.exists():
                try:
                    output_path.unlink()
                except:
                    pass
            
            return False, None
            
    except FileNotFoundError:
        print("\n错误: 找不到FFmpeg，请确保FFmpeg已安装并添加到系统PATH")
        # 删除可能的不完整文件
        if output_path.exists():
            try:
                output_path.unlink()
            except:
                pass
        return False, None
    except Exception as e:
        progress_dict[file_key] = (index, total, input_path.name, 0.0, 'failed')
        update_progress_display()
        with print_lock:
            print(f"\n错误: {input_path.name} - {str(e)}")
        # 删除可能的不完整文件
        if output_path.exists():
            try:
                output_path.unlink()
            except:
                pass
        return False, None


def main():
    global current_lang
    global use_nvenc
    
    # 显示炫酷开屏动画，并获取语言和模式选择
    language, mode = show_splash_animation()  # ('en'/'zh', 'basic'/'advanced')
    current_lang = language  # 设置全局语言
    
    # 检测NVENC是否可用
    use_nvenc = check_nvenc_available()
    
    # 显示模式确认
    print()
    if mode == 'advanced':
        print(t('mode_advanced_selected'))
    else:
        print(t('mode_basic_selected'))
    
    # 显示NVENC可用性状态
    if use_nvenc:
        print(t('nvenc_available'))
    else:
        print(t('nvenc_not_available'))
    
    print("=" * 60)
    print(t('title'))
    print("=" * 60)
    
    # 高级模式额外支持的输入格式
    ADVANCED_INPUT_FORMATS = ['.mp4', '.mov', '.mkv', '.webm']
    
    # 根据模式确定支持的格式
    if mode == 'advanced':
        supported_formats = ALL_SUPPORTED_FORMATS + ADVANCED_INPUT_FORMATS
        print(f"\n{t('supported_formats')}")
        print(f"  {t('remux_recommended')}: {', '.join(REMUX_RECOMMENDED_FORMATS)}")
        print(f"  {t('transcode_recommended')}: {', '.join(TRANSCODE_RECOMMENDED_FORMATS)}")
        print(f"  {t('advanced_input_formats')}")
    else:
        supported_formats = ALL_SUPPORTED_FORMATS
        print(f"\n{t('supported_formats')}")
        print(f"  {t('remux_recommended')}: {', '.join(REMUX_RECOMMENDED_FORMATS)}")
        print(f"  {t('transcode_recommended')}: {', '.join(TRANSCODE_RECOMMENDED_FORMATS)}")
    
    # 高级模式：自定义输入路径
    if mode == 'advanced':
        custom_path = input(f"\n{t('custom_path_prompt')}").strip()
        if custom_path:
            if os.path.isdir(custom_path):
                current_dir = custom_path
                print(t('using_path', path=current_dir))
            else:
                print(t('invalid_path'))
                current_dir = os.getcwd()
        else:
            current_dir = os.getcwd()
    else:
        current_dir = os.getcwd()
    
    print(f"\n{t('current_path')}: {current_dir}")
    
    # 查找所有支持的视频文件
    print(f"\n{t('searching_files')}")
    video_files = find_video_files([current_dir], supported_formats)
    
    if not video_files:
        print(t('no_files_found'))
        print(f"{t('supported_formats_list')}: {', '.join(supported_formats)}")
        input(f"\n{t('press_enter_exit')}")
        sys.exit(0)
    
    # 按格式分类统计
    format_counts = {}
    for f in video_files:
        ext = f.suffix.lower()
        format_counts[ext] = format_counts.get(ext, 0) + 1
    
    print(f"\n{t('found_files', count=len(video_files))}")
    for ext, count in sorted(format_counts.items()):
        print(f"  {ext}: {t('files_count', count=count)}")
    print()
    for i, f in enumerate(video_files, 1):
        print(f"{i}. {f}")
    
    # 高级模式：选择输出格式 (移到搜索视频文件之后)
    output_format = '.mp4'  # 默认
    if mode == 'advanced':
        import msvcrt
        print(f"\n{t('output_format_prompt')}")
        print(f"  {t('output_format_1')}")
        print(f"  {t('output_format_2')}")
        print(f"  {t('output_format_3')}")
        print(f"  {t('press_output_format')}", end='', flush=True)
        
        while True:
            key = msvcrt.getch()
            if key == b'2':
                print('2')
                output_format = '.mov'
                break
            elif key == b'3':
                print('3')
                output_format = '.mkv'
                break
            elif key == b'1' or key == b'\r' or key == b'\n':
                print('1' if key == b'1' else '')
                output_format = '.mp4'
                break
        print(t('output_format_selected', format=output_format))
    
    # 高级模式：选择编码器
    encoder = 'hevc'  # 默认
    if mode == 'advanced':
        print(f"\n{t('encoder_prompt')}")
        print(f"  {t('encoder_1')}")
        print(f"  {t('encoder_2')}")
        print(f"  {t('encoder_3')}")
        print(f"  {t('press_encoder')}", end='', flush=True)
        
        while True:
            key = msvcrt.getch()
            if key == b'2':
                print('2')
                encoder = 'h264'
                break
            elif key == b'3':
                print('3')
                encoder = 'av1'
                break
            elif key == b'1' or key == b'\r' or key == b'\n':
                print('1' if key == b'1' else '')
                encoder = 'hevc'
                break
        encoder_names = {'hevc': 'HEVC/H.265', 'h264': 'AVC/H.264', 'av1': 'AV1'}
        print(t('encoder_selected', encoder=encoder_names[encoder]))
    
    # 检查是否有已存在的输出文件
    existing_files = []
    for video_file in video_files:
        video_path = Path(video_file)
        file_ext = video_path.suffix.lower()
        # 如果源文件和目标文件扩展名相同，使用带后缀的输出路径
        if file_ext == output_format:
            encoder_suffix = {'hevc': '_h265', 'h264': '_h264', 'av1': '_av1'}.get(encoder, '_converted')
            output_file = video_path.with_stem(video_path.stem + encoder_suffix).with_suffix(output_format)
        else:
            output_file = video_path.with_suffix(output_format)
        if output_file.exists():
            existing_files.append(output_file.name)
    
    overwrite = False
    if existing_files:
        print(f"\n{t('existing_files_found', count=len(existing_files))}")
        overwrite_input = input(t('overwrite_prompt')).strip().lower()
        overwrite = overwrite_input == 'y'
        if overwrite:
            print(t('will_overwrite'))
        else:
            print(t('will_skip'))
    
    # 逐个文件询问是否只转容器
    print("\n" + "=" * 60)
    print(t('select_mode'))
    print("=" * 60)
    
    # 批量模式选项
    batch_mode = False
    batch_format_settings = {}  # 存储每种格式的批量设置
    
    if len(video_files) > 1:
        batch_input = input(f"\n{t('batch_mode_prompt')}").strip().lower()
        batch_mode = batch_input == 'y'
        if batch_mode:
            print(t('batch_mode_enabled'))
            # 为每种存在的格式设置默认选项
            for ext in format_counts.keys():
                is_remux_recommended = ext in REMUX_RECOMMENDED_FORMATS
                print(f"\n{t('format_info', ext=ext, count=format_counts[ext])}")
                if is_remux_recommended:
                    print(t('remux_only_recommended'))
                    remux_input = input(t('remux_prompt_y')).strip().lower()
                    use_remux = remux_input != 'n'
                else:
                    print(t('transcode_recommended_msg'))
                    remux_input = input(t('remux_prompt_n')).strip().lower()
                    use_remux = remux_input == 'y'
                
                # 音频处理选择 - 批量模式下记录用户偏好，实际应用时根据文件检测决定
                # 用户选择是否对非AAC音频进行转码（对于已经是AAC的文件会自动跳过）
                audio_input = input(t('transcode_audio_prompt')).strip().lower()
                transcode_audio_pref = audio_input != 'n'  # 默认y
                
                batch_format_settings[ext] = {
                    'remux': use_remux,
                    'transcode_audio_pref': transcode_audio_pref  # 用户偏好，实际应用时会检查
                }
                
                mode_str = t('mode_remux_only') if use_remux else t('mode_transcode_h265')
                audio_str = t('audio_transcode_aac') if transcode_audio_pref else t('audio_copy')
                print(f"  ✓ {mode_str}, {audio_str}")
    
    # 存储每个文件的转换模式: True=remux, False=transcode
    file_modes = {}
    # 存储每个文件的音频转码选择: True=转码为AAC, False=复制音频
    audio_transcode_modes = {}
    
    unknown_text = "Unknown" if current_lang == 'en' else "未知"
    
    for i, f in enumerate(video_files, 1):
        file_ext = f.suffix.lower()
        
        # 如果使用批量模式，直接应用格式设置
        if batch_mode and file_ext in batch_format_settings:
            settings = batch_format_settings[file_ext]
            file_modes[str(f)] = settings['remux']
            
            # 对于remux模式，检查实际音频编码来决定是否需要转码
            if settings['remux']:
                audio_codec = get_audio_codec(f)
                # 如果音频已经是AAC（包括aac, aac_lc, aac_he等变体），使用AAC提示
                if audio_codec and (audio_codec == 'aac' or audio_codec.startswith('aac_') or 'aac' in audio_codec):
                    audio_transcode_modes[str(f)] = False
                else:
                    # 检查是否为必须转码的格式（PCM/TrueHD不兼容MP4）
                    is_incompatible = audio_codec and (audio_codec in AUDIO_NEEDS_TRANSCODE or audio_codec.startswith('pcm'))
                    # 使用用户偏好或强制转码
                    audio_transcode_modes[str(f)] = settings['transcode_audio_pref'] or is_incompatible
            else:
                audio_transcode_modes[str(f)] = True
            continue
        
        # 非批量模式：逐个询问
        # 检测视频编码格式
        codec = get_video_codec(f)
        codec_display = codec.upper() if codec else unknown_text
        # 检测音频编码格式
        audio_codec = get_audio_codec(f)
        audio_display = audio_codec.upper() if audio_codec else unknown_text
        
        # 根据格式类型设置默认推荐
        is_remux_recommended = file_ext in REMUX_RECOMMENDED_FORMATS
        
        # 高级模式：如果视频编码与目标编码器一致，建议只转容器
        if mode == 'advanced' and codec:
            # encoder: 'hevc', 'h264', 'av1'
            # codec: 'hevc', 'h265', 'h264', 'avc1', 'avc', 'av1', etc.
            codec_matches_encoder = False
            if encoder == 'hevc' and codec in ['hevc', 'h265']:
                codec_matches_encoder = True
            elif encoder == 'h264' and codec in ['h264', 'avc1', 'avc']:
                codec_matches_encoder = True
            elif encoder == 'av1' and codec == 'av1':
                codec_matches_encoder = True
            
            if codec_matches_encoder:
                is_remux_recommended = True
        
        print(f"\n[{i}/{len(video_files)}] {Path(f).name}")
        print(f"  {t('video_codec')}: {codec_display} | {t('audio_codec')}: {audio_display}")
        
        if is_remux_recommended:
            print(f"  {t('format_remux_recommended', ext=file_ext)}")
            remux_input = input(t('remux_prompt_detail', default='y')).strip().lower()
            file_modes[str(f)] = remux_input != 'n'  # 默认y
        else:
            print(f"  {t('format_transcode_recommended', ext=file_ext)}")
            remux_input = input(t('remux_prompt_detail', default='n')).strip().lower()
            file_modes[str(f)] = remux_input == 'y'  # 默认n
        
        if file_modes[str(f)]:
            print(t('will_remux'))
            # 对于remux文件，检查音频是否为AAC（包括aac, aac_lc, aac_he等变体）
            is_aac = audio_codec and (audio_codec == 'aac' or audio_codec.startswith('aac_') or 'aac' in audio_codec)
            if audio_codec and not is_aac:
                # 检查是否为必须转码的格式（PCM/TrueHD）
                is_incompatible = (audio_codec in AUDIO_NEEDS_TRANSCODE or audio_codec.startswith('pcm'))
                if is_incompatible:
                    print(t('audio_incompatible', codec=audio_display))
                    audio_transcode_modes[str(f)] = True
                else:
                    audio_input = input(t('audio_transcode_prompt', codec=audio_display)).strip().lower()
                    audio_transcode_modes[str(f)] = audio_input != 'n'  # 默认y
                    if audio_transcode_modes[str(f)]:
                        print(t('will_transcode_audio'))
                    else:
                        print(t('will_copy_audio'))
            elif is_aac:
                # 音频已经是AAC，询问是否仍要转码（默认n）
                audio_input = input(t('audio_aac_transcode_prompt')).strip().lower()
                audio_transcode_modes[str(f)] = audio_input == 'y'  # 默认n
                if audio_transcode_modes[str(f)]:
                    print(t('will_transcode_audio'))
                else:
                    print(t('audio_already_aac'))
            else:
                # 没有检测到音频编码，默认复制
                audio_transcode_modes[str(f)] = False
        else:
            print(t('will_transcode'))
            # 转码模式也询问音频是否转AAC
            is_aac = audio_codec and (audio_codec == 'aac' or audio_codec.startswith('aac_') or 'aac' in audio_codec)
            if is_aac:
                # 原音频是AAC，询问是否转码（默认n）
                audio_input = input(t('audio_aac_transcode_prompt')).strip().lower()
                audio_transcode_modes[str(f)] = audio_input == 'y'  # 默认n
                if audio_transcode_modes[str(f)]:
                    print(t('will_transcode_audio'))
                else:
                    print(t('audio_already_aac'))
            elif audio_codec:
                # 原音频不是AAC，询问是否转码（默认y）
                audio_input = input(t('audio_transcode_prompt', codec=audio_display)).strip().lower()
                audio_transcode_modes[str(f)] = audio_input != 'n'  # 默认y
                if audio_transcode_modes[str(f)]:
                    print(t('will_transcode_audio'))
                else:
                    print(t('will_copy_audio'))
            else:
                # 没有检测到音频编码，默认转码
                audio_transcode_modes[str(f)] = True

    
    # 统计选择
    remux_count = sum(1 for v in file_modes.values() if v)
    transcode_count = len(file_modes) - remux_count
    print(f"\n{t('selection_summary', remux=remux_count, transcode=transcode_count)}")
    
    # 原始文件处理选项
    print("\n" + "=" * 60)
    print(t('original_file_handling'))
    print("=" * 60)
    delete_input = input(t('delete_original_prompt')).strip().lower()
    delete_on_success = delete_input == 'y'
    if delete_on_success:
        print(t('will_delete_original'))
    else:
        print(t('will_keep_original'))
    
    # 显示预估时间提示（在确认提示之前）
    total_size = sum(get_file_size(f) for f in video_files)
    print(f"\n{t('total_size')}: {format_size(total_size)}")
    if remux_count > 0 and transcode_count == 0:
        print(t('estimated_time_remux'))
    elif transcode_count > 0:
        print(t('estimated_time_transcode'))
    
    # 确认开始转换
    response = input(f"\n{t('start_conversion_prompt', count=len(video_files))}").strip().lower()
    if response == 'n':
        print(t('cancel_conversion'))
        sys.exit(0)
    
    # 只有需要转码的文件才需要设置转码参数
    preset = "p5" if use_nvenc else "medium"
    crf = 21
    deinterlace = False
    if transcode_count > 0:
        print(f"\n{t('encoding_settings')}")
        # 显示编码器类型
        if use_nvenc:
            print(t('using_nvenc'))
            preset = input(t('nvenc_preset_prompt')).strip() or "p5"
        else:
            print(t('using_cpu_encoder'))
            preset = input(t('cpu_preset_prompt')).strip() or "medium"
        crf_input = input(t('quality_prompt')).strip()
        crf = int(crf_input) if crf_input else 21
        deinterlace_input = input(t('deinterlace_prompt')).strip().lower()
        deinterlace = deinterlace_input == 'y'
        if deinterlace:
            print(t('deinterlace_enabled'))
    
    workers_input = input(t('concurrent_prompt')).strip()
    
    # 验证并设置并发数
    try:
        workers = int(workers_input) if workers_input else 3
        if workers < 1:
            workers = 3
        elif workers > 10:
            print(t('concurrent_warning'))
            workers = 10
    except ValueError:
        print(t('invalid_input_default'))
        workers = 3
    
    if workers > 1:
        print(t('will_process_concurrent', count=workers))
    

    # 批量转换（使用线程池）
    success_count = 0
    fail_count = 0
    total_start_time = time.time()
    
    print("\n" + "=" * 60)
    if workers > 1:
        print(t('start_batch_concurrent', count=workers))
    else:
        print(t('start_batch_conversion'))
    print("=" * 60)
    print()  # 为进度条预留空行
    
    with ThreadPoolExecutor(max_workers=workers) as executor:
        # 提交所有任务
        futures = {}
        for i, video_file in enumerate(video_files, 1):
            file_key = str(video_file)
            if file_modes.get(file_key, True):  # 默认remux
                future = executor.submit(
                    remux_to_mp4, 
                    video_file, 
                    index=i,
                    total=len(video_files),
                    overwrite=overwrite,
                    transcode_audio=audio_transcode_modes.get(file_key, False),
                    delete_on_success=delete_on_success,
                    output_format=output_format
                )
            else:
                future = executor.submit(
                    convert_to_h265, 
                    video_file, 
                    preset=preset, 
                    crf=crf, 
                    deinterlace=deinterlace,
                    index=i,
                    total=len(video_files),
                    overwrite=overwrite,
                    delete_on_success=delete_on_success,
                    output_format=output_format,
                    encoder=encoder
                )
            futures[future] = video_file
        
        # 等待所有任务完成
        for future in as_completed(futures):
            try:
                result = future.result()
                if isinstance(result, tuple):
                    success, _ = result
                else:
                    success = result
                if success:
                    success_count += 1
                else:
                    fail_count += 1
            except Exception as e:
                fail_count += 1
                with print_lock:
                    print(f"\n{t('task_exception', error=str(e))}")
    
    total_elapsed_time = time.time() - total_start_time
    
    # 确保所有进度条显示完成后再显示总结
    print("\n")  # 换行
    
    # 总结
    print("\n" + "=" * 60)
    print(t('conversion_complete'))
    print("=" * 60)
    print(f"{t('success')}: {success_count}")
    print(f"{t('failed')}: {fail_count}")
    print(f"{t('total')}: {len(video_files)}")
    print(f"{t('total_time')}: {format_time(total_elapsed_time)}")
    
    # 显示文件大小对比
    if conversion_results:
        print("\n" + "-" * 60)
        print(t('size_comparison'))
        print("-" * 60)
        total_original = 0
        total_output = 0
        for file_key, result in conversion_results.items():
            if result['success']:
                orig_size = result['original_size']
                out_size = result['output_size']
                total_original += orig_size
                total_output += out_size
                
                # 计算大小变化百分比（变小为负，变大为正）
                if orig_size > 0:
                    ratio = ((out_size - orig_size) / orig_size) * 100
                    ratio_str = f"{ratio:+.1f}%"
                else:
                    ratio_str = "N/A"
                
                print(f"  {result['input']}")
                print(f"    {format_size(orig_size)} → {format_size(out_size)} ({ratio_str})")
        
        # 总计
        if total_original > 0:
            total_ratio = ((total_output - total_original) / total_original) * 100
            print("-" * 60)
            print(f"{t('total')}: {format_size(total_original)} → {format_size(total_output)} ({total_ratio:+.1f}%)")
            if total_ratio < 0:
                print(f"{t('space_saved')}: {format_size(total_original - total_output)}")
            elif total_ratio > 0:
                print(f"{t('space_increased')}: {format_size(total_output - total_original)}")
    
    # 等待用户按键后退出
    input(f"\n{t('press_enter_exit')}")

if __name__ == "__main__":
    main()
