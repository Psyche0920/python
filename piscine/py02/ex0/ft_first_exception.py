def check_temperature(temp_str: str):
    """Check if temperature is safe for plants (0-40°C)."""
    try:
        temp = int(temp_str)
        if temp < 0:
            print(f"Error: {temp}°C is too cold for plants (min 0°C)")
        elif temp > 40:
            print(f"Error: {temp}°C is too hot for plants (max 40°C)")
        else:
            print(f"Temperature {temp}°C is perfect for plants!")
    except ValueError:
        print(f"Error: '{temp_str}' is not a valid number")


def test_temperature_input():
    """Test the temperature checker with different inputs."""
    test_cases = ['25', 'abc', '100', '-50']
    for test_value in test_cases:
        print(f"\nTesting temperature: {test_value}")
        check_temperature(test_value)


if __name__ == "__main__":
    print("=== Garden Temperature Checker ===")
    test_temperature_input()
    print("\nAll tests completed - program didn't crash!")

# try-except 可以只用一行处理所有未知错误
# try:
#     任意可能失败的操作()
# except Exception:  # 就这一行，捕获所有错误！
#     处理任何错误()  # 包括你完全不知道的错误
#
# # if 做不到这一点！
# # 你无法用 if 检查你不知道的条件
# if 我没想到的条件():  # 不可能！
#     任意可能失败的操作()
# else:
#     处理任何错误()
#
# The try block lets you test a block of code for errors.
#
# The except block lets you handle the error.
