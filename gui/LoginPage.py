# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox,PhotoImage
from gui.MenuPage import menu_page
from log.LogSql import log_input
from tkinter import ttk
from PIL import Image, ImageTk
from login import Login
from menu.UserOption import bg_color, update_combobox
from picture.VersionInformation import version

def login_page():
    root = tk.Tk()
    # 设置标题
    root.title("GeekTest登录")
    # 设置窗口不可改变大小
    root.resizable(False, False)
    # 设置窗口图标
    icon_path = "picture/xmind.png"
    icon_image = PhotoImage(file=icon_path)
    root.iconphoto(True, icon_image)

    root.option_add('*TCombobox*Listbox*Font', ('Helvetica Neue', 11))

    # 设置窗口大小和位置
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 600
    window_height = 440
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    root.geometry(f'{window_width}x{window_height}+{x}+{y}')

    container = tk.Frame(root, bg="#f0f0f0", padx=0, pady=0)
    container.pack(fill=tk.BOTH, expand=True)

    # 标题部分
    title_frame = tk.Frame(container, bg="#0c1622", pady=10)
    title_frame.pack(fill=tk.X)
    title_label = tk.Label(title_frame, text="GeekTest登录", font=("Helvetica Neue", 30, "bold"), fg="white", bg="#0c1622",
                           padx=15)
    title_label.pack(side=tk.LEFT)

    # 账号输入部分
    username_var = tk.StringVar(root)
    username_var.set('刘正晗')
    username_frame = tk.Frame(container, bg="white", pady=25)
    username_frame.pack(pady=(40, 0))
    username_label = tk.Label(username_frame, text="禅道用户:", font=("Helvetica Neue", 14), bg="white", padx=16)
    username_label.pack(side=tk.LEFT)

    username_combobox = ttk.Combobox(username_frame, textvariable=username_var, values=Login.qa_list, width=28,
                                     font=("Helvetica Neue", 14),state='readonly')
    username_combobox.pack(fill=tk.X, expand=True, padx=(10, 10), pady=0)
    username_combobox.config(justify='center')
    username_combobox.timer_id = None
    username_combobox.bind('<KeyRelease>', lambda event: update_combobox(event, Login.qa_list))
    username_combobox.event_generate('<Button-1>')
    # 密码输入部分
    password_frame = tk.Frame(container, bg="white", pady=25)
    password_frame.pack(pady=0)
    password_label = tk.Label(password_frame, text="禅道密码:", font=("Helvetica Neue", 13), bg="white", padx=1)
    password_label.grid(row=0, column=0, sticky=tk.W, padx=(16, 12))
    password_entry = tk.Entry(password_frame, show="*", width=26, font=("Helvetica Neue", 16), bd=2, relief='groove')
    password_entry.grid(row=0, column=1, sticky=tk.W + tk.E, padx=(14, 14), pady=2)

    # 加载图片
    def load_resized_image(image_path, size):
        original_image = Image.open(image_path)
        resized_image = original_image.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(resized_image)

    show_password_var = tk.BooleanVar(value=False)
    show_image = load_resized_image("picture/zhanshi.png", (24, 24))
    hide_image = load_resized_image("picture/yingcang.png", (24, 24))
    # 使用图片创建按钮
    show_password_button = tk.Button(password_frame, image=show_image,
                                     command=lambda: toggle_password(password_entry, show_password_button,
                                                                     show_password_var, show_image, hide_image))
    show_password_button.grid(row=0, column=1, sticky=tk.E, padx=(0, 10))

    # 修改toggle_password函数以处理图片切换
    def toggle_password(entry, button, var, show_image, hide_image):
        if var.get():
            entry.config(show="")
            button.config(image=hide_image)
        else:
            entry.config(show="*")
            button.config(image=show_image)
        var.set(not var.get())

    # 提交按钮
    submit_button = ttk.Button(container, text="登 录")
    submit_button.pack(pady=50)
    submit_button.config(command=lambda: submit_credentials(username_var, password_entry))

    # 为根窗口绑定回车键事件
    def on_return_key(event):
        if password_entry==password_entry.focus_get():  # 检查焦点是否在密码输入框上
            submit_button.invoke()  # 触发提交按钮的点击事件

    root.bind("<Return>", on_return_key)  # 绑定回车键事件

    # 点击登录后的处理
    def submit_credentials(username_var, password_entry):
        username = username_var.get()
        password = password_entry.get()

        if Login.login_verify(username, password) == 1:
            messagebox.showerror("错误", "密码不能为空！",icon="error")
        elif Login.login_verify(username, password) == 0:
            messagebox.showinfo("成功", f"{username},恭喜您登录成功!")
            #版本号修改
            log_input(username, 'Login', f'{username}登录系统,版本号为:{version()}')
            root.withdraw()
            password_entry.delete(0, tk.END)
            menu_page(root, username)
        else:
            messagebox.showerror("错误", "禅道密码错误！",icon="error")

    root.mainloop()
