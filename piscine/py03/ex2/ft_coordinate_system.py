import sys
import math


def calculate_distance(p1, p2):
    """Calculate 3D Euclidean distance between two points"""
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)


def parse_coordinate_str(coord_str):
    """Parse coordinate string like 'x,y,z' into a tuple"""
    parts = coord_str.split(",")
    if len(parts) != 3:
        raise ValueError(f"Expected 3 coordinates, got {len(parts)}")
    return (int(parts[0]), int(parts[1]), int(parts[2]))


def main():
    print("=== Game Coordinate System ===")
    origin = (0, 0, 0)
    pos1 = (10, 20, 5)
    print(f"\nPosition created: {pos1}")
    dist1 = calculate_distance(origin, pos1)
    print(f"Distance between {origin} and {pos1}: {dist1:.2f}")

    if len(sys.argv) < 2:
        coord_str = "3,4,0"
    else:
        coord_str = sys.argv[1]

    print(f'\nParsing coordinates: "{coord_str}"')
    try:
        pos2 = parse_coordinate_str(coord_str)
        print(f"Parsed position: {pos2}")
        dist2 = calculate_distance(origin, pos2)
        print(f"Distance between {origin} and {pos2}: {dist2:.1f}")

        invalid_coord = "abc,def,ghi"
        print(f'\nParsing invalid coordinates: {invalid_coord!r}')
        try:
            parse_coordinate_str(invalid_coord)
        except ValueError as e:
            print(f"Error parsing coordinates: {e}")
            print(f"Error details - Type: ValueError, Args: {e.args}")

        x, y, z = pos2
        print("\nUnpacking demonstration:")
        print(f"Player at x={x}, y={y}, z={z}")
        print(f"Coordinates: X={x}, Y={y}, Z={z}")
    except ValueError as e:
        print(f"Error parsing coordinates: {e}")
        print(f"Error details - Type: ValueError, Args: {e.args}")


if __name__ == "__main__":
    main()
# Q1
# 🔑 为什么用 tuple？
# 坐标 不应该被修改
# tuple：()
# 有顺序
# 不可变
# 语义上非常适合“位置”
# 2. teleport commands?
# 这些字符串需要被解析成程序可以理解的数字坐标。
# Q2
# 3. x, y, z = position
# 是真正的元组解包（Tuple Unpacking）
# 像拆开一个包裹，把所有东西都拿出来
# 一次性操作，优雅且安全
# Pythonic的写法，推荐使用
# x = position[0]
# 不是元组解包，只是索引访问（Index Access）
# 像从盒子里一次拿一件东西
# 多次操作，不够优雅
# 在某些定场景有用，但不是"解包"
# 4. e vs e.args
# 特性	   e（异常对象）	   e.args（异常参数）
# 是什么	完整的异常对象	    创建异常时的参数元组
# 显示内容	人类可读的错误消息	 原始的错误数据
# 类型  	ValueError 实例	  tuple
# 通常用途	给用户显示错误	    调试和日志记录
# 在项目中	不够详细	       ✅ 符合要求格式
# 示例     invalid literal...	("invalid literal...",)
# 5. !r = 使用 repr() 函数格式化
# 显示字符串的代码表示，包括引号
# 在调试和错误处理中特别有用
# 符合项目输出要求：显示 'abc,def,ghi' 而不是 abc,def,ghi
