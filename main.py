import tkinter as tk
import subprocess

# Chạy file in_gate.py
def run_in_gate():
    subprocess.run(["python", "in_gate.py"])

# Chạy file out_gate.py
def run_out_gate():
    subprocess.run(["python", "out_gate.py"])

# Hiển thị giao diện
root = tk.Tk()
root.title("Giả lập hệ thống bãi xe")

in_button = tk.Button(root, text="Cổng vào", command=run_in_gate, width=20, height=2)
in_button.pack(pady=10)

out_button = tk.Button(root, text="Cổng ra", command=run_out_gate, width=20, height=2)
out_button.pack(pady=10)

root.mainloop()
