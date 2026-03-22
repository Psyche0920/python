def water_plants(plant_list: list):
    print("Opening watering system")
    try:
        for plant in plant_list:
            if plant is None:
                raise ValueError("Cannot water None - invalid plant!")
            print(f"Watering {plant}")
    except ValueError as e:
        print(f"Error: {e}")
        return
    finally:
        print("Closing watering system (cleanup)")
    print("Watering completed successfully!")


def test_watering_system():
    print("=== Garden Watering System ===\n")
    print("Testing normal watering...")
    water_plants(["tomato", "lettuce", "carrots"])
    print("\nTesting with error...")
    water_plants(["tomato", None, "carrots"])
    print("\nCleanup always happens, even with errors!")


if __name__ == "__main__":
    test_watering_system()


# 1. raise 做了三件事：
# 创建异常对象：ValueError("Cannot water None - invalid plant!")
# 中断当前执行：立即停止当前代码块的执行
# 向上传递异常：沿着调用栈向上寻找匹配的 except 块
# 2. 对比其他跳出循环的方式：
# 方法	作用	是否继续执行循环外代码
# break	跳出当前循环	会执行循环后的代码
# return	跳出整个函数	不会执行函数后面的代码
# raise	抛出异常，跳出到最近的 except	不会执行异常后的代码
# 3. Q1: finally 块中的重要性：
# 根据 PDF 要求，这个练习的重点是 finally 块。
# "Clean up" = 做完该做的事，收拾好工具，关好门，让一切回到正常/安全状态。
# Q2: 无论是否发生错误，finally 块都会执行，确保资源被清理：
# 4. try:
#     # 1. 执行代码...
#     raise SomeError()  # ← 触发点
#     # 之后的代码不执行
# except SomeError:
#     # 2. 处理异常
#     # 如果这里没有 return/raise → 继续
#     # 如果有 return → 准备返回
#     # 如果有另一个 raise → 重新抛出
# finally:
#     # 3. 总是执行！
#     # 无论上面发生什么
# # 4. 这里的代码：
# #    - 如果上面正常完成 → 执行
# #    - 如果上面有 return → 不执行
# #    - 如果上面有新的 raise → 不执行
# 5. None or if not?
# 1) 题目文字确实没明确说检查什么
# 题目只说："Handles errors if a plant name is invalid"
# 什么是"invalid"？没定义
# 可能是 None、空字符串、数字等等
# 2) 但示例明确显示了 None
# 示例错误信息是："Cannot water None - invalid plant!"
# 这明确显示测试用例中有 None
