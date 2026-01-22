if __name__ == "__main__":
    name = "Rose"
    height = 25
    age = 30

    print("=== Welcome to My Garden ===")
    print(f"Plant: {name}")
    print(f"Height: {height}cm")
    print(f"Age: {age} days\n")
    print("=== End of Program ===")

# 1️⃣什么是 shebang（#!）？
# 这一行叫 shebang（释伴），它：
# 不是 Python 代码
# 是给 Linux / macOS 的 shell 看的
# 告诉系统：
# 👉 “这个文件应该用哪个解释器来执行
# 2️⃣ shebang 什么时候有用？
# 只有在这种情况下才有用：
# ./ft_garden_intro.py
# 并且你还需要：
# chmod +x ft_garden_intro.py
#
# 3. c after compiling vs python + jeshiqi/shebang
# C 编译后生成的是操作系统可直接执行的机器码，而 Python 源文件只是文本，必须通过解释器执行，
# 因此需要显式指定 Python 解释器或使用 shebang。
# 4. an example
# imported file add1.py
# def add():
#         a = 1
#         b = 2
#         result = a + b
#         return(result)
# if __name__ == "__main__":
#         print(add())
#
# file main.py
# if __name__ == "__main__":
#     import add1
#     print(add1.add() + add1.add())
