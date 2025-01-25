import torch
import whisper
import os
import natsort
from tqdm import tqdm

# 设置参数
path = 'after-vad'
audio_extensions = ('.wav', '.mp3', '.flac', '.ogg', '.m4a', '.aac')
result_path = "transcribe_result.txt"  # 保存结果的文件

# 加载模型
device = torch.device('cuda')
model = whisper.load_model(
    name="large-v3", device=device, download_root='models')  # 模型太大了，所以手动指定保存的位置

file_list = [f for f in os.listdir(
    path) if f.lower().endswith(audio_extensions)]
file_list = natsort.natsorted(file_list, alg=natsort.ns.PATH)

# 逐个文件转录
with open(result_path, "a+", encoding="utf-8") as f:
    for filename in tqdm(file_list, desc="Transcribing files"):
        file_path = os.path.join(path, filename)
        audio = whisper.load_audio(file_path)
        result = model.transcribe(audio, language='zh', task='transcribe', fp16=False,
                                  initial_prompt="以下是普通话的句子。")
        segments = result["segments"]
        texts = []
        num_segments = len(segments)
        for idx, segment in enumerate(segments):
            segment_text = segment["text"]

            # 如果不是最后一段，且最后一个字符不是句号或逗号，添加逗号
            if idx != num_segments - 1 and segment_text[-1] not in ('。', ','):
                segment_text += ','

            texts.append(segment_text)
        full_text = ''.join(texts)
        f.write(f"{filename}|{full_text}\n")
