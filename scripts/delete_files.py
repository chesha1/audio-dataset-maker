import os

# 设置参数
folder_path = 'after-vad'
txt_path = 'transcribe_result.txt'

# 记录所有允许存在的文件
allowed_files = set()
with open(txt_path, 'r', encoding='utf-8') as f:
    for line in f:
        if '|' in line:
            filename = line.strip().split('|')[0]
            allowed_files.add(filename)

# 遍历文件夹
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    # 如果是文件且不在允许列表中,且不是.gitkeep,则删除
    if os.path.isfile(file_path) and filename not in allowed_files and filename != '.gitkeep':
        os.remove(file_path)
        print(f'Deleted: {filename}')
