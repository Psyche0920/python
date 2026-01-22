def ft_garden_summary():
    name = str(input("Enter garden name: "))
    number = int(input("Enter number of plants: "))
    print("Garden:", name)
    print("Plants:", number)
    print("Status: Growing well!")

# 其实 input() 默认返回字符串，这里显式转换是好的做法
