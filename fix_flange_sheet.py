# 修复FlangeSheet.py文件中的重复行问题

with open('FlangeSheet.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 检查最后两行是否都是sys.exit(app.exec_())
if len(lines) >= 2 and lines[-1].strip() == 'sys.exit(app.exec_())' and lines[-2].strip() == 'sys.exit(app.exec_())':
    # 删除最后一行
    lines = lines[:-1]

# 写回文件
with open('FlangeSheet.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("修复完成")