from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    @abstractmethod
    def process(self, data: Any) -> str:
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    def format_output(self, result: str) -> str:
        return f"Output: {result}"


class NumericProcessor(DataProcessor):
    def __init__(self):
        # 这里创建了自己的 __init__
        self.processed_count = 0  # 添加子类特有的属性
        # 因为没有调用 super().__init__()
        # 但 DataProcessor 也没有 __init__ 需要调用
        # 所以这样写是没问题的

    def validate(self, data: Any) -> bool:
        try:
            if not isinstance(data, list):
                return False
            for item in data:
                if not isinstance(item, (int, float)):
                    return False
            return True
        except Exception:
            return False

    def process(self, data: Any) -> str:
        try:
            if not self.validate(data):
                return "Error: Invalid numeric data"
            count = len(data)
            total = sum(data)
            average = total / count if count > 0 else 0
            self.processed_count += count
            result = (
                f"Processed {count} numeric values, "
                f"sum={total}, avg={average:.1f}"
            )

            return result
        except Exception as e:
            return f"Error processing numeric data: {str(e)}"

# 如果 count == 0，程序不会报错，average 会被安全地设为 0，整个函数正常返回。


class TextProcessor(DataProcessor):
    def __init__(self):
        self.processed_chars = 0

    def validate(self, data: Any) -> bool:
        return isinstance(data, str)

    def process(self, data: Any) -> str:
        try:
            if not self.validate(data):
                return "Error: Invalid text data (not a string)"
            char_count = len(data)
            word_count = len(data.split())
            self.processed_chars += char_count
            result = (
                f"Processed text: {char_count} characters, "
                f"{word_count} words"
            )
            return result
        except Exception as e:
            return f"Error processing text data: {str(e)}"


class LogProcessor(DataProcessor):
    """
    处理日志字符串的处理器
    """
    # 日志级别与前缀映射
    LOG_LEVELS = {
        "ERROR": "[ALERT]",
        "WARN": "[WARNING]",
        "INFO": "[INFO]",
        "DEBUG": "[DEBUG]"
    }

    def __init__(self):
        self.error_count = 0

    def validate(self, data: Any) -> bool:
        """
        校验日志是否以合法的日志级别开头
        """
        if not isinstance(data, str):
            return False
        data_upper = data.upper()
        for level in self.LOG_LEVELS.keys():
            if data_upper.startswith(level + ":"):
                return True
        return False

    def process(self, data: Any) -> str:
        """
        解析日志级别并生成对应输出
        """
        try:
            if not self.validate(data):
                return "Error: Invalid log entry"
            parts = data.split(":", 1)
            if len(parts) < 2:
                return "Error: Malformed log entry"
            log_level = parts[0].strip().upper()
            message = parts[1].strip()

            prefix = self.LOG_LEVELS.get(log_level, "UNKNOWN")
            if log_level == "ERROR":
                self.error_count += 1

            result = f"{prefix} {log_level} level detected: {message}"
            return result
        except Exception as e:
            return f"Error processing log data: {str(e)}"


def main() -> None:
    print("=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===\n")

    # -------- Numeric --------
    print("Initializing Numeric Processor...")
    numeric = NumericProcessor()
    numeric_data = [1, 2, 3, 4, 5]
    print(f"Processing data: {numeric_data}")
    print("Validation:", "Numeric data verified"
          if numeric.validate(numeric_data) else "Invalid")
    print(numeric.format_output(numeric.process(numeric_data)))
    print()

    # -------- Text --------
    print("Initializing Text Processor...")
    text = TextProcessor()
    text_data = "Hello Nexus World"
    print(f'Processing data: "{text_data}"')
    print("Validation:", "Text data verified"
          if text.validate(text_data) else "Invalid")
    print(text.format_output(text.process(text_data)))
    print()

    # -------- Log --------
    print("Initializing Log Processor...")
    log = LogProcessor()
    log_data = "ERROR: Connection timeout"
    print(f'Processing data: "{log_data}"')
    print("Validation:", "Log entry verified"
          if log.validate(log_data) else "Invalid")
    print(log.format_output(log.process(log_data)))
    print()

    # -------- Polymorphism Demo --------
    print("=== Polymorphic Processing Demo ===\n")
    print("Processing multiple data types through same interface...")

    processors = [NumericProcessor(), TextProcessor(), LogProcessor()]
    datas = [[1, 2, 3], "Hello Nexus", "INFO: System ready"]

    for i in range(3):
        processor = processors[i]
        data = datas[i]
        result = processor.process(data)
        print(f"Result {i + 1}: {result}")

    print("\nFoundation systems online. Nexus ready for advanced streams.")


if __name__ == "__main__":
    main()

# 1. 方法重写是如何让同一个处理接口可以处理完全不同的数据类型的？
# 方法重写的核心作用，是让子类在保持相同方法名和接口的前提下，实现各自不同的行为。
# 在这个例子中，父类 DataProcessor 定义了统一的接口，比如：
# process()
# validate()
# format_output()
# 这些方法只定义“做什么”，而不关心“怎么做”。
# 每个子类根
# NumericProcessor.process() 负责数值计算
# TextProcessor.process() 负责文本统计
# LogProcessor.process() 负责日志解析
# 当程序调用：
# processor.process(data)时，Python 会在运行时根据 processor 实际指向的对象类型，自动选择对应子类的实现。
# 因此，接口是统一的，但行为是多样的，这就是多态
#
# 2. 为什么这种方式比把所有逻辑写成独立的处理函数更强大？
# 1)不需要大量的条件判断2)不需要知道具体是哪种处理器。
#
# 这个示例是为了演示多态机制，本身假设数据和处理器已经正确匹配。
# 自动匹配属于更高层的调度问题，不在这个 exercise 的范围内
