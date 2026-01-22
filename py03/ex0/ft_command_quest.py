# sys.argv 是命令行处理，因为它是程序与命令行之间的唯一数据通道，把用户在终端输入的所有信息传递给程序
# sys 模块是 Python 标准库 中的一个核心模块，它提供了与 Python 解释器 和 运行时环境 交互的变量和函数。
# 为什么 Python 选择使用列表（数组）来存储命令行参数。本质上：这是一个有序的字符串序列
# 列表的特性：有序、可索引、保持顺序 → 完美匹配！
import sys


def main():
    av = sys.argv
    print("=== Command Quest ===")
    ac = len(av)
    if ac < 2:
        print("No arguments provided!")
        print(f"Program name: {av[0]}")
        print(f"Total arguments: {ac}")
    else:
        i = 1
        print(f"Program name: {av[0]}")
        print(f"Arguments received: {ac - 1}")
        while i < ac:
            print(f"Argument {i}: {av[i]}")
            i += 1
        print("Total arguments:", ac)


if __name__ == "__main__":
    main()

# Q1: 你的程序如何知道用户想要它做什么？
# 你的程序通过 sys.argv 知道用户想要它做什么
# 用户意图 → 终端命令 → 操作系统 → Python解释器 → 你的程序
# 总结：你的程序通过 sys.argv 接收用户的命令行输入，然后根据参数的[数量、位置和内容]，推断出用户想要它做什么，并执行相应的操作。
# Q2: 程序名和参数之间的区别是什么？
# 特征	               程序名 (Program Name)	参数 (Arguments)
# 是什么	           程序的文件名	              给程序的额外信息
# 在 sys.argv 中的位置	索引 0 (sys.argv[0])	  索引 1 及之后 (sys.argv[1:])
# 谁提供的	            操作系统/Shell自动提供	     用户手动提供
# 是否必需	            总是存在	                可选
# 作用	                标识要运行的程序	         告诉程序具体做什么/给程序的输入数据或配置信息
