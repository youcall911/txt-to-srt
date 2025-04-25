#首先使用华为电脑管家-控制中心-智慧语音-AI字幕，先把视频听一遍，然后导出字幕到txt文件。打开txt文件，修复错别字，编辑每行的内容。再运行此脚本，选择刚才修改好的txt，保存为srt文件。最后在剪映里导入本地字幕。
#在第69行，可以修改每分钟朗读的字数，默认230个字。
#我用的是python3.10.9


import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from datetime import datetime, timedelta

# 创建主窗口
root = tk.Tk()
root.title("读取 TXT 文件并估算朗读时间")

# 设置窗口大小和位置
window_width = 600
window_height = 800
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = int((screen_width / 2) - (window_width / 2))
y_coordinate = int((screen_height / 2) - (window_height / 2))
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

# 创建一个可滚动的文本区域用于显示文件内容
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20)
text_area.pack(padx=10, pady=10)

# 创建一个可滚动的文本区域用于显示结果
result_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=15)
result_area.pack(padx=10, pady=10)

# 打开文件选择对话框
file_path = filedialog.askopenfilename(
    title="选择 TXT 文件",
    filetypes=[("TXT 文件", "*.txt"), ("所有文件", "*.*")]
)

# 如果用户选择了文件
if file_path:
    try:
        # 打开并读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # 清空文本框并显示文件内容
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, content)

        # 估算朗读时间并计算累计时间
        lines = content.split('\n')
        total_chars = 0
        cumulative_time = 0  # 累计时间（毫秒）
        result = ""
        subtitle_index = 1  # 字幕编号

        def format_time(milliseconds):
            # 将毫秒转换为字幕时间格式
            time_delta = timedelta(milliseconds=milliseconds)
            hours = time_delta.seconds // 3600
            minutes = (time_delta.seconds // 60) % 60
            seconds = time_delta.seconds % 60
            milliseconds = time_delta.microseconds // 1000
            return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

        for i, line in enumerate(lines):
            line = line.strip()  # 去除行首尾的空白字符
            if not line:  # 跳过空行
                continue
            line_chars = len(line)
            total_chars += line_chars
            # 转换为毫秒（每行朗读时间）
            estimated_seconds = round((line_chars / 230) * 60) #每分钟读230个字
            estimated_milliseconds = estimated_seconds * 1000
            start_time = cumulative_time
            end_time = cumulative_time + estimated_milliseconds
            cumulative_time = end_time

            # 格式化为字幕格式
            time_stamp = f"{format_time(start_time)} --> {format_time(end_time)}"
            result += f"{subtitle_index}\n{time_stamp}\n{line}\n\n"
            subtitle_index += 1  # 增加字幕编号

        # 显示估算结果
        result_area.delete(1.0, tk.END)
        result_area.insert(tk.END, result)

        # 添加保存功能
        def save_subtitle():
            save_path = filedialog.asksaveasfilename(
                defaultextension=".srt",
                filetypes=[("字幕文件", "*.srt"), ("所有文件", "*.*")],
                title="保存字幕文件"
            )
            if save_path:
                with open(save_path, 'w', encoding='utf-8') as file:
                    file.write(result)
                messagebox.showinfo("保存成功", f"字幕文件已保存到: {save_path}")

        # 创建保存按钮
        save_button = tk.Button(root, text="保存字幕", command=save_subtitle)
        save_button.pack(pady=10)

    except Exception as e:
        tk.messagebox.showerror("错误", f"读取文件时出错: {e}")

# 运行主循环
root.mainloop()