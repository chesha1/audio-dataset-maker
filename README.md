# audio-dataset-maker
参考[文章](https://echoccc.online/posts/tts-2025/)，把原始数据转化成可用的音频数据集

## 使用方法
1. 对音频源文件进行去噪，增强人声处理
2. 把音频源文件放入 `raw/` 文件夹中，编辑 `scripts/vad.py` 中的参数
3. 执行 `python -u scripts/vad.py` 后，音频切片出现在 `after-vad/` 中，音频分布图片 `duration_distribution.png` 出现在项目根目录下
4. 执行 `python -u scripts\transcribe.py` 后，结果 `transcribe_result.txt` 出现在项目根目录下
5. 手动校验后，对于想要删除的文件，直接在文件中删除这一行，然后 `python -u scripts\delete_files.py` 一键删除不想要的文件
6. `python -u scripts\audio_duration.py` 统计数据集大小

## TODO
- [x] VAD 原始音频重采样到 16 khz 单声道 
- [x] 支持 `raw/` 中多个文件的处理
- [ ] VAD 多线程或使用 GPU 加速
- [ ] 把短小切片合成，符合正态分布
- [ ] 整理 `requirements.txt`
