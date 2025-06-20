import os
import shutil

def find_and_copy_unique_files(folder1, folder2, output_folder):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 获取两个文件夹中的所有文件名
    files1 = set(os.listdir(folder1))
    files2 = set(os.listdir(folder2))

    # 找出名字不一样的文件
    unique_files = files1.symmetric_difference(files2)

    # 复制文件到新文件夹
    for file_name in unique_files:
        if file_name in files1:
            source_path = os.path.join(folder1, file_name)
        else:
            source_path = os.path.join(folder2, file_name)

        destination_path = os.path.join(output_folder, file_name)

        if os.path.isfile(source_path):
            shutil.copy2(source_path, destination_path)
            print(f"已复制文件: {source_path} 到 {destination_path}")

if __name__ == "__main__":
    # 替换为实际的文件夹路径
    folder1 = "D:\MyDesktop\export2.5\Texture2D"
    folder2 = "D:\临时1.25\\texture\Texture2D"
    output_folder = "diff"

    find_and_copy_unique_files(folder1, folder2, output_folder)
