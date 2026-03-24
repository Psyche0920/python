def main() -> None:
    """Create a new archive file with preservation entries."""
    print("=== CYBER ARCHIVES - PRESERVATION SYSTEM ===\n")
    print("Initializing new storage unit: new_discovery.txt")

    # 使用with语句安全地创建和写入文件
    with open('new_discovery.txt', 'w') as archive:
        print("Storage unit created successfully...\n")
        print("Inscribing preservation data...")

        # 写入第一行数据并显示
        archive.write("[ENTRY 001] New quantum algorithm discovered\n")
        print("[ENTRY 001] New quantum algorithm discovered")

        # 写入第二行数据并显示
        archive.write("[ENTRY 002] Efficiency increased by 347%\n")
        print("[ENTRY 002] Efficiency increased by 347%")

        # 写入第三行数据并显示
        archive.write("[ENTRY 003] Archived by Data Archivist trainee\n")
        print("[ENTRY 003] Archived by Data Archivist trainee\n")

    # 文件自动关闭后打印完成消息
    print("Data inscription complete. Storage unit sealed.")
    print("Archive 'new_discovery.txt' ready for long-term preservation.")


if __name__ == "__main__":
    main()


# 1. with open(...) as f: = open() + 自动close() + 异常安全保证
# 文件对象 (f)
#         文件名	              文件对象 (f)
# 类型	   字符串（str）	       文件对象（file object）
# 包含什么	只是名字，如 "test.txt"	整个打开的文件，有状态、位置等
# 能做什么	只是一个文本标签	     可以读取、写入、关闭等操作
# 比喻	   书的标题	               一本实际打开的书
#
# 2. !!!重要注意事项：
# 文件名必须精确：必须使用new_discovery.txt作为文件名
# 写入模式是覆盖的：'w'模式会清空已存在的文件内容
# 需要手动换行：write()方法不会自动添加换行符，需要自己加\n
# 使用with语句：确保文件正确关闭，避免数据损坏
# 退出：测试完成后，在终端按Ctrl+D或输入exit即可退出。
# 思考题答案（来自练习文档）：
# 什么是提取模式('r')和保存模式('w')的关键区别？
# 'r'（读取）模式：只能读取文件，不能修改，如果文件不存在会报错
# 'w'（写入）模式：创建新文件或清空现有文件，可以写入内容
# 为什么这个区别对档案管理员很重要？
# 因为档案管理员处理的是宝贵的历史数据，如果误用'w'模式可能会永久覆盖重要档案。
# 必须清楚知道何时读取（查看历史）和何时写入（创建新记录）
