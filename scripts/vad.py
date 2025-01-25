import torch
import os
import time
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np

torch.set_num_threads(1)

# 设置参数
audio_path = 'raw/2.wav'
save_path = 'after-vad'
min_speech_duration_ms = 1000
max_speech_duration_s = 20

model, utils = torch.hub.load(
    repo_or_dir='snakers4/silero-vad', model='silero_vad')
(get_speech_timestamps, save_audio, read_audio, VADIterator, collect_chunks) = utils
wav = read_audio(audio_path, sampling_rate=48000)

# VAD
start = time.time()
speech_timestamps = get_speech_timestamps(
    wav, model, sampling_rate=48000, min_speech_duration_ms=min_speech_duration_ms, max_speech_duration_s=max_speech_duration_s)
end = time.time()
print('First VAD costs {:.2f}s'.format(end - start))

# 保存音频
durations = []
for idx, timestamp in tqdm(enumerate(speech_timestamps), total=len(speech_timestamps), desc='Saving segments'):
    file_name = os.path.join(save_path, '{}.wav'.format(idx))
    save_audio(file_name, collect_chunks(
        [timestamp], wav), sampling_rate=48000)
    duration = (timestamp["end"] - timestamp["start"]) / 48000
    durations.append(duration)

# 绘制时长分布
plt.hist(durations, bins=20, color='skyblue', edgecolor='black')
plt.savefig('duration_distribution.png')
