import sys


def main() -> None:
    """Demonstrate proper use of stdin, stdout, and stderr streams."""
    # 1. 输出到 stdout（标准输出）- 系统标题
    print("=== CYBER ARCHIVES - COMMUNICATION SYSTEM ===\n")
    # 2. 从 stdin（标准输入）读取用户输入
    print("Input Steam active.", end=" ")
    archivist_id: str = input("Enter archivist ID: ")
    print("Input Stream active.", end=" ")
    status_report: str = input("Enter status report: ")
    print()
    # 3. 输出到 stdout（正常状态信息）
    print(f"[STANDARD] Archive status from {archivist_id}: {status_report}")
    # 4. 输出到 stderr（标准错误）- 警报信息
    print("[ALERT] System diagnostic: Communication channels verified",
          file=sys.stderr)
    # 5. 输出到 stdout（完成消息）
    print("[STANDARD] Data transmission complete")
    print()
    print("Three-channel communication test successful.")


if __name__ == "__main__":
    main()

# 1. 实际应用场景：
# 日志系统：正常日志到 stdout，错误日志到 stderr
# 命令行工具：正常输出可以被管道处理，错误信息直接显示
# 服务程序：stdout 可以重定向到日志文件，stderr 发送到监控系统
# 2. 最终验证检查清单
# ✅ 文件名：ft_stream_management.py
# ✅ 目录：ex2/
# ✅ 导入：import sys
# ✅ 使用 input() 从 stdin 读取
# ✅ 使用 print() 输出到 stdout
# ✅ 使用 print(..., file=sys.stderr) 输出到 stderr
# ✅ 输出格式符合要求
# ✅ 类型提示：def main() -> None:
# ✅ 文档字符串（可选但推荐）
# 3. 思考题答案：
# 为什么档案馆要维护独立的通道？如果这些流混合会发生什么？
# 原因：分离正常数据和警报，便于监控和故障排查
# 后果：如果混合，紧急警报可能被正常输出淹没，无法快速响应危机
# 退出：测试完成后，按 Ctrl+D 或输入 exit 退出终端。
# 4. print()默认换行, end=" " 用空格结尾，而不是换行
# 5. print() 默认就是 file=sys.stdout，input() 默认就是读取 sys.stdin
