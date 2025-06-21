print("""
# 原创作者：B站 听雨夜荷
# 拓展作者：Sh茗
# 拓展版本：3.2.0
# 交流群：1015660780
# 日期：2025/6/16
# 适配版本：2.6.1
# 功能：禅境花园修改器 + 深渊植物等级修改 + 深渊植物等级格式化 + 深渊词条刷新次数修改
""")
import os
import time
import json
import threading
import re
from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter.messagebox import *
from tkinter import simpledialog
from PIL import Image, ImageTk

# 定义错误显示函数
ShowError = print


class GardenModifier:
    def __init__(self, root):
        """
        初始化花园修改器类
        :param root: Tkinter 根窗口
        """
        self.root = root
        self.root.title('禅境花园修改器拓展版3.2.0原创：听雨夜荷')
        self.root.geometry('975x650')  # 调整窗口高度以容纳新增内容

        # 切换到当前脚本所在目录
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        # 显示公告窗口
        self.show_announcement()

        # 加载植物 ID 信息
        self.load_plant_info()
        # 初始化配置
        self.init_config()
        # 裁剪图片
        self.pre_images()
        # 加载图片资源
        self.load_images()
        # 创建菜单
        self.create_menu()
        # 创建界面组件
        self.create_widgets()
        # 初始化最后选中的索引
        self.last_selected_index = None
        # 加载花园数据
        self.load_garden_data()

    def show_announcement(self):
        """显示公告窗口"""
        # 创建公告窗口
        self.announcement_window = Toplevel(self.root)
        self.announcement_window.title("公告3.2.0")
        self.announcement_window.geometry("400x200")
        self.announcement_window.resizable(False, False)
        self.announcement_window.transient(self.root)  # 设置为主窗口的子窗口
        self.announcement_window.grab_set()  # 模态窗口，阻止操作主窗口

        # 计算窗口居中位置
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 200) // 2
        self.announcement_window.geometry(f"+{x}+{y}")

        # 添加公告文本
        Label(
            self.announcement_window,
            text="本修改器为哔哩哔哩up主听雨夜荷制作的，本人只是做了几个拓展功能。拓展功能需要重启游戏.   版本：3.2.0",
            font=("SimHei", 12),
            wraplength=380,
            justify=CENTER
        ).place(relx=0.5, rely=0.3, anchor=CENTER)

        # 添加确认按钮
        Button(
            self.announcement_window,
            text="我已知晓",
            command=self.close_announcement,
            font=("SimHei", 12),
            width=15
        ).place(relx=0.5, rely=0.7, anchor=CENTER)

    def close_announcement(self):
        """关闭公告窗口"""
        self.announcement_window.destroy()

    def load_plant_info(self):
        """
        从文件中加载植物 ID 信息，并构建相关映射
        """
        with open('plant_id.txt', 'r', encoding="UTF-8") as file:
            # 在文件内容前添加空植物信息
            plant_info_text = "ID: -1, 空\n" + file.read()
        if plant_info_text[-1] == "\n":
            plant_info_text = plant_info_text[:-1]
        lines = plant_info_text.split("\n")
        # 存储 ID 到植物名称的映射
        self.id_to_name = {}
        # 存储植物名称到 ID 的映射
        self.name_to_id = {}
        # 存储 ID 到显示索引的映射
        self.id_to_display_index = {}
        # 存储显示用的植物信息列表
        self.display_plant_list = []

        for index, line in enumerate(lines):
            start_index = 4
            comma_index = line.find(",")
            plant_id = int(line[start_index:comma_index])
            self.id_to_display_index[plant_id] = index

        for line in lines:
            start_index = 4
            comma_index = line.find(",")
            plant_id = int(line[start_index:comma_index])
            plant_name = line[comma_index + 2:]
            display_text = f"{plant_id}:  {plant_name}"
            self.display_plant_list.append(display_text)
            self.id_to_name[plant_id] = plant_name
            self.name_to_id[display_text] = plant_id

        self.display_plant_tuple = tuple(self.display_plant_list)

    def init_config(self):
        """
        初始化配置文件，如果不存在则创建默认配置
        """
        self.config_path = "cfg"
        if not os.path.exists(self.config_path):
            self.save_config({
                'use_image': 1,
                'use_custom_path': 0,
                'auto_refresh': 0,
                'use_compatible_mode': 1
            })
        self.config = self.load_config()

    def load_config(self):
        """
        从配置文件中加载配置信息
        :return: 配置信息字典
        """
        with open(self.config_path, "r") as file:
            return json.load(file)

    def save_config(self, data):
        """
        将配置信息保存到文件中
        :param data: 配置信息字典
        """
        with open(self.config_path, "w") as file:
            json.dump(data, file)

    def pre_images(self):
        """
        预加载图片资源，用于加速界面显示
        """
        input_dir = './res/pre'

        output_dir = './res/'

        for filename in os.listdir(input_dir):
            if filename.endswith('.png'):
                input_path = os.path.join(input_dir, filename)
                try:
                    with Image.open(input_path) as img:
                        cropped_img = img.resize((30, 30))
                        output_path = os.path.join(output_dir + "0\\", filename)
                        cropped_img.save(output_path)
                        cropped_img = img.resize((45, 45))
                        output_path = os.path.join(output_dir + "1\\", filename)
                        cropped_img.save(output_path)
                        cropped_img = img.resize((60, 60))
                        output_path = os.path.join(output_dir + "2\\", filename)
                        cropped_img.save(output_path)
                        print(f"{filename} ok")
                except Exception as e:
                    print(f" {filename} : {e}")

    def load_images(self):
        """
        加载图片资源，如果加载失败则显示错误信息
        """
        self.use_image_mode = self.config["use_image"]
        self.images_size_0 = {}
        self.images_size_1 = {}
        self.images_size_2 = {}
        self.error_image = ImageTk.PhotoImage(Image.open(f"res//2//error.png").resize((60, 60)))
        for plant_id in self.id_to_name:
            try:
                image_size_0 = Image.open(f"res//0//{plant_id}.png")
                image_size_1 = Image.open(f"res//1//{plant_id}.png")
                image_size_2 = Image.open(f"res//2//{plant_id}.png")
                self.images_size_0[plant_id] = ImageTk.PhotoImage(image_size_0)
                self.images_size_1[plant_id] = ImageTk.PhotoImage(image_size_1)
                self.images_size_2[plant_id] = ImageTk.PhotoImage(image_size_2)
            except (TclError, FileNotFoundError) as e:
                ShowError(f"资源文件丢失 res//{plant_id}.png {self.id_to_name[plant_id]}", type(e), e)

    def create_menu(self):
        """
        创建菜单栏并添加菜单项
        """
        font.Font(name='font_1', family='Segoe UI', size=15,
                  weight='bold', slant='roman', underline=0, overstrike=0)

        menubar = Menu(self.root)

        def open_author_page():
            """
            打开作者的哔哩哔哩页面
            """
            import webbrowser
            webbrowser.open("https://space.bilibili.com/2016244084")

        menubar.add_command(label='点此关注up主Sh茗', command=open_author_page)
        menubar.add_command(label='交流群：1015660780', command=open_author_page)
        menubar.add_command(label='设置', command=self.open_settings_window)
        self.root.config(menu=menubar)

    def open_settings_window(self):
        """
        打开设置窗口，允许用户修改配置
        """
        settings_window = Toplevel(self.root)
        settings_window.title("设置")
        settings_window.geometry("300x200")

        use_custom_path_var = IntVar()
        custom_path_checkbox = Checkbutton(settings_window, indicatoron=True, text='使用自定义存档目录',
                                           variable=use_custom_path_var, bd=2)
        custom_path_checkbox.pack()
        use_custom_path_var.set(self.config["use_custom_path"])

        auto_refresh_var = IntVar()
        auto_refresh_checkbox = Checkbutton(settings_window, indicatoron=True, text='自动同步',
                                            variable=auto_refresh_var, bd=2)
        auto_refresh_checkbox.pack()
        auto_refresh_var.set(self.config["auto_refresh"])

        compatible_mode_var = IntVar()
        compatible_mode_checkbox = Checkbutton(settings_window, indicatoron=True, text='2.1.4兼容模式',
                                               variable=compatible_mode_var, bd=2)
        compatible_mode_checkbox.pack()
        compatible_mode_var.set(1 - self.config["use_compatible_mode"])

        def update_config():
            """
            更新配置信息并保存到文件
            """
            self.config["use_custom_path"] = use_custom_path_var.get()
            if use_custom_path_var.get():
                self.config["path"] = self.save_directory_path
            self.config["auto_refresh"] = auto_refresh_var.get()
            self.config["use_compatible_mode"] = 1 - compatible_mode_var.get()
            self.save_config(self.config)

        update_button = Button(settings_window, text='更新', command=update_config, bd=2)
        update_button.pack(pady=20)

    def create_widgets(self):
        """
        创建界面上的各种组件，如按钮、输入框、标签等
        """
        # 定义界面上的行位置（增加了行间距以容纳新增按钮）
        self.row_1 = 15
        self.row_2 = 55
        self.row_3 = 100
        self.row_4 = 135
        self.row_5 = 170
        self.row_6 = 205
        self.row_7 = 260
        self.row_8 = 300
        self.row_9 = 335
        self.row_10 = 395
        self.row_11 = 445
        self.row_12 = 485
        self.row_13 = 510
        self.row_14 = 550
        self.row_15 = 590
        self.separator = 50

        if self.config["use_custom_path"]:
            self.save_directory_path = self.config["path"]
        else:
            self.save_directory_path = f"C:/Users/{os.getenv('USERNAME')}/AppData/LocalLow/LanPiaoPiao/PlantsVsZombiesRH"
        self.garden_number = 0
        self.empty_plant = {"thePlantRow": None, "thePlantColumn": None, "thePlantType": -1, "growStage": 0,
                            "waterLevel": 0,
                            "love": 0, "nextTime": 11451419198, "needTool": 1, "page": 0}

        # 显示 ID 复选框变量
        self.show_id_var = IntVar()
        Checkbutton(indicatoron=True, text='显示 ID', variable=self.show_id_var).place(x=460, y=self.row_2, height=30,
                                                                                       width=100,
                                                                                       anchor='nw')
        # 显示成长状态复选框变量
        self.show_growth_status_var = IntVar()
        Checkbutton(indicatoron=True, text='显示成长状态', variable=self.show_growth_status_var).place(x=560,
                                                                                                       y=self.row_2,
                                                                                                       height=30,
                                                                                                       width=100,
                                                                                                       anchor='nw')
        self.show_growth_status_var.set(1)
        # 显示水分值复选框变量
        self.show_water_level_var = IntVar()
        Checkbutton(indicatoron=True, text='显示水分值', variable=self.show_water_level_var).place(x=665, y=self.row_2,
                                                                                                   height=30, width=100,
                                                                                                   anchor='nw')
        # 显示成长时间复选框变量
        self.show_growth_time_var = IntVar()
        Checkbutton(indicatoron=True, text='显示成长时间', variable=self.show_growth_time_var).place(x=765,
                                                                                                     y=self.row_2,
                                                                                                     height=30,
                                                                                                     width=100,
                                                                                                     anchor='nw')
        self.show_growth_time_var.set(1)
        # 图像模式复选框变量
        self.image_mode_var = IntVar()
        Checkbutton(indicatoron=True, text='图像模式（需要重启）', variable=self.image_mode_var).place(x=325,
                                                                                                     y=self.row_2,
                                                                                                     height=30,
                                                                                                     width=140,
                                                                                                     anchor='nw')
        self.image_mode_var.set(self.use_image_mode)

        # 游戏存档目录输入框
        self.save_directory_entry = Entry()
        self.save_directory_entry.place(x=603, y=self.row_1 + 5, height=21, width=499, anchor='ne')
        self.save_directory_entry.insert("0", self.save_directory_path)
        # 花园编号输入框
        self.garden_number_entry = Entry()
        self.garden_number_entry.place(x=115, y=self.row_2 + 5, height=20, width=36, anchor='nw')
        self.garden_number_entry.insert("0", "1")
        # 其他输入框
        self.water_level_entry = Entry()
        self.water_level_entry.place(x=self.separator + 645, y=self.row_5 + 5, height=20, width=36, anchor='nw')
        self.maturity_time_entry = Entry()
        self.maturity_time_entry.place(x=self.separator + 760, y=self.row_5 + 5, height=20, width=90, anchor='nw')
        self.plant_id_entry = Entry()
        self.plant_id_entry.place(x=self.separator + 559, y=self.row_4 + 5, height=20, width=51, anchor='nw')
        self.row_start_entry = Entry()
        self.row_start_entry.place(x=self.separator + 560, y=self.row_8 + 5, height=20, width=40, anchor='nw')
        self.row_end_entry = Entry()
        self.row_end_entry.place(x=self.separator + 630, y=self.row_8 + 5, height=20, width=40, anchor='nw')
        self.col_start_entry = Entry()
        self.col_start_entry.place(x=self.separator + 560, y=self.row_9 + 5, height=20, width=40, anchor='nw')
        self.col_end_entry = Entry()
        self.col_end_entry.place(x=self.separator + 630, y=self.row_9 + 5, height=20, width=40, anchor='nw')
        self.love_value_entry = Entry()
        self.love_value_entry.place(x=self.separator + 760, y=self.row_6 + 5, height=20, width=40, anchor='nw')

        # 各种标签
        Label(text='游戏存档目录').place(x=9, y=self.row_1, height=30, width=89, anchor='nw')
        Label(text='花园编号：').place(x=36, y=self.row_2, height=30, width=70, anchor='nw')
        self.plant_stack_label = Label(text='植物栈位：0')
        self.plant_stack_label.place(x=self.separator + 511, y=self.row_5, height=30, width=70, anchor='nw')
        Label(text='植物：').place(x=self.separator + 509, y=self.row_4, height=30, width=50, anchor='nw')
        Label(text='水分值：').place(x=self.separator + 588, y=self.row_5, height=30, width=47, anchor='nw')
        Label(text='成熟时间').place(x=self.separator + 690, y=self.row_5, height=30, width=65, anchor='nw')
        Label(text='大小：').place(x=self.separator + 510, y=self.row_6, height=30, width=40, anchor='nw')
        Label(font='font_1', text='修改植物').place(x=self.separator + 515, y=self.row_3, height=30, width=90,
                                                    anchor='nw')
        Label(text='下一工具：').place(x=self.separator + 600, y=self.row_6, height=30, width=70, anchor='nw')
        Label(text='成长值').place(x=self.separator + 710, y=self.row_6, height=30, width=50, anchor='nw')
        Label(font='font_1', text='批量操作').place(x=self.separator + 513, y=self.row_7, height=30, width=90,
                                                    anchor='nw')
        Label(font='font_1', text='快捷操作').place(x=self.separator + 512, y=self.row_10, height=30, width=90,
                                                    anchor='nw')
        Label(text='行').place(x=self.separator + 525, y=self.row_8, height=30, width=35, anchor='nw')
        Label(text='~').place(x=self.separator + 605, y=self.row_8, height=30, width=20, anchor='nw')
        Label(text='列').place(x=self.separator + 525, y=self.row_9, height=30, width=35, anchor='nw')
        Label(text='~').place(x=self.separator + 605, y=self.row_9, height=30, width=20, anchor='nw')

        # 存储植物选择按钮的列表
        self.plant_buttons = []
        # 存储每个按钮对应的植物数据索引
        self.plant_index_mapping = [None for _ in range(32)]
        # 当前选中的植物数据索引
        self.current_selected_index = None
        # 当前选中的按钮索引
        self.current_button_index = None

        # 存储按钮的坐标列表
        button_coordinates = []
        for row in range(4):
            for col in range(8):
                x_coord = col * 70
                y_coord = 110 + 100 * row
                button_coordinates.append((x_coord, y_coord))

        def create_plant_button(index):
            """
            创建植物选择按钮
            :param index: 按钮的索引
            """
            coord = button_coordinates[index]
            # 创建按钮，点击时调用 set_selected_index 方法
            button = Button(
                text=f"X: {coord[0]} Y: {coord[1]}",
                command=lambda idx=index: self.set_selected_index(idx)
            )
            button.place(x=coord[0], y=coord[1], height=90, width=70)
            self.plant_buttons.append(button)

        for button_index in range(32):
            create_plant_button(button_index)

        # 植物选择下拉框
        self.plant_combobox = ttk.Combobox()
        self.plant_combobox.place(x=self.separator + 610, y=self.row_4 + 5, height=20, width=188, anchor='nw')
        self.plant_combobox['value'] = self.display_plant_tuple
        self.plant_combobox.current(0)

        # 植物大小选择下拉框
        self.size_combobox = ttk.Combobox()
        self.size_combobox.place(x=self.separator + 545, y=self.row_6 + 5, height=20, width=60, anchor='nw')
        self.size_combobox['value'] = ("0(小)", "1(中)", "2(大)")
        self.size_combobox.current(0)

        # 下一工具选择下拉框
        self.tool_combobox = ttk.Combobox()
        self.tool_combobox.place(x=self.separator + 655, y=self.row_6 + 5, height=20, width=60, anchor='nw')
        self.tool_combobox['value'] = ("None", "水壶", "肥料", "杀虫剂", "唱片机")
        self.tool_combobox.current(1)

        # 各种按钮
        Button(text='选择', command=self.select_directory).place(x=609, y=self.row_1, height=30, width=55, anchor='nw')
        Button(text='自动加载', command=self.auto_load_directory).place(x=803, y=self.row_1, height=30, width=81,
                                                                        anchor='ne')
        Button(text='载入', command=self.load_directory).place(x=856, y=self.row_1, height=30, width=57, anchor='nw')
        Button(text='上一花园', command=self.prev_garden).place(x=165, y=self.row_2, height=31, width=72, anchor='nw')
        Button(text='下一花园', command=self.next_garden).place(x=241, y=self.row_2, height=30, width=70, anchor='nw')
        Button(text='一键长大', command=self.grow_all_plants).place(x=self.separator + 520, y=self.row_11, height=30,
                                                                    width=65, anchor='nw')
        Button(text='一键浇水', command=self.water_all_plants).place(x=self.separator + 590, y=self.row_11, height=30,
                                                                     width=65, anchor='nw')
        Button(text='跳过时间', command=self.skip_time).place(x=self.separator + 660, y=self.row_11, height=30,
                                                              width=65, anchor='nw')
        Button(text='无限时间', command=self.infinite_time).place(x=self.separator + 730, y=self.row_11, height=30,
                                                                  width=65, anchor='nw')
        Button(text='清空花园', command=self.clear_garden).place(x=self.separator + 805, y=self.row_11, height=30,
                                                                 width=65, anchor='nw')
        Button(text='替换/种植', command=self.replace_or_plant).place(x=self.separator + 700, y=self.row_9, height=30,
                                                                      width=80, anchor='nw')
        Button(text='重新加载', command=self.reload_data).place(x=self.separator + 630, y=self.row_3, height=30,
                                                                width=80, anchor='nw')
        Button(text='保存', command=self.save_data).place(x=self.separator + 800, y=self.row_3, height=30, width=50,
                                                          anchor='nw')
        Button(text='同步', command=self.sync_data).place(x=self.separator + 800, y=self.row_4, height=30, width=40,
                                                          anchor='nw')
        Button(text='一键全植物（不含花盆类）', command=self.all_plants).place(x=10, y=self.row_13, height=30, width=160,
                                                                             anchor='nw')
        Button(text='修复存档', command=self.fix_save).place(x=180, y=self.row_13, height=30, width=80, anchor='nw')
        Button(text='花园钱数加一亿', command=self.add_money).place(x=280, y=self.row_13, height=30, width=110,
                                                                    anchor='nw')
        Button(text='一键全成就', command=self.unlock_all_achievements).place(x=400, y=self.row_13, height=30, width=80,
                                                                              anchor='nw')
        Button(text="关注原创作者：B站 听雨夜荷", command=self.open_author_page1, bg='#FF6347', fg='white').place(x=10, y=self.row_14, height=30,
                                                                                       width=230, anchor='nw')
        Button(text="关注拓展作者：B站 Sh茗", command=self.open_author_page2, bg='#FF6347', fg='white').place(x=244, y=self.row_14, height=30,
                                                                                   width=190,
                                                                                   anchor='nw')
        Button(text='自定义叶绿素', command=self.customize_abyss_money, bg='#FF6347', fg='white').place(x=10, y=self.row_15, height=30,
                                                                              width=120, anchor='nw')
        Button(text='深渊关卡修改', command=self.modify_abyss_level, bg='#FF6347', fg='white').place(x=140, y=self.row_15, height=30,
                                                                           width=150, anchor='nw')
        Button(text='深渊植物升级', command=self.open_abyss_upgrade_window, bg='#FF6347', fg='white').place(x=300,
                                                                                                            y=self.row_15,
                                                                                                            height=30,
                                                                                                            width=120,
                                                                                                            anchor='nw')
        Button(text='深渊植物一键满级', command=self.maximize_abyss_plant_levels, bg='#FF6347', fg='white').place(x=430,
                                                                                                                  y=self.row_15,
                                                                                                                  height=30,
                                                                                                                  width=120,
                                                                                                                  anchor='nw')
        Button(text='格式化深渊植物等级', command=self.format_abyss_plant_levels, bg='#FF6347', fg='white').place(x=560,
                                                                                                                  y=self.row_15,
                                                                                                                  height=30,
                                                                                                                  width=160,
                                                                                                                  anchor='nw')
        Button(text='深渊词条刷新次数', command=self.open_refresh_count_window, bg='#FF6347', fg='white').place(x=730,
                                                                                                                  y=self.row_15,
                                                                                                                  height=30,
                                                                                                                  width=160,
                                                                                                                  anchor='nw')

    def open_author_page1(self):
        """
        关注原创作者：B站 听雨夜荷
        """
        import webbrowser
        webbrowser.open("https://space.bilibili.com/3537110030092294")

    def open_author_page2(self):
        """
        关注现作者：B站 Sh茗
        """
        import webbrowser
        webbrowser.open("https://space.bilibili.com/2016244084")

    def set_selected_index(self, index):
        """
        设置当前选中的按钮索引，并更新按钮状态
        :param index: 按钮的索引
        """
        for i in range(32):
            if i == index:
                self.plant_buttons[i]['state'] = 'disabled'
                self.plant_buttons[i]['relief'] = 'sunken'
            else:
                self.plant_buttons[i]['state'] = 'active'
                self.plant_buttons[i]['relief'] = 'raised'

        self.current_selected_index = self.plant_index_mapping[index]
        self.current_button_index = index

    def select_directory(self):
        """
        打开文件选择对话框，让用户选择游戏存档目录
        """
        path = filedialog.askdirectory(title='打开游戏存档目录', initialdir=self.save_directory_path)
        self.save_directory_entry.delete(0, "end")
        self.save_directory_entry.insert(0, path)

    def auto_load_directory(self):
        """
        根据配置自动加载游戏存档目录
        """
        if self.config["use_custom_path"]:
            path = self.config["path"]
        else:
            path = f"C:/Users/{os.getenv('USERNAME')}/AppData/LocalLow/LanPiaoPiao/PlantsVsZombiesRH"
        self.save_directory_entry.delete(0, "end")
        self.save_directory_entry.insert(0, path)

    def load_directory(self):
        """
        从输入框中获取游戏存档目录
        """
        self.save_directory_path = self.save_directory_entry.get()

    def prev_garden(self):
        """
        切换到上一个花园
        """
        current_number = int(self.garden_number_entry.get()) - 1
        if current_number == 0:
            current_number = 1
        self.garden_number_entry.delete(0, "end")
        self.garden_number_entry.insert(0, str(current_number))

    def next_garden(self):
        """
        切换到下一个花园
        """
        current_number = int(self.garden_number_entry.get()) + 1
        self.garden_number_entry.delete(0, "end")
        self.garden_number_entry.insert(0, str(current_number))

    def grow_all_plants(self):
        """
        让所有植物一键长大
        """
        for plant in self.plant_data['plantData']:
            plant['growStage'] = 2
            plant['love'] = 100
        self.save_garden_file(self.get_garden_file_path())
        self.reload_data()

    def water_all_plants(self):
        """
        让所有植物一键浇水
        """
        for plant in self.plant_data['plantData']:
            plant['waterLevel'] = 100
        self.save_garden_file(self.get_garden_file_path())
        self.reload_data()

    def skip_time(self):
        """
        让所有植物跳过成长时间
        """
        for plant in self.plant_data['plantData']:
            plant['nextTime'] = 2
        self.save_garden_file(self.get_garden_file_path())
        self.reload_data()

    def infinite_time(self):
        """
        让所有植物拥有无限成长时间
        """
        for plant in self.plant_data['plantData']:
            plant['nextTime'] = time.time() + 100000000
        self.save_garden_file(self.get_garden_file_path())
        self.reload_data()

    def clear_garden(self):
        """
        清空当前花园的存档文件
        """
        if askquestion(title="", message="确定删除？操作不可逆") == 'yes':
            os.remove(self.get_garden_file_path())
            self.reload_data()

    def replace_or_plant(self):
        """
        替换或种植植物
        """
        start_row = int(self.row_start_entry.get()) - 1
        end_row = int(self.row_end_entry.get())
        start_col = int(self.col_start_entry.get()) - 1
        end_col = int(self.col_end_entry.get())

        for row in range(start_row, end_row):
            for col in range(start_col, end_col):
                button_index = row * 8 + col
                existing_index = self.plant_index_mapping[button_index]

                new_plant = {
                    "thePlantRow": row,
                    "thePlantColumn": col,
                    "thePlantType": int(self.plant_id_entry.get()),
                    "growStage": {"0(小)": 0, "1(中)": 1, "2(大)": 2}[self.size_combobox.get()],
                    "waterLevel": int(self.water_level_entry.get()),
                    "love": int(self.love_value_entry.get()),
                    "nextTime": int(self.maturity_time_entry.get()[:-1]) + int(time.time()),
                    "needTool": {"None": 1, "null": 1, "水壶": 1, "肥料": 2, "杀虫剂": 3, "唱片机": 4}[
                        self.tool_combobox.get()],
                    "page": self.garden_number
                }

                if existing_index is not None:
                    self.plant_data['plantData'][existing_index] = new_plant
                else:
                    self.plant_data['plantData'].append(new_plant)

        self.save_garden_file(self.get_garden_file_path())
        self.load_buttons()
        self.reload_data()

    def get_garden_file_path(self):
        """
        根据花园编号获取对应的存档文件路径
        :return: 存档文件路径
        """
        if self.garden_number == 0:
            return self.save_directory_path + "/GardenData.json"
        return self.save_directory_path + "/GardenData" + str(self.garden_number) + ".json"

    def read_garden_file(self, path):
        """
        读取花园存档文件，如果文件不存在则创建
        :param path: 存档文件路径
        :return: 花园数据字典
        """
        try:
            with open(path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            directory = os.path.dirname(path)
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(path, "w") as file:
                json.dump({"plantData": []}, file)
            return {"plantData": []}

    def save_garden_file(self, path):
        """
        将花园数据保存到文件中
        :param path: 存档文件路径
        """
        with open(path, "w") as file:
            json.dump(self.plant_data, file)

    def load_buttons(self):
        """
        加载按钮信息，更新按钮的文本和图片
        """
        available_indices = [i for i in range(32)]
        for index, plant in enumerate(self.plant_data['plantData']):
            try:
                plant_id = plant['thePlantType']
                plant_name = self.id_to_name.get(plant_id, str(plant_id))
                row = int(plant['thePlantRow'])
                col = int(plant['thePlantColumn'])
                button_index = row * 8 + col

                info_parts = []
                if self.show_id_var.get():
                    info_parts.append(f"ID {plant_id}")
                info_parts.append(plant_name)
                if self.show_growth_status_var.get():
                    status_options = ("0(小)", "1(中)", "2(大)")
                    info_parts.append(status_options[int(plant["growStage"])])
                if self.show_water_level_var.get():
                    info_parts.append(f"水分 {plant['waterLevel']}")
                if self.show_growth_time_var.get():
                    remaining_time = max(int(float(plant['nextTime']) - time.time()), 0)
                    info_parts.append(f"{remaining_time}s")

                button_text = '\n'.join(info_parts)
                self.plant_index_mapping[button_index] = index

                try:
                    available_indices.remove(button_index)
                except ValueError as e:
                    ShowError("ValueError", e)

                try:
                    self.plant_buttons[button_index].config(text=button_text)
                    if self.use_image_mode:
                        size = plant["growStage"]
                        if size == 0:
                            self.plant_buttons[button_index].config(image=self.images_size_0[plant_id])
                        elif size == 1:
                            self.plant_buttons[button_index].config(image=self.images_size_1[plant_id])
                        elif size == 2:
                            self.plant_buttons[button_index].config(image=self.images_size_2[plant_id])
                except (TypeError, KeyError) as e:
                    if isinstance(e, TypeError):
                        ShowError("TypeError", e)
                    elif isinstance(e, KeyError):
                        ShowError("缺少贴图,", e)
                        if self.use_image_mode:
                            self.plant_buttons[button_index].config(image=self.error_image)
            except Exception as e:
                ShowError(type(e), e)

        for index in available_indices:
            self.plant_index_mapping[index] = None
            self.plant_buttons[index].config(text="空")
            if self.use_image_mode:
                self.plant_buttons[index].config(image=self.images_size_2[-1])

    def reload_data(self, first=True):
        """
        重新加载花园数据，并更新输入框和下拉框的值
        :param first: 是否是第一次加载
        """
        if self.current_selected_index is None:
            plant = self.empty_plant
        else:
            button_index = self.plant_index_mapping.index(self.current_selected_index)
            plant = self.plant_data['plantData'][self.current_selected_index]

        self.plant_id_entry.delete(0, "end")
        self.plant_id_entry.insert("0", plant["thePlantType"])
        self.water_level_entry.delete(0, "end")
        self.water_level_entry.insert("0", plant["waterLevel"])
        self.maturity_time_entry.delete(0, "end")
        self.love_value_entry.delete(0, "end")
        self.love_value_entry.insert("0", plant["love"])
        remaining_time = max(0, int(plant['nextTime'] - time.time()))
        self.maturity_time_entry.insert("0", str(remaining_time) + "s")
        self.plant_stack_label.config(text="植物栈位:" + str(self.current_selected_index))

        try:
            self.plant_combobox.current(self.id_to_display_index[int(plant['thePlantType'])])
        except:
            self.plant_combobox.current(self.id_to_display_index[0])

        self.size_combobox.current(int(plant['growStage']))
        self.tool_combobox.current(int(plant['needTool']))

    def save_data(self):
        """
        保存当前选中植物的修改信息
        """
        if self.current_selected_index is not None:
            plant = self.plant_data['plantData'][self.current_selected_index]

            plant["thePlantType"] = int(self.plant_id_entry.get())
            plant["waterLevel"] = int(self.water_level_entry.get())
            plant["love"] = int(self.love_value_entry.get())
            plant["nextTime"] = int(self.maturity_time_entry.get()[:-1]) + int(time.time())
            plant["growStage"] = {"0(小)": 0, "1(中)": 1, "2(大)": 2}[self.size_combobox.get()]
            plant["needTool"] = {"None": 1, "null": 1, "水壶": 1, "肥料": 2, "杀虫剂": 3, "唱片机": 4}[
                self.tool_combobox.get()]
            plant["waterLevel"] = int(self.water_level_entry.get())

            if plant["thePlantType"] == -1:
                del self.plant_data['plantData'][self.current_selected_index]
                self.current_selected_index = None
        else:
            new_plant = {
                "thePlantType": int(self.plant_id_entry.get()),
                "love": int(self.love_value_entry.get()),
                "nextTime": int(self.maturity_time_entry.get()[:-1]) + int(time.time()),
                "growStage": {"0(小)": 0, "1(中)": 1, "2(大)": 2}[self.size_combobox.get()],
                "waterLevel": int(self.water_level_entry.get()),
                "needTool": {"None": 1, "null": 1, "水壶": 1, "肥料": 2, "杀虫剂": 3, "唱片机": 4}[
                    self.tool_combobox.get()],
                "thePlantRow": self.current_button_index // 8,
                "thePlantColumn": self.current_button_index % 8,
                "page": int(self.garden_number_entry.get())
            }
            self.plant_data['plantData'].append(new_plant)

        self.save_garden_file(self.get_garden_file_path())
        self.reload_data()

    def sync_data(self):
        """
        同步下拉框选择的植物 ID 到输入框
        """
        self.plant_id_entry.delete(0, "end")
        self.plant_id_entry.insert("0", self.name_to_id[self.plant_combobox.get()])

    def all_plants(self):
        """
        执行一键全植物操作
        """
        os.system("copy.bat")

    def fix_save(self):
        """
        修复花园存档文件
        """
        index = 0
        while index < len(self.plant_data['plantData']):
            plant = self.plant_data['plantData'][index]
            try:
                plant["thePlantRow"] = int(plant["thePlantRow"])
                plant["thePlantColumn"] = int(plant["thePlantColumn"])
                plant["thePlantType"] = int(plant["thePlantType"])
                if plant["thePlantType"] == -1:
                    raise ValueError("unknown plant")
                plant["growStage"] = int(plant["growStage"]) % 3
                plant["waterLevel"] = int(plant["waterLevel"]) % 100
                plant["nextTime"] = max(int(plant["nextTime"]), int(time.time()))
                plant["needTool"] = int(plant["needTool"]) % 4
                if plant["needTool"] == 0:
                    plant["needTool"] = 1
                plant["page"] = self.garden_number
            except Exception as e:
                ShowError(e)
                del self.plant_data['plantData'][index]
            else:
                index += 1

        self.save_garden_file(self.get_garden_file_path())
        showinfo("", "修复完成！请重启修改器")

    def add_money(self):
        """
        给花园添加一亿金钱
        """
        player_data_path = self.save_directory_path + "/playerData.json"
        with open(player_data_path, "r") as file:
            data = json.load(file)
        data["theMoneyCount"] += 100000000
        with open(player_data_path, "w") as file:
            json.dump(data, file)
        showinfo("", "修改完成！可能需要重启游戏才能生效。建议关闭游戏后修改")

    def unlock_all_achievements(self):
        """
        解锁所有成就
        """
        player_data_path = self.save_directory_path + "/playerData.json"
        with open(player_data_path, "r") as file:
            data = json.load(file)
        data["achievements"] = [i for i in range(66)] + [999, 1000, 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008,
                                                         1009]
        with open(player_data_path, "w") as file:
            json.dump(data, file)
        showinfo("", "修改完成！可能需要重启游戏才能生效。建议关闭游戏后修改")

    def refresh(self):
        """
        刷新花园数据
        """
        if self.config["auto_refresh"]:
            self.sync_data()

        if self.use_image_mode != self.image_mode_var.get():
            self.use_image_mode = self.image_mode_var.get()
            self.config["use_image"] = self.use_image_mode
            self.save_config(self.config)
            showinfo("", "应用设置需要重启修改器")

        self.garden_number = int(self.garden_number_entry.get()) - 1
        self.plant_data = self.read_garden_file(self.get_garden_file_path())

        self.load_buttons()
        if self.last_selected_index != self.current_selected_index:
            self.reload_data()
        self.last_selected_index = self.current_selected_index

    def auto_refresh_loop(self):
        """
        自动刷新循环
        """
        while True:
            time.sleep(0.1)
            self.refresh()

    def load_garden_data(self):
        """
        加载花园数据并启动自动刷新线程
        """
        self.garden_number = int(self.garden_number_entry.get()) - 1
        self.plant_data = self.read_garden_file(self.get_garden_file_path())
        self.load_buttons()
        self.reload_data(False)

        # 使用threading模块创建和启动线程
        self.refresh_thread = threading.Thread(target=self.auto_refresh_loop, daemon=True)
        self.refresh_thread.start()

    def customize_abyss_money(self):
        """
        自定义深渊货币（叶绿素）功能
        """
        # 创建输入窗口
        self.money_window = Toplevel(self.root)
        self.money_window.title("自定义叶绿素")
        self.money_window.geometry("300x200")
        self.money_window.resizable(False, False)

        # 居中显示窗口
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 300) // 2
        y = (screen_height - 200) // 2
        self.money_window.geometry(f"+{x}+{y}")

        # 创建输入框和标签
        Label(self.money_window, text="请输入叶绿素数值（需要关闭游戏修改）:").pack(pady=20)

        self.money_entry = Entry(self.money_window, width=20, font=("Arial", 12))
        self.money_entry.pack(pady=10)
        self.money_entry.focus_set()  # 设置焦点到输入框

        # 绑定回车键事件
        self.money_entry.bind("<Return>", lambda event: self.update_abyss_money())

        # 创建按钮
        Button(self.money_window, text="确认修改", command=self.update_abyss_money, width=15, height=1).pack(pady=10)

        # 状态标签
        self.status_label = Label(self.money_window, text="", fg="red")
        self.status_label.pack(pady=5)

    def update_abyss_money(self):
        """
        获取用户输入，更新JSON文件中的abyssMoney字段
        """
        try:
            # 获取用户输入
            money_value = self.money_entry.get().strip()
            if not money_value:
                raise ValueError("输入不能为空")

            # 转换为整数
            money_value = int(money_value)
            if money_value < 0:
                raise ValueError("金额不能为负数")

            # 构建文件路径
            username = os.getenv('USERNAME')
            if not username:
                username = "Unknown"  # 如果无法获取用户名，使用默认值
            file_path = os.path.join(self.save_directory_path, "playerData.json")

            # 检查文件是否存在
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"文件不存在: {file_path}")

            # 读取JSON文件
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 更新abyssMoney字段
            if "abyssMoney" in data:
                original_value = data["abyssMoney"]
                data["abyssMoney"] = money_value
            else:
                raise KeyError("JSON文件中未找到abyssMoney字段")

            # 写入更新后的JSON文件
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            # 关闭窗口
            self.money_window.destroy()
            showinfo("", f"成功更新叶绿素为: {money_value}\n原数值: {original_value}，")

        except ValueError as e:
            self.status_label.config(text=f"错误: {str(e)}", fg="red")
        except FileNotFoundError as e:
            self.status_label.config(text=f"文件错误: {str(e)}", fg="red")
        except KeyError as e:
            self.status_label.config(text=f"JSON结构错误: {str(e)}", fg="red")
        except Exception as e:
            self.status_label.config(text=f"未知错误: {str(e)}", fg="red")

    # ===== 深渊关卡修改功能 =====
    def modify_abyss_level(self):
        """修改深渊关卡的功能"""
        # 创建输入窗口
        self.level_window = Toplevel(self.root)
        self.level_window.title("深渊关卡修改")
        self.level_window.geometry("300x200")
        self.level_window.resizable(False, False)

        # 居中显示窗口
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 300) // 2
        y = (screen_height - 200) // 2
        self.level_window.geometry(f"+{x}+{y}")

        # 显示当前深渊关卡
        current_level = self.get_current_abyss_level()
        current_level_label = Label(self.level_window, text=f"当前关卡: {current_level}")
        current_level_label.pack(pady=10)

        # 创建输入框和标签
        Label(self.level_window, text="请输入关卡数 (1-31):").pack(pady=10)

        self.level_entry = Entry(self.level_window, width=20, font=("Arial", 12))
        self.level_entry.pack(pady=10)
        self.level_entry.focus_set()  # 设置焦点到输入框

        # 绑定回车键事件
        self.level_entry.bind("<Return>", lambda event: self.update_abyss_level())

        # 创建按钮
        Button(self.level_window, text="确认修改", command=self.update_abyss_level, width=15, height=1).pack(pady=10)

        # 状态标签
        self.level_status_label = Label(self.level_window, text="", fg="red")
        self.level_status_label.pack(pady=5)

    def get_current_abyss_level(self):
        """获取当前深渊关卡数"""
        try:
            file_path = os.path.join(self.save_directory_path, "playerData.json")
            if not os.path.exists(file_path):
                return "未知"

            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if "abyssLevel" in data:
                return data["abyssLevel"]
            else:
                return "未知"
        except Exception as e:
            ShowError(f"获取当前深渊关卡失败: {e}")
            return "未知"

    def update_abyss_level(self):
        """更新深渊关卡数"""
        try:
            # 获取用户输入
            level_value = self.level_entry.get().strip()
            if not level_value:
                raise ValueError("输入不能为空")

            # 转换为整数
            level_value = int(level_value)
            if level_value < 1 or level_value > 31:
                raise ValueError("关卡数必须在1-31之间")

            # 构建文件路径
            file_path = os.path.join(self.save_directory_path, "playerData.json")

            # 检查文件是否存在
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"文件不存在: {file_path}")

            # 读取JSON文件
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 更新abyssLevel字段
            if "abyssLevel" in data:
                original_value = data["abyssLevel"]
                data["abyssLevel"] = level_value
            else:
                raise KeyError("JSON文件中未找到abyssLevel字段")

            # 写入更新后的JSON文件
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            # 关闭窗口
            self.level_window.destroy()
            showinfo("",
                     f"成功更新深渊关卡为: {level_value}\n原关卡: {original_value}，修改完成！可能需要重启游戏才能生效。建议关闭游戏后修改")

        except ValueError as e:
            self.level_status_label.config(text=f"错误: {str(e)}", fg="red")
        except FileNotFoundError as e:
            self.level_status_label.config(text=f"文件错误: {str(e)}", fg="red")
        except KeyError as e:
            self.level_status_label.config(text=f"JSON结构错误: {str(e)}", fg="red")
        except Exception as e:
            self.level_status_label.config(text=f"未知错误: {str(e)}", fg="red")

    def open_abyss_upgrade_window(self):
                """打开深渊植物升级窗口"""
                upgrade_window = Toplevel(self.root)
                upgrade_window.title("深渊植物升级")
                upgrade_window.geometry("300x200")

                # 植物 ID 输入框
                plant_id_label = Label(upgrade_window, text="植物 ID:")
                plant_id_label.pack()
                plant_id_entry = Entry(upgrade_window)
                plant_id_entry.pack()

                # 等级输入框
                level_label = Label(upgrade_window, text="等级（1~3）:")
                level_label.pack()
                level_entry = Entry(upgrade_window)
                level_entry.pack()

                # 修改按钮
                modify_button = Button(upgrade_window, text="修改",
                                       command=lambda: self.upgrade_abyss_plant(plant_id_entry.get(),
                                                                                level_entry.get()))
                modify_button.pack(pady=20)

    def upgrade_abyss_plant(self, plant_id, level):
        """更新深渊植物等级"""
        try:
            plant_id = int(plant_id)
            level = int(level)
        except ValueError:
            ShowError("输入的植物 ID 或等级必须为整数，等级为1~3")
            return

        # 构建文件路径
        player_data_path = f"C:/Users/{os.getenv('USERNAME')}/AppData/LocalLow/LanPiaoPiao/PlantsVsZombiesRH/playerData.json"

        try:
            # 读取文件
            with open(player_data_path, "r") as file:
                player_data = json.load(file)

            # 查找并更新深渊植物等级
            abyss_plant_levels = player_data.get("abyssPlantLevels", [])
            found = False
            for index, plant in enumerate(abyss_plant_levels):
                if plant["thePlantType"] == plant_id:
                    abyss_plant_levels[index]["level"] = level
                    found = True
                    break

            if not found:
                new_plant = {"thePlantType": plant_id, "level": level}
                abyss_plant_levels.append(new_plant)
                # 按植物 ID 排序
                abyss_plant_levels.sort(key=lambda x: x["thePlantType"])

            # 更新文件内容
            player_data["abyssPlantLevels"] = abyss_plant_levels

            # 保存更新后的文件
            with open(player_data_path, "w") as file:
                json.dump(player_data, file, indent=4)

            showinfo("成功", "深渊植物等级更新成功.请重启游戏。")
        except Exception as e:
            ShowError("更新失败", type(e), e)

    def maximize_abyss_plant_levels(self):
        """
        将深渊植物等级设置为满级
        """
        player_data_path = f"C:/Users/{os.getenv('USERNAME')}/AppData/LocalLow/LanPiaoPiao/PlantsVsZombiesRH/playerData.json"
        try:
            # 读取 playerData.json 文件
            with open(player_data_path, 'r', encoding='utf-8') as file:
                player_data = json.load(file)

            # 生成满级的深渊植物等级数据
            max_level_data = []
            plant_ids = [i for i in range(39)] + [234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247,
                                                  248, 249, 250, 251, 252, 253, 254, 255, 256, 300] + [i for i in
                                                                                                       range(900,
                                                                                                             952)] + [i
                                                                                                                      for
                                                                                                                      i
                                                                                                                      in
                                                                                                                      range(
                                                                                                                          1000,
                                                                                                                          1242)]
            for plant_id in plant_ids:
                max_level_data.append({"thePlantType": plant_id, "level": 3})

            # 更新 playerData 中的 abyssPlantLevels 字段
            player_data["abyssPlantLevels"] = max_level_data

            # 保存修改后的 playerData.json 文件
            with open(player_data_path, 'w', encoding='utf-8') as file:
                json.dump(player_data, file, indent=4)

            showinfo("提示", "深渊植物已全部设置为满级！，请重启游戏")
        except Exception as e:
            ShowError("修改深渊植物等级时出错", type(e), e)
            showerror("错误", f"修改深渊植物等级时出错：{str(e)}")

    def format_abyss_plant_levels(self):
        """
        格式化深渊植物等级
        """
        player_data_path = f"C:/Users/{os.getenv('USERNAME')}/AppData/LocalLow/LanPiaoPiao/PlantsVsZombiesRH/playerData.json"
        try:
            with open(player_data_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            data["abyssPlantLevels"] = []
            with open(player_data_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
            showinfo("成功", "深渊植物等级已格式化，请重启游戏")
        except FileNotFoundError:
            showerror("错误", "未找到 playerData.json 文件")
        except Exception as e:
            showerror("错误", f"发生未知错误: {e}")

    def open_refresh_count_window(self):
        """
        打开输入深渊词条刷新次数的窗口
        """
        self.refresh_count_window = Toplevel(self.root)
        self.refresh_count_window.title("深渊词条刷新次数")
        self.refresh_count_window.geometry("300x200")

        Label(self.refresh_count_window, text="请输入刷新次数:").pack(pady=10)
        self.refresh_count_entry = Entry(self.refresh_count_window)
        self.refresh_count_entry.pack(pady=5)

        Button(self.refresh_count_window, text="修改", command=self.modify_refresh_count).pack(pady=10)

    def modify_refresh_count(self):
        """
        修改playerData.json文件中的深渊词条刷新次数
        """
        try:
            count = int(self.refresh_count_entry.get())
            player_data_path = f"C:/Users/{os.getenv('USERNAME')}/AppData/LocalLow/LanPiaoPiao/PlantsVsZombiesRH/playerData.json"
            with open(player_data_path, 'r') as file:
                player_data = json.load(file)
            player_data["abyssRefreshCount"] = count
            with open(player_data_path, 'w') as file:
                json.dump(player_data, file)
            showinfo("成功", "深渊词条刷新次数修改成功！")
            self.refresh_count_window.destroy()
        except ValueError:
            showerror("错误", "请输入有效的整数！")
        except FileNotFoundError:
            showerror("错误", "未找到playerData.json文件！")


if __name__ == "__main__":
    root = Tk()
    app = GardenModifier(root)
    root.mainloop()