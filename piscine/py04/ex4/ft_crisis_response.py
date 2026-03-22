def main() -> None:
    print("== CYBER ARCHIVES - CRISIS RESPONSE SYSTEM ===")
    print()
    # ========== 场景 1: 文件不存在 ==========
    print('CRISIS ALERT: Attempting access to "lost_archive.txt"...')
    try:
        with open('lost_archive.txt', 'r') as f:
            f.read()
    except FileNotFoundError:
        print('RESPONSE: Archive not found in storage matrix')
        print('STATUS: Crisis handled, system stable')
    # ========== 场景 2: 权限错误 ==========
    print()
    print('CRISIS ALERT: Attempting access to "classified_data.txt"...')
    try:
        with open('classified_data.txt', 'r') as f:
            f.read()
    except PermissionError:
        print('RESPONSE: Security protocols deny access')
        print('STATUS: Crisis handled, security maintained')
    # ========== 场景 3: 正常访问 ==========
    print()
    print('ROUTINE ACCESS: Attempting access to "standard_archive.txt"...')
    try:
        with open('standard_archive.txt', 'r') as f:
            data = f.read().strip()
        print(f'SUCCESS: Archive recovered - "{data}"')
        print('STATUS: Normal operations resumed')
    except Exception:
        print('STATUS: Crisis handled')
    print()
    print('All crisis scenarios handled successfully. Archives secure.')


if __name__ == "__main__":
    main()

# !!!!!!! the tester has some problems no file+ access
# !!!!!!! chmod -r classified_data.txt
# 1. 什么是 Failsafe Protocols（故障安全协议）？
# Failsafe = 故障安全，意思是"即使失败了也是安全的"
# Failsafe Protocols 的核心原则：
# [优雅降级（Graceful Degradation）
# try:
#     高精度操作()
# except:
#     低精度但安全的替代方案()  # 即使失败也能工作
# [自动恢复（Automatic Recovery）]
# python
# with open("data.txt", "r") as f:  # 获取资源
#     process(f)                    # 使用
# # 自动：释放资源 ← 恢复系统状态
# [隔离故障（Fault Isolation）]
# python
# try:
#     危险操作()
# except SpecificError:  # 只捕获特定错误
#     处理这个错误()
# # 其他错误还是会正常崩溃，防止隐藏真正问题
# 2. Failsafe Protocol 在这里是指 with + try/except 吗？
# 层次1：with 语句（资源安全）
# 层次2：try/except（错误处理）
# 3. 核心逻辑
# 真实世界：
# 文件可能不存在
# 权限可能不足
# 内容可能损坏
# 👉 程序不能死
# 4.
# .read().strip() 为什么需要 .strip()？
# .strip() 的作用：移除字符串开头和结尾的空白字符（空格、换行符、制表符等）。
# 在类 Unix 系统（Linux / macOS）里：一个“规范的文本文件”应该以 \n 结尾
# data_generator 生成的文件几乎一定带结尾 \n
# write() 不会帮你自动换行，你必须自己加 \n

