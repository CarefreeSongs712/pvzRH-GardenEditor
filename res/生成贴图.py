import os
from PIL import Image
input_dir = 'F:\\no_backup\其他\pvz\融合\自制合集\-1'

output_dir = 'F:\\no_backup\其他\pvz\融合\自制合集\禅境花园修改器（新）\禅境花园修改器1.3.2 cid\\res\\'

for filename in os.listdir(input_dir):
    if filename.endswith('.png'):
        input_path = os.path.join(input_dir, filename)
        try:
            with Image.open(input_path) as img:
                cropped_img = img.resize((30, 30))
                output_path = os.path.join(output_dir+"0\\", filename)
                cropped_img.save(output_path)
                cropped_img = img.resize((45, 45))
                output_path = os.path.join(output_dir+"1\\", filename)
                cropped_img.save(output_path)
                cropped_img = img.resize((60, 60))
                output_path = os.path.join(output_dir+"2\\", filename)
                cropped_img.save(output_path)
                print(f"{filename} ok")
        except Exception as e:
            print(f" {filename} : {e}")

            