import requests
from bs4 import BeautifulSoup
import time
import tkinter as tk
from tkinter import messagebox
import threading

is_running = False  # 初始状态为暂停
student_no = None  # 初始学号为空

def login_spider():
    global is_running, student_no
    if not student_no:
        messagebox.showerror("错误", "请输入学号")
        return

    url = 'http://cc.szpu.edu.cn/sSign.aspx'
    session = requests.Session()

    while is_running:
        try:
            response = session.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            head = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"}

            # 获取隐藏字段
            viewstate = soup.find(id="__VIEWSTATE")['value']
            viewstategenerator = soup.find(id="__VIEWSTATEGENERATOR")['value']
            eventvalidation = soup.find(id="__EVENTVALIDATION")['value']

            payload = {
                'TextBoxStudentNo': student_no,
                '__VIEWSTATE': viewstate,
                '__VIEWSTATEGENERATOR': viewstategenerator,
                '__EVENTVALIDATION': eventvalidation,
                'ButtonSign': '提交'
            }

            resp = session.post(url, data=payload, headers=head)

            # 判断是否登录成功
            if '成功' in resp.text:
                messagebox.showinfo("成功", "签到成功！")
                break
            else:
                time.sleep(0.2)
        except Exception as e:
            print("trying")

# 启动签到线程
def start_spider():
    global is_running, student_no
    student_no = student_no_entry.get()  # 获取输入框中的学号
    if not student_no:
        messagebox.showerror("错误", "请输入学号")
        return
    if not is_running:
        is_running = True
        threading.Thread(target=login_spider, daemon=True).start()
        messagebox.showinfo(title="请求开始",message="请求开始")

# 停止签到
def stop_spider():
    global is_running
    is_running = False
    messagebox.showinfo(title="请求已暂停",message="请求已暂停")

root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
position_top = int(height // 2)
position_right = int(width // 2)
root.geometry(f'{250}x{200}+{position_right}+{position_top}')
root.title("cc网自动签到")

# 学号输入框
tk.Label(root, text="学号:").pack()
student_no_entry = tk.Entry(root)
student_no_entry.pack(pady=5)

# 开始签到按钮
start_button = tk.Button(root, text="开始请求", command=start_spider)
start_button.pack(pady=10)

# 暂停按钮
pause_button = tk.Button(root, text="暂停请求", command=stop_spider)
pause_button.pack(pady=10)

root.mainloop()
