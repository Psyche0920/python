from abc import ABC, abstractmethod
from typing import Any, List, Dict, Union, Optional


def pretty_batch(items: List[str]) -> str:
    # 用某个字符串，把列表里的字符串“粘”起来
    return "[" + ", ".join(items) + "]"


class DataStream(ABC):
    """
    DataStream 是所有数据流的「父类」
    作用：
    - 定义统一接口（process_batch）
    - 提供可复用的默认行为（filter_data / get_stats）
    """

    def __init__(self, stream_id: str, stream_type: str) -> None:
        self.stream_id: str = stream_id
        self.stream_type: str = stream_type
        self.processed_count: int = 0
    # 因为 DataStream 已经是业务层的父类，ABC 不需要初始化，所以不需要调用 super()

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        pass

    def summarize_batch(self, data_batch: List[Any]) -> str:
        return self.process_batch(data_batch)

    def filter_data(self, data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
        if criteria is None:
            return data_batch
        # 默认策略：如果是字符串，只保留包含 criteria 的项
        return [item for item in data_batch
                if isinstance(item, str) and criteria in item]

    def get_stats(self) -> Dict[str, Union[str, int]]:
        """
        返回通用统计信息
        """
        return {
            "stream_id": self.stream_id,
            "type": self.stream_type,
            "processed_count": self.processed_count
        }


class SensorStream(DataStream):
    """
    传感器数据流
    专门处理数值型数据（int / float）
    """
    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id, "Environmental Data")

    def process_batch(self, data_batch: List[Any]) -> str:
        try:
            numeric_data: List[float] = []
            temp_values: List[float] = []

            for x in data_batch:
                if isinstance(x, str) and ":" in x:
                    key, value_str = x.split(":", 1)
                    numeric_data.append(float(value_str.strip()))
                    if key == "temp":
                        temp_values.append(float(value_str.strip()))

            if not numeric_data:
                raise ValueError("No valid sensor data")

            self.processed_count += len(numeric_data)
            if not temp_values:
                raise ValueError("No temperature reading found")
            avg_value = sum(temp_values) / len(temp_values)

            return (
                f"Sensor analysis: {len(numeric_data)} readings processed, "
                f"avg temp: {avg_value:.1f}°C"
            )
        except Exception as e:
            return f"[SensorStream Error {e}]"

    def summarize_batch(self, data_batch: List[Any]) -> str:
        count = sum(1 for x in data_batch if isinstance(x, str) and ":" in x)
        self.processed_count += count
        return f"Sensor data: {count} readings processed"


class TransactionStream(DataStream):
    """
    交易数据流
    专门处理带 buy / sell 的字符串
    """
    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id, "Financial Data")

    def process_batch(self, data_batch: List[Any]) -> str:
        try:
            transactions = [
                x for x in data_batch
                if isinstance(x, str)
            ]
            if not transactions:
                raise ValueError("No transaction data")
            net_flow = 0
            op_count = 0
            for t in transactions:
                if ":" not in t:
                    continue
                action, value_str = t.split(":", 1)
                action = action.strip().lower()
                value = int(value_str.strip())

                if action == "buy":
                    net_flow += value
                    op_count += 1
                elif action == "sell":
                    net_flow -= value
                    op_count += 1

            if op_count == 0:
                raise ValueError("No valid operations")

            self.processed_count += op_count
            sign = "+" if net_flow >= 0 else ""

            return (
                f"Transaction analysis: {op_count} operations, "
                f"net flow: {sign}{net_flow} units"
            )
        except Exception as e:
            return f"[TransactionStream ERROR] {e}"

    def summarize_batch(self, data_batch: List[Any]) -> str:
        count = 0
        for t in data_batch:
            if isinstance(t, str) and ":" in t:
                action = t.split(":", 1)[0].strip().lower()
                if action in ("buy", "sell"):
                    count += 1
        self.processed_count += count
        return f"Transaction data: {count} operations processed"


class EventStream(DataStream):
    """
    事件数据流
    用于系统日志 / 事件（login / error / logout）
    """
    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id, "System Events")

    def process_batch(self, data_batch: List[Any]) -> str:
        try:
            events = [
                x for x in data_batch
                if isinstance(x, str)
            ]
            if not events:
                raise ValueError("No event data")
            error_count = sum(1 for x in events if "error" in x.lower())
            self.processed_count += len(events)
            return (
                f"Event data: {len(events)} events processed, "
                f"{error_count} errors detected"
            )
        except Exception as e:
            return f"[EventStream ERROR] {e}"

    def summarize_batch(self, data_batch: List[Any]) -> str:
        count = sum(1 for x in data_batch if isinstance(x, str))
        self.processed_count += count
        return f"Event data: {count} events processed"


class StreamProcessor:
    """
    统一的流处理器
    - 不关心具体是哪种 Stream
    streams= [sensor, transaction, event]
    self.streams.append(stream) means add sensor, transaction, event...
    process_all : batches [[]]
    """
    def __init__(self) -> None:
        self.streams: List[DataStream] = []

    def add_stream(self, stream: DataStream) -> None:
        self.streams.append(stream)

    def process_all(self, batches: List[List[Any]]) -> List[str]:
        """
        体现多态：
        - 同一个方法调用
        - 不同 stream 自动执行不同实现
        """
        results: List[str] = []
        for stream, batch in zip(self.streams, batches):
            results.append(stream.process_batch(batch))
        return results

    def summarize_all(self, batches: List[List[Any]]) -> List[str]:
        results: List[str] = []
        for stream, batch in zip(self.streams, batches):
            results.append(stream.summarize_batch(batch))
        return results

# 把两个列表 一一配对
# zip(self.streams, batches)
# [
#     (self.streams[0], batches[0]),
#     (self.streams[1], batches[1]),
#     (self.streams[2], batches[2])
# ]


if __name__ == "__main__":
    print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===")

    sensor_stream = SensorStream("SENSOR_001")
    transaction_stream = TransactionStream("TRANS_001")
    event_stream = EventStream("EVENT_001")

    processor = StreamProcessor()
    processor.add_stream(sensor_stream)
    processor.add_stream(transaction_stream)
    processor.add_stream(event_stream)
    # add_stream: add the created Stream to a processor list

    data_batches = [
        ["temp:22.5", "humidity:65", "pressure:1013"],
        ["buy:100", "sell:150", "buy:75"],
        ["login", "error", "logout"]
    ]

    # ===== 剧情化输出（初始化阶段）=====
    print("Initializing Sensor Stream...")
    print(f"Stream ID: {sensor_stream.stream_id}, "
          f"Type: {sensor_stream.stream_type}")
    print("Processing sensor batch:", pretty_batch(data_batches[0]))
    print(sensor_stream.process_batch(data_batches[0]))
    print()

    print("Initializing Transaction Stream...")
    print(f"Stream ID: {transaction_stream.stream_id}, "
          f"Type: {transaction_stream.stream_type}")
    print("Processing transaction batch:", pretty_batch(data_batches[1]))
    print(transaction_stream.process_batch(data_batches[1]))
    print()

    print("Initializing Event Stream...")
    print(f"Stream ID: {event_stream.stream_id}, "
          f"Type: {event_stream.stream_type}")
    print("Processing event batch:", pretty_batch(data_batches[2]))
    print(event_stream.process_batch(data_batches[2]))
    print()

    # ===== 多态演示阶段 =====
    data_batches1 = [
        ["temp:22.5", "pressure:1013"],
        ["buy:100", "sell:150", "buy:75", "buy:10"],
        ["login", "error", "logout"]
    ]
    print("=== Polymorphic Stream Processing ===")
    print("Processing mixed stream types through unified interface...")
    print("Batch 1 Results:")

    results = processor.summarize_all(data_batches1)
    for line in results:
        print(f"- {line}")

    # ===== 过滤演示用数据 =====
    print()
    print("Stream filtering active: High-priority data only")

    sensor_filter_batch = [
        "CRITICAL: temp:99.9",
        "CRITICAL: pressure:2000",
        "temp:22.5"
    ]
    trans_filter_batch = [
        "buy:10",
        "sell:20",
        "buy:1000"
    ]

    critical_sensor_alerts = [x for x in sensor_filter_batch
                              if "CRITICAL" in x]
    large_transactions = [
        t for t in trans_filter_batch
        if ":" in t and int(t.split(":", 1)[1].strip()) >= 1000
    ]
    print(
        f"Filtered results: {len(critical_sensor_alerts)} "
        f"critical sensor alerts, "
        f"{len(large_transactions)} large transaction"
    )
    print()
    print("All streams processed successfully. Nexus throughput optimal.")
# 1
# ┌──────────────────────────────────────────────┐
# │                 ① 对象层（Objects）          │
# │  “会干活的人 / 处理器对象”                     │
# │                                              │
# │  SensorStream("SENSOR_001")                   │
# │    - stream_id = "SENSOR_001"                 │
# │    - processed_count = 0                      │
# │    - process_batch(...)  # 处理数字/传感器逻辑  │
# │                                              │
# │  TransactionStream("TRANS_001")               │
# │    - stream_id = "TRANS_001"                  │
# │    - processed_count = 0                      │
# │    - process_batch(...)  # 处理买卖/净流逻辑    │
# │                                              │
# │  EventStream("EVENT_001")                     │
# │    - stream_id = "EVENT_001"                  │
# │    - processed_count = 0                      │
# │    - process_batch(...)  # 处理事件/error统计  │
# └──────────────────────────────────────────────┘
#
#                  │  add_stream(...) 把“人”登记进系统
#                  │
# ┌──────────────────────────────────────────────┐
# │                 ② 调度层（Scheduler）        │
# │          StreamProcessor（指挥官 / 管理器）   │
# │                                              │
# │  processor.streams = [                        │
# │     SensorStream(...),                        │
# │     TransactionStream(...),                   │
# │     EventStream(...)                          │
# │  ]                                           │
# │                                              │
# │  process_all(batches):                        │
# │    for stream, batch in zip(streams, batches) │
# │        stream.process_batch(batch)   ← 多态发生 │
# │        stream.get_stats()                     │
# └──────────────────────────────────────────────┘
#                  │
#                  │  zip(streams, batches) “一一配对”
#                  │  (第 i 个对象 ↔ 第 i 批数据)
#                  ▼
# ┌──────────────────────────────────────────────┐
# │                 ③ 数据层（Data）             │
# │     “原材料 / 输入数据（每个 stream 一批）”     │
# │                                              │
# │  batches = [                                  │
# │    sensor_batch,       # 给 SensorStream       │
# │    transaction_batch,  # 给 TransactionStream  │
# │    event_batch         # 给 EventStream        │
# │  ]                                           │
# │                                              │
# │  sensor_batch      = [22.5, 23.0, 21.8, ...]  │
# │  transaction_batch = ["buy:100","sell:50",...]│
# │  event_batch       = ["login","error","logout"]│
# └──────────────────────────────────────────────┘

# 1. Optional[str] 是什么？
# 这是 typing 语法，等价于：
# Union[str, None]
# 2. ex0	vs     ex1
# main负责一切	    main 只负责组装
# for 循环 = 调度	StreamProcessor = 调度
# 逻辑混在一起	     逻辑有明确边界
# # 所以ex0和ex1的多模态本质是一样的，只不过一个是在main里for循环实现，另一个先用类再调用
# Q1：多态如何让 StreamProcessor 在不知道具体实现的情况下处理不同 stream？
# 通过多态，StreamProcessor 只依赖 DataStream 这个抽象父类接口，
# 在运行时由 Python 自动根据对象的真实类型调用对应子类的实现，
# 因此不需要知道具体是 SensorStream、TransactionStream 还是其他类型。
# Q2：这种设计的好处是什么？
# 这种设计实现了解耦、可扩展性和可维护性，使系统可以在不修改调度逻辑的情况下新增新的数据流类型。
# For example, to support a new LogStream, I only need to create a new class
# that implements DataStream and add it to the processor.
# The StreamProcessor itself does not need to be modified,
# which demonstrates extensibility.
# Transformation pipeline（转换流水线
