#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
注册码验证器GUI应用程序
用于验证注册码并显示相关信息
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime
from cryptography.fernet import Fernet
from registration_generator import RegistrationGenerator


class RegistrationKeyValidatorGUI:
    """
    注册码验证器GUI界面
    """

    def __init__(self, master):
        """
        初始化注册码验证器GUI
        
        Args:
            master: Tk根窗口
        """
        self.master = master
        master.title("注册码验证器")
        master.geometry("600x500")
        master.resizable(True, True)

        self.storage_file = "license.dat"
        self.key_file = "license.key"
        # 使用与生成器相同的盐值以确保验证一致性
        self.generator = RegistrationGenerator(salt="default_salt_value_for_extra_security")
        self.cipher = None
        self.load_encryption_key()
        
        self.create_widgets()
        self.check_registration_status()

    def load_encryption_key(self):
        """
        加载加密密钥
        """
        if os.path.exists(self.key_file):
            try:
                with open(self.key_file, "rb") as f:
                    key = f.read()
                self.cipher = Fernet(key)
            except Exception as e:
                messagebox.showerror("错误", f"加载加密密钥失败: {str(e)}")
        else:
            # 如果密钥文件不存在，创建新的
            try:
                key = Fernet.generate_key()
                with open(self.key_file, "wb") as f:
                    f.write(key)
                self.cipher = Fernet(key)
            except Exception as e:
                messagebox.showerror("错误", f"创建加密密钥失败: {str(e)}")

    def create_widgets(self):
        """
        创建界面控件
        """
        # 主框架
        main_frame = ttk.Frame(self.master, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 标题
        title_label = ttk.Label(main_frame, text="注册码验证器", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))

        # 机器码显示区域
        machine_code_frame = ttk.LabelFrame(main_frame, text="本机机器码", padding="10")
        machine_code_frame.pack(fill=tk.X, pady=(0, 10))

        self.machine_code_var = tk.StringVar()
        machine_code_entry = ttk.Entry(machine_code_frame, textvariable=self.machine_code_var, 
                                      state="readonly", width=50)
        machine_code_entry.pack(fill=tk.X, pady=(0, 10))

        generate_mc_button = ttk.Button(machine_code_frame, text="生成本机机器码", command=self.generate_machine_code)
        generate_mc_button.pack(side=tk.LEFT)

        copy_mc_button = ttk.Button(machine_code_frame, text="复制机器码", command=self.copy_machine_code)
        copy_mc_button.pack(side=tk.LEFT, padx=(5, 0))

        # 注册码输入区域
        reg_key_frame = ttk.LabelFrame(main_frame, text="注册码输入", padding="10")
        reg_key_frame.pack(fill=tk.X, pady=(0, 10))

        self.reg_key_var = tk.StringVar()
        reg_key_entry = ttk.Entry(reg_key_frame, textvariable=self.reg_key_var, width=50)
        reg_key_entry.pack(fill=tk.X, pady=(0, 10))

        # 从文件加载按钮
        load_reg_button = ttk.Button(reg_key_frame, text="从文件加载注册码", command=self.load_registration_key_from_file)
        load_reg_button.pack(side=tk.LEFT)

        # 激活按钮
        activate_button = ttk.Button(reg_key_frame, text="激活注册码", command=self.activate_license)
        activate_button.pack(side=tk.LEFT, padx=(5, 0))

        # 注册信息显示区域
        info_frame = ttk.LabelFrame(main_frame, text="注册信息", padding="10")
        info_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # 创建信息显示表格
        info_table_frame = ttk.Frame(info_frame)
        info_table_frame.pack(fill=tk.BOTH, expand=True)

        # 机器码信息
        ttk.Label(info_table_frame, text="机器码:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.display_machine_code_var = tk.StringVar()
        ttk.Label(info_table_frame, textvariable=self.display_machine_code_var, 
                 wraplength=400, justify=tk.LEFT).grid(row=0, column=1, sticky=tk.W, pady=2)

        # 注册码信息
        ttk.Label(info_table_frame, text="注册码:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.display_reg_key_var = tk.StringVar()
        ttk.Label(info_table_frame, textvariable=self.display_reg_key_var, 
                 wraplength=400, justify=tk.LEFT).grid(row=1, column=1, sticky=tk.W, pady=2)

        # 到期时间信息
        ttk.Label(info_table_frame, text="到期时间:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.expiry_date_var = tk.StringVar()
        ttk.Label(info_table_frame, textvariable=self.expiry_date_var).grid(row=2, column=1, sticky=tk.W, pady=2)

        # 有效期信息
        ttk.Label(info_table_frame, text="有效期:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.validity_days_var = tk.StringVar()
        ttk.Label(info_table_frame, textvariable=self.validity_days_var).grid(row=3, column=1, sticky=tk.W, pady=2)

        # 剩余天数信息
        ttk.Label(info_table_frame, text="剩余天数:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.days_left_var = tk.StringVar()
        ttk.Label(info_table_frame, textvariable=self.days_left_var).grid(row=4, column=1, sticky=tk.W, pady=2)

        # 状态信息
        ttk.Label(info_table_frame, text="状态:").grid(row=5, column=0, sticky=tk.W, pady=2)
        self.status_var = tk.StringVar()
        ttk.Label(info_table_frame, textvariable=self.status_var, font=("Arial", 9, "bold")).grid(row=5, column=1, sticky=tk.W, pady=2)

        # 操作按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))

        clear_button = ttk.Button(button_frame, text="清空", command=self.clear_all)
        clear_button.pack(side=tk.LEFT)

        refresh_button = ttk.Button(button_frame, text="刷新状态", command=self.check_registration_status)
        refresh_button.pack(side=tk.LEFT, padx=(5, 0))

        # 状态栏
        self.status_bar_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(main_frame, textvariable=self.status_bar_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        # 初始化机器码
        self.generate_machine_code()

    def generate_machine_code(self):
        """
        生成本机机器码（基于硬件信息）
        """
        # 实际应用中应该收集真实的硬件信息
        import hashlib
        import uuid
        
        # 使用MAC地址和一些其他信息作为示例硬件信息
        mac = uuid.getnode()
        machine_code = hashlib.md5(str(mac).encode('utf-8')).hexdigest()
        self.machine_code_var.set(machine_code)

    def copy_machine_code(self):
        """
        复制机器码到剪贴板
        """
        machine_code = self.machine_code_var.get()
        if machine_code:
            self.master.clipboard_clear()
            self.master.clipboard_append(machine_code)
            messagebox.showinfo("提示", "机器码已复制到剪贴板")
        else:
            messagebox.showwarning("警告", "没有可复制的机器码")

    def load_registration_key_from_file(self):
        """
        从文件加载注册码
        """
        file_path = filedialog.askopenfilename(
            title="选择包含注册码的文件",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    reg_key = f.read().strip()
                    self.reg_key_var.set(reg_key)
                self.status_bar_var.set(f"已从文件加载注册码: {file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"读取文件失败: {str(e)}")

    def activate_license(self):
        """
        激活许可证
        """
        reg_key = self.reg_key_var.get().strip()
        machine_code = self.machine_code_var.get()
        
        if not reg_key:
            messagebox.showerror("错误", "请输入注册码")
            return
        
        if not self.cipher:
            messagebox.showerror("错误", "加密系统未初始化")
            return

        try:
            # 验证注册码
            verification_result = self.generator.verify_registration_key(reg_key)
            
            if not verification_result['valid']:
                error_msg = verification_result.get('message', '注册码验证失败')
                messagebox.showerror("错误", f"注册码验证失败: {error_msg}")
                return
                
            # 检查机器码是否匹配
            if verification_result['machine_code'] != machine_code:
                messagebox.showerror("错误", "注册码与本机机器码不匹配")
                return
            
            # 创建注册信息
            reg_info = {
                'registration_key': reg_key,
                'machine_code': machine_code,
                'expiry_date': verification_result['expiry_date'],
                'validity_days': verification_result['validity_days']
            }
            
            # 加密并保存注册信息
            json_data = json.dumps(reg_info)
            encrypted_data = self.cipher.encrypt(json_data.encode('utf-8'))
            
            with open(self.storage_file, "wb") as f:
                f.write(encrypted_data)
            
            messagebox.showinfo("提示", "注册信息已保存并激活")
            self.status_bar_var.set("注册信息已保存并激活")
            
            # 更新显示
            self.check_registration_status()
            
        except Exception as e:
            messagebox.showerror("错误", f"激活注册码失败: {str(e)}")

    def load_registration_info(self):
        """
        从本地文件加载并解密注册信息
        
        Returns:
            dict or None: 注册信息，如果文件不存在或解密失败则返回None
        """
        if not os.path.exists(self.storage_file) or not self.cipher:
            return None
            
        try:
            # 从文件读取加密数据
            with open(self.storage_file, "rb") as f:
                encrypted_data = f.read()
            
            # 解密数据
            decrypted_data = self.cipher.decrypt(encrypted_data)
            
            # 将JSON字符串转换为字典
            registration_info = json.loads(decrypted_data.decode('utf-8'))
            
            return registration_info
        except Exception:
            return None

    def check_registration_status(self):
        """
        检查并显示注册状态
        """
        registration_info = self.load_registration_info()
        
        if not registration_info:
            self.display_machine_code_var.set("无")
            self.display_reg_key_var.set("无")
            self.expiry_date_var.set("无")
            self.validity_days_var.set("无")
            self.days_left_var.set("无")
            self.status_var.set("未激活")
            return
        
        # 显示注册信息
        machine_code = registration_info.get('machine_code', '无')
        reg_key = registration_info.get('registration_key', '无')
        expiry_date_str = registration_info.get('expiry_date', '无')
        validity_days = registration_info.get('validity_days', '无')
        
        self.display_machine_code_var.set(machine_code)
        self.display_reg_key_var.set(reg_key)
        self.expiry_date_var.set(expiry_date_str)
        self.validity_days_var.set(f"{validity_days} 天" if validity_days != '无' else '无')
        
        # 检查机器码是否匹配
        local_machine_code = self.machine_code_var.get()
        if machine_code != local_machine_code:
            self.status_var.set("机器码不匹配")
            self.days_left_var.set("无效")
            return
        
        # 检查是否过期
        if expiry_date_str and expiry_date_str != '无':
            try:
                expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d")
                current_date = datetime.now()
                
                if current_date > expiry_date:
                    self.days_left_var.set("已过期")
                    self.status_var.set("已过期")
                else:
                    days_left = (expiry_date - current_date).days
                    self.days_left_var.set(str(days_left))
                    self.status_var.set("有效")
            except Exception as e:
                self.days_left_var.set("无效日期")
                self.status_var.set("信息错误")
        else:
            self.days_left_var.set("无")
            self.status_var.set("信息不完整")

    def clear_all(self):
        """
        清空所有输入
        """
        self.reg_key_var.set("")
        self.status_bar_var.set("已清空")


def main():
    """
    主函数
    """
    root = tk.Tk()
    app = RegistrationKeyValidatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()