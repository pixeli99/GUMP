import os
import shutil
import subprocess

# 定义源目录和目标目录
source_dir = "/lpai/dataset/nuplan-v1-1/0-1-0/nuPlan-v1.1/data/cache/trainval"
target_dir = "/lpai/lipengxiang/nuplan/nuplan_trainval_subset"
preprocess_script = "./scripts/preprocess/cache_nuplan_data_v1_1.sh"

# 获取源目录中的所有文件
all_files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]
all_files.sort()

# 每次处理2000个文件
batch_size = 10
total_files = len(all_files)

for i in range(0, total_files, batch_size):
    # 按顺序抽取当前批次的文件
    sampled_files = all_files[i:i + batch_size]

    # 确保目标目录存在
    os.makedirs(target_dir, exist_ok=True)

    # 复制文件到目标目录
    for file_name in sampled_files:
        src_file = os.path.join(source_dir, file_name)
        dst_file = os.path.join(target_dir, file_name)
        shutil.copy(src_file, dst_file)
        print(f"Copied {file_name} to {target_dir}")

    # 执行预处理脚本
    subprocess.run(["bash", preprocess_script], check=True)

    # 清空目标目录
    for file_name in os.listdir(target_dir):
        file_path = os.path.join(target_dir, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
        print(f"Removed {file_name} from {target_dir}")

    print(f"Batch {i // batch_size + 1} processed.")
