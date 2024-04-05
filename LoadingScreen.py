import tkinter as tk
import time, threading

class LoadingScreen:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("加载中...")
        self.parent.geometry("50x50")
        self.parent.overrideredirect(True)  # 移除标题栏
        self.parent.resizable(False, False)  # 设置窗口为不可调整大小
        # 设置窗口居中
        self.parent.geometry(
            f"+{int(self.parent.winfo_screenwidth() / 2 - 100)}+{int(self.parent.winfo_screenheight() / 2 - 100)}")

        self.canvas = tk.Canvas(self.parent, width=200, height=200)
        self.canvas.pack()
        self.progress_angle = 0
        self.progress_color = "red"

        self.draw_progress()

    def draw_progress(self):
        self.canvas.create_arc(0, 0, 50, 50, start=self.progress_angle, extent=360, fill=self.progress_color, width=2)
        self.progress_angle += 360 / 10  # 设置进度条完成的角度

        if self.progress_angle > 360:
            self.progress_angle = 0
            self.canvas.delete('all')  # 清空画布

        self.canvas.after(100, self.draw_progress)  # 每100毫秒更新一次


if __name__ == "__main__":
    root = tk.Tk()
    app = LoadingScreen(root)
    root.mainloop()

