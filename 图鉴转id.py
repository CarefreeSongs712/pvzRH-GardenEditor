import json

# 定义输入和输出文件路径
input_file_path = 'f:/no_backup/其他/pvz/融合/自制合集/禅境花园修改器（新）/禅境花园修改器1.4.0/LawnString.json'
output_file_path = 'output.txt'

try:
    # 读取 JSON 文件
    with open(input_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # 准备存储格式化数据的列表
    formatted_lines = []
    
    # 遍历 plants 列表
    for plant in data.get('plants', []):
        seed_type = plant.get('seedType')
        name = plant.get('name')
        formatted_line = f"ID: {seed_type}, {name}"
        formatted_lines.append(formatted_line)
    
    # 将格式化数据写入输出文件
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for line in formatted_lines:
            output_file.write(line + '\n')
    
    print(f"数据已成功写入 {output_file_path}")

except FileNotFoundError:
    print(f"未找到文件: {input_file_path}")
except json.JSONDecodeError:
    print(f"无法解析 {input_file_path} 中的 JSON 数据")
except Exception as e:
    print(f"发生错误: {e}")
