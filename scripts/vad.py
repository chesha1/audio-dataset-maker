import torch
import os
import time
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np

torch.set_num_threads(1)

# 参数配置
input_dir = "raw"  # 原始音频所在目录
save_path = "after-vad"  # 分段后音频保存目录
min_speech_duration_ms = 1000
max_speech_duration_s = 20
audio_extensions = (".wav", ".mp3", ".flac", ".ogg", ".m4a", ".aac")

# 如果输出目录不存在，则创建
os.makedirs(save_path, exist_ok=True)

# 加载 Silero VAD 模型
model, utils = torch.hub.load(repo_or_dir="snakers4/silero-vad", model="silero_vad")
(get_speech_timestamps, save_audio, read_audio, VADIterator, collect_chunks) = utils

# 用于累积所有音频片段时长（秒），绘制直方图
all_durations = []

# 遍历目录，筛选音频后缀文件
audio_files = [f for f in os.listdir(input_dir) if f.lower().endswith(audio_extensions)]

for audio_file in audio_files:
    audio_path = os.path.join(input_dir, audio_file)
    print(f"处理文件: {audio_file}")

    # 获取不带后缀的原始文件名（例如“1.wav” -> “1”）
    original_root, original_ext = os.path.splitext(audio_file)

    # 读取音频并统一重采样到 16k
    # 如果不指定 sampling_rate，则默认会用 16k。为了更清晰，显式写出来。
    wav = read_audio(audio_path, sampling_rate=16000)

    # 执行 VAD
    start = time.time()
    speech_timestamps = get_speech_timestamps(
        wav,
        model,
        sampling_rate=16000,  # 这里的采样率与上面读入一致
        min_speech_duration_ms=min_speech_duration_ms,
        max_speech_duration_s=max_speech_duration_s,
    )
    end = time.time()
    print(f"{audio_file} 的 VAD 耗时: {end - start:.2f}s")

    # 保存切分后的音频片段，不再单独创建文件夹，直接在文件名加入后缀
    for idx, timestamp in tqdm(
        enumerate(speech_timestamps),
        total=len(speech_timestamps),
        desc=f"保存切分片段 -> {audio_file}",
    ):
        # 构建新的文件名，例如：1.wav -> 1-0.wav
        segment_file_name = f"{original_root}-{idx}.wav"
        save_file_path = os.path.join(save_path, segment_file_name)

        # 从原始（已是 16k）波形中提取该片段
        audio_chunk = collect_chunks([timestamp], wav)

        # 保存切分结果，输出采样率同样设置为 16k
        save_audio(save_file_path, audio_chunk, sampling_rate=16000)

        # 记录片段时长，注意这里除以 16k
        duration = (timestamp["end"] - timestamp["start"]) / 16000
        all_durations.append(duration)

# 绘制所有切分结果的时长分布
plt.figure(figsize=(8, 5))
plt.hist(all_durations, bins=20, color="skyblue", edgecolor="black")
plt.xlabel("Segment Duration (s)")
plt.ylabel("Count")
plt.title("Segment Duration Distribution for All Files")
plt.savefig("duration_distribution.png")
plt.close()

print("完成所有文件的 VAD 处理并绘制时长分布图")
