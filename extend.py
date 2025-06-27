import os
import json
from tkinter import Toplevel, messagebox
from tkinter import ttk

def ShowError(title, error_type, error):
    """错误显示函数（假设原有代码中有定义）"""
    print(f"{title}: {error_type} - {error}")

if __name__ != "__main__":

    def maximize_abyss_plant_levels(self):
        """
        将深渊植物等级设置为满级
        """
        if self.config["use_custom_path"]:
            player_data_path = os.path.join(self.config["path"], "playerData.json")
        else:
            player_data_path = f"C:/Users/{os.getenv('USERNAME')}/AppData/LocalLow/LanPiaoPiao/PlantsVsZombiesRH/playerData.json"
        try:
            # 读取 playerData.json 文件
            with open(player_data_path, 'r', encoding='utf-8') as file:
                player_data = json.load(file)

            # 生成满级的深渊植物等级数据
            max_level_data = []

            # 假设 self.id_to_name 在主程序中定义
            plant_ids = list(self.id_to_name.keys())[1:]  # 去除 -1 的id

            for plant_id in plant_ids:
                max_level_data.append({"thePlantType": plant_id, "level": 3})

            # 更新 playerData 中的 abyssPlantLevels 字段
            player_data["abyssPlantLevels"] = max_level_data

            # 保存修改后的 playerData.json 文件
            with open(player_data_path, 'w', encoding='utf-8') as file:
                json.dump(player_data, file, indent=4)

            messagebox.showinfo("提示", "深渊植物已全部设置为满级！请重启游戏")
        except Exception as e:
            ShowError("修改深渊植物等级时出错", type(e), e)
            messagebox.showerror("提示", f"修改深渊植物等级时出错：{str(e)}")


    def format_abyss_plant_levels(self):
        """
        格式化深渊植物等级
        """
        if self.config["use_custom_path"]:
            player_data_path = os.path.join(self.config["path"], "playerData.json")
        else:
            player_data_path = f"C:/Users/{os.getenv('USERNAME')}/AppData/LocalLow/LanPiaoPiao/PlantsVsZombiesRH/playerData.json"
        try:
            with open(player_data_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            data["abyssPlantLevels"] = []
            with open(player_data_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
            messagebox.showinfo("提示", "深渊植物等级已格式化，请重启游戏")
        except FileNotFoundError:
            messagebox.showerror("提示", "未找到 playerData.json 文件")
        except Exception as e:
            messagebox.showerror("提示", f"发生未知错误: {e}")


    def open_modify_plant_level_window(self):
        """
        创建修改特定植物等级的窗口
        """
        input_window = Toplevel(self.root)
        input_window.title("输入植物 ID 和等级")
        input_window.geometry("400x300")
        input_window.configure(bg='#FFF5F0')
        input_window.transient(self.root)  # 设置为主窗口的子窗口
        input_window.grab_set()  # 模态窗口，阻止操作主窗口

        if self.config["use_custom_path"]:
            player_data_path = os.path.join(self.config["path"], "playerData.json")
        else:
            player_data_path = f"C:/Users/{os.getenv('USERNAME')}/AppData/LocalLow/LanPiaoPiao/PlantsVsZombiesRH/playerData.json"

        try:
            with open(player_data_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            abyss_plant_levels = data.get("abyssPlantLevels", [])
        except FileNotFoundError:
            abyss_plant_levels = []
            messagebox.showerror("提示", f"未找到文件: {player_data_path}")
        except Exception as e:
            abyss_plant_levels = []
            messagebox.showerror("提示", f"发生未知错误: {str(e)}")

        ttk.Label(input_window, text="植物 ID:", style='Custom.TLabel').pack(pady=10)
        plant_id_entry = ttk.Entry(input_window)
        plant_id_entry.pack(pady=5)
        plant_id_entry.focus_set()  # 设置焦点到输入框

        ttk.Label(input_window, text="植物等级 (1~3):", style='Custom.TLabel').pack(pady=10)
        plant_level_entry = ttk.Entry(input_window)
        plant_level_entry.pack(pady=5)

        def modify_plant_level():
            try:
                plant_id = int(plant_id_entry.get())
                plant_level = int(plant_level_entry.get())
                if 1 <= plant_level <= 3:
                    _modify_plant_level(self, plant_id, plant_level, player_data_path, abyss_plant_levels)
                    input_window.destroy()
                else:
                    messagebox.showerror("提示", "植物等级必须在 1~3 之间")
            except ValueError:
                messagebox.showerror("提示", "请输入有效的整数")

        button = ttk.Button(input_window, text="修改", command=modify_plant_level, style='Custom.TButton')
        button.pack(pady=20)

        # 绑定回车键触发修改
        input_window.bind('<Return>', lambda event: modify_plant_level())


    def _modify_plant_level(self, plant_id, plant_level, player_data_path, abyss_plant_levels):
        """
        修改特定植物的等级
        """
        found = False
        for item in abyss_plant_levels:
            if item["thePlantType"] == plant_id:
                item["level"] = plant_level
                found = True
                break
        if not found:
            new_item = {"thePlantType": plant_id, "level": plant_level}
            abyss_plant_levels.append(new_item)
            abyss_plant_levels.sort(key=lambda x: x["thePlantType"])

        try:
            with open(player_data_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            data["abyssPlantLevels"] = abyss_plant_levels
            with open(player_data_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
            messagebox.showinfo("提示", "修改成功")
        except Exception as e:
            messagebox.showerror("提示", f"发生未知错误: {str(e)}")

    def open_abyss_money_window(self):
        """
        创建修改叶绿素的窗口
        """
        # 获取当前的叶绿素值
        current_value = _get_current_abyss_money(self)

        input_window = Toplevel(self.root)
        input_window.title("修改叶绿素")
        input_window.geometry("250x130")
        input_window.configure(bg='#FFF5F0')
        input_window.transient(self.root)  # 设置为主窗口的子窗口
        input_window.grab_set()  # 模态窗口，阻止操作主窗口

        # 显示当前值的标签
        ttk.Label(input_window, text=f"当前叶绿素: {current_value}", style='Custom.TLabel').pack(pady=10)

        # 输入框
        entry = ttk.Entry(input_window)
        entry.pack(pady=5)
        entry.insert(0, str(current_value))  # 预填充当前值
        entry.select_range(0, "end")  # 选中所有文本
        entry.focus_set()  # 设置焦点到输入框

        def modify_abyss_money():
            try:
                new_value = int(entry.get())
                _modify_abyss_money(self, new_value)
                input_window.destroy()
            except ValueError:
                messagebox.showerror("提示", "请输入有效的整数")

        button = ttk.Button(input_window, text="修改", command=modify_abyss_money, style='Custom.TButton')
        button.pack(pady=10)

        # 绑定回车键触发修改
        input_window.bind('<Return>', lambda event: modify_abyss_money())


    def _get_current_abyss_money(self):
        """
        获取当前的深渊金钱值
        """
        if self.config["use_custom_path"]:
            player_data_path = os.path.join(self.config["path"], "playerData.json")
        else:
            player_data_path = f"C:/Users/{os.getenv('USERNAME')}/AppData/LocalLow/LanPiaoPiao/PlantsVsZombiesRH/playerData.json"

        try:
            with open(player_data_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return data.get("abyssMoney", 0)
        except FileNotFoundError:
            messagebox.showerror("错误", f"未找到文件: {player_data_path}")
            return 0
        except Exception as e:
            messagebox.showerror("错误", f"发生未知错误: {str(e)}")
            return 0


    def _modify_abyss_money(self, new_value):
        """
        修改叶绿素
        """
        if self.config["use_custom_path"]:
            player_data_path = os.path.join(self.config["path"], "playerData.json")
        else:
            player_data_path = f"C:/Users/{os.getenv('USERNAME')}/AppData/LocalLow/LanPiaoPiao/PlantsVsZombiesRH/playerData.json"

        try:
            with open(player_data_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            data["abyssMoney"] = new_value
            with open(player_data_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
            messagebox.showinfo("提示", f"叶绿素已修改为 {new_value}，请重启游戏")
        except FileNotFoundError:
            messagebox.showerror("提示", f"未找到文件: {player_data_path}")
        except Exception as e:
            messagebox.showerror("提示", f"发生未知错误: {str(e)}")


    def open_abyss_level_window(self):
        """
        创建修改深渊关卡的窗口
        """
        input_window = Toplevel(self.root)
        input_window.title("输入深渊关卡的数值")
        input_window.geometry("300x200")
        input_window.configure(bg='#FFF5F0')
        input_window.transient(self.root)  # 设置为主窗口的子窗口
        input_window.grab_set()  # 模态窗口，阻止操作主窗口

        if self.config["use_custom_path"]:
            player_data_path = os.path.join(self.config["path"], "playerData.json")
        else:
            player_data_path = f"C:/Users/{os.getenv('USERNAME')}/AppData/LocalLow/LanPiaoPiao/PlantsVsZombiesRH/playerData.json"

        try:
            with open(player_data_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            current_level = data.get("abyssLevel", 0)
        except FileNotFoundError:
            current_level = 0
            messagebox.showerror("提示", f"未找到文件: {player_data_path}")
        except Exception as e:
            current_level = 0
            messagebox.showerror("提示", f"发生未知错误: {str(e)}")

        ttk.Label(input_window, text=f"当前深渊等级: {current_level}", style='Custom.TLabel').pack(pady=10)

        entry = ttk.Entry(input_window)
        entry.pack(pady=20)
        entry.focus_set()  # 设置焦点到输入框

        def modify_abyss_level():
            try:
                new_value = int(entry.get())
                _modify_abyss_level(self, new_value)
                input_window.destroy()
            except ValueError:
                messagebox.showerror("提示", "请输入有效的整数")

        button = ttk.Button(input_window, text="修改", command=modify_abyss_level, style='Custom.TButton')
        button.pack(pady=10)

        # 绑定回车键触发修改
        input_window.bind('<Return>', lambda event: modify_abyss_level())


    def _modify_abyss_level(self, new_value):
        """
        修改深渊关卡
        """
        if self.config["use_custom_path"]:
            player_data_path = os.path.join(self.config["path"], "playerData.json")
        else:
            player_data_path = f"C:/Users/{os.getenv('USERNAME')}/AppData/LocalLow/LanPiaoPiao/PlantsVsZombiesRH/playerData.json"

        try:
            with open(player_data_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            data["abyssLevel"] = new_value
            with open(player_data_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
            messagebox.showinfo("提示", f"深渊关卡已修改为 {new_value}，请重启游戏")
        except FileNotFoundError:
            messagebox.showerror("提示", f"未找到文件: {player_data_path}")
        except Exception as e:
            messagebox.showerror("提示", f"发生未知错误: {str(e)}")


    def open_abyss_refresh_count_window(self):
        """
        创建修改深渊刷新次数的窗口
        """
        if self.config["use_custom_path"]:
            player_data_path = os.path.join(self.config["path"], "playerData.json")
        else:
            player_data_path = f"C:/Users/{os.getenv('USERNAME')}/AppData/LocalLow/LanPiaoPiao/PlantsVsZombiesRH/playerData.json"

        try:
            with open(player_data_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            current_count = data.get("abyssRefreshCount", 0)
        except FileNotFoundError:
            current_count = 0
            messagebox.showerror("提示", f"未找到文件: {player_data_path}")
        except Exception as e:
            current_count = 0
            messagebox.showerror("提示", f"发生未知错误: {str(e)}")

        input_window = Toplevel(self.root)
        input_window.title("输入深渊刷新次数")
        input_window.geometry("250x130")
        input_window.configure(bg='#FFF5F0')
        input_window.transient(self.root)  # 设置为主窗口的子窗口
        input_window.grab_set()  # 模态窗口，阻止操作主窗口

        # 显示当前值的标签
        ttk.Label(input_window, text=f"当前深渊刷新次数: {current_count}", style='Custom.TLabel').pack(pady=10)

        # 输入框
        entry = ttk.Entry(input_window)
        entry.pack(pady=5)
        entry.insert(0, str(current_count))  # 预填充当前值
        entry.select_range(0, "end")  # 选中所有文本
        entry.focus_set()  # 设置焦点到输入框

        def modify_abyss_refresh_count():
            try:
                new_value = int(entry.get())
                _modify_abyss_refresh_count(self, new_value, player_data_path)
                input_window.destroy()
            except ValueError:
                messagebox.showerror("提示", "请输入有效的整数")

        button = ttk.Button(input_window, text="修改", command=modify_abyss_refresh_count, style='Custom.TButton')
        button.pack(pady=10)

        # 绑定回车键触发修改
        input_window.bind('<Return>', lambda event: modify_abyss_refresh_count())


    def _modify_abyss_refresh_count(self, new_value, player_data_path):
        """
        修改深渊刷新次数
        """
        try:
            with open(player_data_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            data["abyssRefreshCount"] = new_value
            with open(player_data_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
            messagebox.showinfo("提示", "修改成功！")
        except FileNotFoundError:
            messagebox.showerror("提示", f"未找到文件: {player_data_path}")
        except Exception as e:
            messagebox.showerror("提示", f"发生未知错误: {str(e)}")