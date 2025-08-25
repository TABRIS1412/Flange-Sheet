import os
import sys
import subprocess
import shutil

def build_flangesheet():
    """
    将FlangeSheet.py打包成独立的可执行文件
    """
    print("开始打包FlangeSheet应用程序...")
    
    # 确保在正确的目录中
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # 创建dist和build目录（如果不存在）
    if not os.path.exists("dist"):
        os.makedirs("dist")
    if not os.path.exists("build"):
        os.makedirs("build")
    
    # 构建基础命令
    cmd = [
        "pyinstaller",
        "--noconfirm",  # 不提示确认
        "--onefile",    # 打包成单个文件
        "--windowed",   # Windows下不显示控制台窗口
        "--icon=fla_256.ico",  # 应用程序图标
        "--name=FlangeSheet",  # 可用文件名称
        "--add-data=Data;Data",  # 添加Data目录
        "--add-data=flangeWindow.py;.",  # 添加flangeWindow.py文件
        "--add-data=flangeWindow.ui;.",  # 添加UI文件
        "--add-data=img;img",  # 添加img目录
        "--hidden-import=registration_generator",
        "--hidden-import=registration_key_validator",
        "--hidden-import=registration_key_generator",
        "--hidden-import=flangeWindow",
        "FlangeSheet.py"
    ]
    
    # 只有当文件存在时才添加它们
    if os.path.exists("license.key"):
        cmd.extend(["--add-data=license.key;."])
    
    if os.path.exists("license.dat"):
        cmd.extend(["--add-data=license.dat;."])
    
    if os.path.exists("img_source_rc.py"):
        cmd.extend(["--add-data=img_source_rc.py;."])
    
    print("执行命令:", " ".join(cmd))
    
    try:
        # 执行PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("打包成功完成!")
        print("可执行文件位置: dist/FlangeSheet.exe")
        return True
    except subprocess.CalledProcessError as e:
        print("打包失败:")
        print("错误输出:", e.stderr)
        return False
    except Exception as e:
        print("发生错误:", str(e))
        return False

if __name__ == "__main__":
    success = build_flangesheet()
    if success:
        print("\n打包完成，可执行文件位于 dist/FlangeSheet.exe")
    else:
        print("\n打包失败，请检查错误信息")
        sys.exit(1)