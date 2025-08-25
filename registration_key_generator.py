#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
注册码生成器GUI应用程序
用于根据机器码生成带有效期的注册码
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import hashlib
from datetime import datetime, timedelta
from registration_generator import RegistrationGenerator


class RegistrationKeyGeneratorGUI:
    """
    注册码生成器GUI界面
    """

    def __init__(self, master):
        """
        初始化注册码生成器GUI
        
        Args:
            master: Tk根窗口
        """
        self.master = master
        master.title("注册码生成器")
        master.geometry("600x400")
        master.resizable(True, True)

        self.generator = RegistrationGenerator()
        self.create_widgets()

    def create_widgets(self):
        """
        创建界面控件
        """
        # 主框架
        main_frame = ttk.Frame(self.master, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 标题
        title_label = ttk.Label(main_frame, text="注册码生成器", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))

        # 机器码输入区域
        machine_code_frame = ttk.LabelFrame(main_frame, text="机器码输入", padding="10")
        machine_code_frame.pack(fill=tk.X, pady=(0, 10))

        self.machine_code_var = tk.StringVar()
        machine_code_entry = ttk.Entry(machine_code_frame, textvariable=self.machine_code_var, width=50)
        machine_code_entry.pack(fill=tk.X, pady=(0, 10))

        # 从文件加载按钮
        load_button = ttk.Button(machine_code_frame, text="从文件加载机器码", command=self.load_machine_code_from_file)
        load_button.pack(side=tk.LEFT)

        # 有效期设置区域
        validity_frame = ttk.LabelFrame(main_frame, text="有效期设置", padding="10")
        validity_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(validity_frame, text="有效期:").pack(side=tk.LEFT)

        # 有效期数值
        self.validity_amount_var = tk.StringVar(value="12")
        validity_amount_spinbox = ttk.Spinbox(validity_frame, from_=1, to=120, width=5, 
                                             textvariable=self.validity_amount_var)
        validity_amount_spinbox.pack(side=tk.LEFT, padx=(5, 0))

        # 有效期单位
        self.validity_unit_var = tk.StringVar(value="月")
        validity_unit_combo = ttk.Combobox(validity_frame, textvariable=self.validity_unit_var,
                                          values=["天", "月", "年"], width=5, state="readonly")
        validity_unit_combo.pack(side=tk.LEFT, padx=(5, 0))

        # 生成按钮
        generate_button = ttk.Button(main_frame, text="生成注册码", command=self.generate_registration_key)
        generate_button.pack(pady=(0, 10))

        # 注册码显示区域
        reg_key_frame = ttk.LabelFrame(main_frame, text="生成的注册码", padding="10")
        reg_key_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.reg_key_var = tk.StringVar()
        reg_key_text = tk.Text(reg_key_frame, height=4, wrap=tk.WORD)
        reg_key_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.reg_key_text_widget = reg_key_text

        # 操作按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)

        copy_button = ttk.Button(button_frame, text="复制注册码", command=self.copy_registration_key)
        copy_button.pack(side=tk.LEFT, padx=(0, 5))

        save_button = ttk.Button(button_frame, text="保存到文件", command=self.save_registration_key_to_file)
        save_button.pack(side=tk.LEFT, padx=(0, 5))

        clear_button = ttk.Button(button_frame, text="清空", command=self.clear_all)
        clear_button.pack(side=tk.LEFT)

        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    def load_machine_code_from_file(self):
        """
        从文件加载机器码
        """
        file_path = filedialog.askopenfilename(
            title="选择包含机器码的文件",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    machine_code = f.read().strip()
                    self.machine_code_var.set(machine_code)
                self.status_var.set(f"已从文件加载机器码: {file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"读取文件失败: {str(e)}")

    def generate_registration_key(self):
        """
        生成注册码
        """
        machine_code = self.machine_code_var.get().strip()
        
        if not machine_code:
            messagebox.showerror("错误", "请输入机器码")
            return
        
        # 获取有效期设置
        try:
            amount = int(self.validity_amount_var.get())
            unit = self.validity_unit_var.get()
            
            # 转换为天数
            if unit == "天":
                validity_days = amount
            elif unit == "月":
                validity_days = amount * 30
            elif unit == "年":
                validity_days = amount * 365
            else:
                validity_days = 365  # 默认1年
                
        except ValueError:
            messagebox.showerror("错误", "请输入有效的时间数值")
            return

        try:
            # 生成可验证的注册码
            verifiable_key = self.generator.create_verifiable_registration_key(machine_code, validity_days)
            
            # 显示注册码
            self.reg_key_text_widget.delete(1.0, tk.END)
            self.reg_key_text_widget.insert(tk.END, verifiable_key)
            
            # 显示到期时间和有效期信息
            expiry_date = (datetime.now() + timedelta(days=validity_days)).strftime("%Y-%m-%d")
            self.status_var.set(f"注册码生成成功，有效期: {amount}{unit}，到期时间: {expiry_date}")
            
        except Exception as e:
            messagebox.showerror("错误", f"生成注册码失败: {str(e)}")

    def copy_registration_key(self):
        """
        复制注册码到剪贴板
        """
        reg_key = self.reg_key_text_widget.get(1.0, tk.END).strip()
        if reg_key:
            self.master.clipboard_clear()
            self.master.clipboard_append(reg_key)
            messagebox.showinfo("提示", "注册码已复制到剪贴板")
        else:
            messagebox.showwarning("警告", "没有可复制的注册码")

    def save_registration_key_to_file(self):
        """
        保存注册码到文件
        """
        reg_key = self.reg_key_text_widget.get(1.0, tk.END).strip()
        if not reg_key:
            messagebox.showwarning("警告", "没有可保存的注册码")
            return

        file_path = filedialog.asksaveasfilename(
            title="保存注册码到文件",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(reg_key)
                messagebox.showinfo("提示", f"注册码已保存到: {file_path}")
                self.status_var.set(f"注册码已保存到: {file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"保存文件失败: {str(e)}")

    def clear_all(self):
        """
        清空所有输入和输出
        """
        self.machine_code_var.set("")
        self.reg_key_text_widget.delete(1.0, tk.END)
        self.status_var.set("已清空")


def main():
    """
    主函数
    """
    root = tk.Tk()
    app = RegistrationKeyGeneratorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()