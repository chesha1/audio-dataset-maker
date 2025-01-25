import os
import torchaudio
from tqdm import tqdm

# 输入文件夹，计算该文件夹中所有音频文件的总长度
path = 'after-vad'
duration = 0
audio_extensions = ('.wav', '.mp3', '.flac', '.ogg', '.m4a', '.aac')

# 过滤文件列表，只保留音频文件
file_list = [f for f in os.listdir(
    path) if f.lower().endswith(audio_extensions)]

for filename in tqdm(file_list, desc="Calculating duration"):
    file_path = os.path.join(path, filename)
    try:
        # 获取音频文件信息
        audio_info = torchaudio.info(file_path)
        duration += audio_info.num_frames / audio_info.sample_rate
    except Exception as e:
        print(f"无法处理文件 {file_path}：{e}")

minute, second = divmod(duration, 60)
hour, minute = divmod(minute, 60)
print(f'{len(file_list)} files, {int(hour)}:{int(minute):02d}:{int(second):02d}')
