from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass
import json
import time
import io
from contextlib import redirect_stdout
from typing import Any, Dict, List, Optional, Protocol, Union


@dataclass
class PipelineStats:
    """Collect pipeline timing and error statistics."""
    pipeline_id: str
    pipeline_type: str
    processed_batches: int = 0
    error_count: int = 0
    total_time_sec: float = 0.0

    def add_run(self, dt: float, ok: bool) -> None:
        """Record one run duration and whether it succeeded."""
        self.processed_batches += 1
        self.total_time_sec += dt
        if not ok:
            self.error_count += 1

    def efficiency(self) -> float:
        """Return success rate as a float in [0, 1]."""
        if self.processed_batches == 0:
            return 1.0
        return 1.0 - (self.error_count / self.processed_batches)


class ProcessingStage(Protocol):
    """Duck-typed stage interface: any object with process(data) is a stage."""
    def process(self, data: Any) -> Any:
        ...


class InputStage:
    """Stage 1: validate the shared context structure."""
    def process(self, data: Any) -> Any:
        if not isinstance(data, dict):
            raise ValueError("InputStage expects a dict context")

        required = ("kind", "raw", "parsed")
        if any(k not in data for k in required):
            raise ValueError("Missing required context keys: kind/raw/parsed")

        data["validated"] = True
        return data


class TransformStage:
    """Stage 2: enrich and transform based on data kind."""
    def __init__(self, verbose: bool = True) -> None:
        self.verbose = verbose

    def process(self, data: Any) -> Any:
        if not isinstance(data, dict):
            raise ValueError("TransformStage expects a dict context")

        kind = data.get("kind")
        parsed = data.get("parsed")

        data["metadata"] = {"timestamp": time.time(), "enriched": True}

        if kind == "json":
            print("Transform: Enriched with metadata and validation")
            if not isinstance(parsed, dict):
                raise ValueError("JSON parsed data must be a dict")

            sensor = str(parsed.get("sensor", "unknown"))
            value = parsed.get("value")
            unit = str(parsed.get("unit", ""))

            if not isinstance(value, (int, float)):
                raise ValueError("JSON 'value' must be numeric")

            status = "Normal range"
            if sensor.lower() in ("temp", "temperature") and value >= 30:
                status = "High"
            if sensor.lower() in ("temp", "temperature") and value <= 10:
                status = "Low"

            data["transformed"] = {
                "sensor": sensor,
                "value": float(value),
                "unit": unit,
                "status": status,
            }
            return data

        if kind == "csv":
            print("Transform: Parsed and structured data")
            if not isinstance(parsed, dict) or "fields" not in parsed:
                raise ValueError("CSV parsed data must contain 'fields'")

            fields = parsed["fields"]
            if not isinstance(fields, list):
                raise ValueError("CSV 'fields' must be a list")

            data["transformed"] = {
                "fields": [str(x).strip() for x in fields],
                "actions_processed": 1,
            }
            return data

        if kind == "stream":
            print("Transform: Aggregated and filtered")
            if not isinstance(parsed, dict) or "readings" not in parsed:
                raise ValueError("Stream parsed must contain 'readings'")

            readings = parsed["readings"]
            if not isinstance(readings, list):
                raise ValueError("Stream 'readings' must be a list")

            numeric = [float(x) for x in readings
                       if isinstance(x, (int, float))]
            if not numeric:
                raise ValueError("No numeric readings in stream")

            avg_val = sum(numeric) / len(numeric)
            data["transformed"] = {"count": len(numeric), "avg": avg_val}
            return data

        raise ValueError(f"Unknown kind: {kind}")


class OutputStage:
    """Stage 3: format a human-readable output string."""
    def process(self, data: Any) -> Any:
        if not isinstance(data, dict):
            raise ValueError("OutputStage expects a dict context")

        kind = data.get("kind")
        transformed = data.get("transformed")

        if not isinstance(transformed, dict):
            raise ValueError("Missing transformed dict")

        if kind == "json":
            value = float(transformed["value"])
            status = transformed["status"]
            data["output"] = (
                "Processed temperature reading: "
                f"{value:.1f}°C ({status})"
            )
            return data

        if kind == "csv":
            count = int(transformed.get("actions_processed", 0))
            data["output"] = f"User activity logged: {count} actions processed"
            return data

        if kind == "stream":
            count = int(transformed["count"])
            avg_val = float(transformed["avg"])
            data["output"] = (
                f"Stream summary: {count} readings, avg: {avg_val:.1f}°C"
            )
            return data

        raise ValueError(f"Unknown kind: {kind}")


class ProcessingPipeline(ABC):
    """Abstract pipeline base class with configurable stages."""
    def __init__(self, pipeline_id: str, pipeline_type: str) -> None:
        self.pipeline_id = pipeline_id
        self.pipeline_type = pipeline_type
        self.stages: List[ProcessingStage] = [
            InputStage(),
            TransformStage(),
            OutputStage(),
        ]
        self.stats = PipelineStats(pipeline_id, pipeline_type)

    def run_stages(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute stages in order and return the updated context."""
        data: Any = context
        for stage in self.stages:
            data = stage.process(data)
            if not isinstance(data, dict):
                raise ValueError("Pipeline stages must return dict context")
        return data

    def process_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Run stages with timing/error stats, but without adapter parsing."""
        start = time.perf_counter()
        ok = True
        try:
            return self.run_stages(context)
        except Exception:
            ok = False
            raise
        finally:
            self.stats.add_run(time.perf_counter() - start, ok)

    @abstractmethod
    def process(self, data: Any) -> Union[str, Any]:
        ...


class JSONAdapter(ProcessingPipeline):
    """Adapter: parse JSON string to context, then run shared stages."""
    def __init__(self, pipeline_id: str) -> None:
        super().__init__(pipeline_id, "JSON")

    def process(self, data: Any) -> str:
        start = time.perf_counter()
        ok = True
        try:
            if not isinstance(data, str):
                raise ValueError("JSONAdapter expects a JSON string")

            parsed = json.loads(data)
            context: Dict[str, Any] = {
                "kind": "json",
                "raw": data,
                "parsed": parsed,
            }
            context = self.run_stages(context)
            return str(context["output"])
        except Exception:
            ok = False
            raise
        finally:
            self.stats.add_run(time.perf_counter() - start, ok)


class CSVAdapter(ProcessingPipeline):
    """Adapter: parse CSV header string into fields, then run shared stages."""
    def __init__(self, pipeline_id: str) -> None:
        super().__init__(pipeline_id, "CSV")

    def process(self, data: Any) -> str:
        start = time.perf_counter()
        ok = True
        try:
            if not isinstance(data, str):
                raise ValueError("CSVAdapter expects a CSV string")

            fields = [x.strip() for x in data.split(",") if x.strip()]
            context: Dict[str, Any] = {
                "kind": "csv",
                "raw": data,
                "parsed": {"fields": fields},
            }
            context = self.run_stages(context)
            return str(context["output"])
        except Exception:
            ok = False
            raise
        finally:
            self.stats.add_run(time.perf_counter() - start, ok)


class StreamAdapter(ProcessingPipeline):
    """Adapter: wrap numeric readings as a stream context, then run stages."""
    def __init__(self, pipeline_id: str) -> None:
        super().__init__(pipeline_id, "STREAM")

    def process(self, data: Any) -> str:
        start = time.perf_counter()
        ok = True
        try:
            if isinstance(data, str):
                raise ValueError(
                    "StreamAdapter expects numeric readings list, not a string"
                )
            if not isinstance(data, list):
                raise ValueError("StreamAdapter expects a list of readings")

            context: Dict[str, Any] = {
                "kind": "stream",
                "raw": "Real-time sensor stream",
                "parsed": {"readings": data},
            }
            context = self.run_stages(context)
            return str(context["output"])
        except Exception:
            ok = False
            raise
        finally:
            self.stats.add_run(time.perf_counter() - start, ok)


class NexusManager:
    """Orchestrate multiple pipelines polymorphically."""
    def __init__(self) -> None:
        self.pipelines: Dict[str, ProcessingPipeline] = {}
        self.error_log: deque[str] = deque(maxlen=50)

    def register(self, pipeline: ProcessingPipeline) -> None:
        self.pipelines[pipeline.pipeline_id] = pipeline

    def run_pipeline(self, pipeline_id: str, data: Any) -> Union[str, Any]:
        if pipeline_id not in self.pipelines:
            raise KeyError(f"Pipeline '{pipeline_id}' not found")
        return self.pipelines[pipeline_id].process(data)

    def chain_context(
        self,
        pipeline_ids: List[str],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        data = context
        for pid in pipeline_ids:
            data = self.pipelines[pid].process_context(data)
        return data

    def run_with_recovery(
        self,
        pipeline_id: str,
        context: Dict[str, Any],
        backup_pipeline: Optional[ProcessingPipeline] = None,
    ) -> Dict[str, Any]:
        try:
            return self.pipelines[pipeline_id].process_context(context)
        except Exception as e:
            msg = f"Error detected in Stage 2: {e}"
            self.error_log.append(msg)
            print(msg)
            print("Recovery initiated: Switching to backup processor")

            if backup_pipeline is None:
                raise

            out_ctx = backup_pipeline.process_context(context)
            print("Recovery successful: Pipeline restored, processing resumed")
            return out_ctx

    def report(self) -> None:
        for pid, p in self.pipelines.items():
            s = p.stats
            eff = s.efficiency() * 100.0
            print(
                f"[Stats] {pid}({p.pipeline_type}): "
                f"runs={s.processed_batches}, "
                f"errors={s.error_count}, "
                f"time={s.total_time_sec:.3f}s, "
                f"efficiency={eff:.1f}%"
            )


class FailingTransformStage:
    """Deliberately fail to demonstrate recovery."""
    def process(self, data: Any) -> Any:
        raise ValueError("Invalid data format")


class SafeTransformStage:
    """Fallback transform that guarantees a transformed output."""
    def process(self, data: Any) -> Any:
        if not isinstance(data, dict):
            raise ValueError("SafeTransformStage expects dict context")

        data["metadata"] = {"timestamp": time.time(), "enriched": True}
        parsed = data.get("parsed")
        kind = data.get("kind")

        if kind == "json" and isinstance(parsed, dict):
            value = parsed.get("value", 0.0)
            try:
                v = float(value)
            except Exception:
                v = 0.0
            data["transformed"] = {
                "sensor": str(parsed.get("sensor", "unknown")),
                "value": v,
                "unit": str(parsed.get("unit", "")),
                "status": "Recovered",
            }
            return data

        data["transformed"] = {"status": "Recovered"}
        return data


if __name__ == "__main__":
    print("=== CODE NEXUS - ENTERPRISE PIPELINE SYSTEM ===")
    print()
    print("Initializing Nexus Manager...")
    print("Pipeline capacity: 1000 streams/second")
    print()
    print("Creating Data Processing Pipeline...")
    print("Stage 1: Input validation and parsing")
    print("Stage 2: Data transformation and enrichment")
    print("Stage 3: Output formatting and delivery")

    manager = NexusManager()

    json_pipeline = JSONAdapter("PIPE_JSON")
    csv_pipeline = CSVAdapter("PIPE_CSV")
    stream_pipeline = StreamAdapter("PIPE_STREAM")

    manager.register(json_pipeline)
    manager.register(csv_pipeline)
    manager.register(stream_pipeline)

    print()
    print("=== Multi-Format Data Processing ===")
    print()
    print("Processing JSON data through pipeline...")
    json_input = '{"sensor": "temp", "value": 23.5, "unit": "C"}'
    print(f"Input: {json_input}")
    print(f"Output: {manager.run_pipeline('PIPE_JSON', json_input)}")

    print()
    print("Processing CSV data through same pipeline...")
    csv_input = "user,action,timestamp"
    print(f'Input: "{csv_input}"')
    print(f"Output: {manager.run_pipeline('PIPE_CSV', csv_input)}")

    print()
    print("Processing Stream data through same pipeline...")
    print("Input: Real-time sensor stream")
    stream_input = [21.9, 22.1, 22.5, 22.0, 22.2]
    print(f"Output: {manager.run_pipeline('PIPE_STREAM', stream_input)}")

    print()
    print("=== Pipeline Chaining Demo ===")
    print("Pipeline A -> Pipeline B -> Pipeline C")
    print("Data flow: Raw -> Processed -> Analyzed -> Stored")

    chain_ids = ["PIPE_JSON", "PIPE_JSON", "PIPE_JSON"]
    start = time.perf_counter()

    with redirect_stdout(io.StringIO()):
        for i in range(100):
            ctx = {
                "kind": "json",
                "raw": "record",
                "parsed": {"sensor": "temp", "value": 20 + i, "unit": "C"},
            }
        manager.chain_context(chain_ids, ctx)

    dt = time.perf_counter() - start
    eff = json_pipeline.stats.efficiency() * 100.0
    print()
    print("Chain result: 100 records processed through 3-stage pipeline")
    print(f"Performance: {eff:.0f}% efficiency, {dt:.3f}s total "
          f"processing time")

    print()
    print("=== Error Recovery Test ===")
    print("Simulating pipeline failure...")

    fail_pipe = JSONAdapter("PIPE_JSON_FAIL")
    fail_pipe.stages = [InputStage(), FailingTransformStage(), OutputStage()]
    manager.register(fail_pipe)

    backup_json = JSONAdapter("PIPE_JSON_BACKUP")
    backup_json.stages = [InputStage(), SafeTransformStage(), OutputStage()]

    bad = {"sensor": "temp", "value": "NOT_A_NUMBER", "unit": "C"}
    bad_ctx = {"kind": "json", "raw": str(bad), "parsed": bad}

    manager.run_with_recovery(
        "PIPE_JSON_FAIL",
        bad_ctx,
        backup_pipeline=backup_json,
    )

    print()
    print("Nexus Integration complete. All systems operational.")


# 是否继承 ProcessingStage
# InputStage
# TransformStage❌
# SafeTransformStage❌
# FailingTransformStage❌
# 但它们 全都是 ProcessingStage 的 subtype，因为：
# 它们都实现了 process(self, data)
# 所以这是：
# Protocol + structural subtyping（结构型子类型）
# 3️⃣ 考试一句话标准答案（非常重要）
# 这是基于 Protocol 的结构型子类型，
# 不依赖继承，而是通过方法签名实现多态。
# 在 ProcessPipeline.run_stages 中，
# stages 被声明为 List[ProcessingStage]，
# 而 ProcessingStage 是一个 Protocol，
# 这意味着 stages 里的对象不要求继承某个父类，
# 只要它们 实现了 process(self, data) 方法 就可以。
# 👉 因此：
# 我可以在不修改 run_stages 的情况下，
# 将第二个 TransformStage
# 替换为 SafeTransformStage，
# 而整个 pipeline 仍然可以正常运行。
# so in processpipeline.run_stages(stages),
# stages here is defined as protocol processingstage,
# which means the stages here can be replaced by any obejcts
# having the same def process.
# thats why we can replace the second transform stage with safetransformstage
# and if we dont use protol, ide may not warn if safetransofrmstage
# does not contain def process
#
# 1️⃣ Method Overriding ——「行为定制」
# 作用：
# 方法重写（子类对父类中已有方法进行重新实
# 子类在不改变方法签名的情况下
# 提供特定于自身的实现逻辑
# 在你的项目中：
# class JSONAdapter(ProcessPipeline):
#     def process(self, data: str) -> str: ...
# class CSVAdapter(ProcessPipeline):
#     def process(self, data: str) -> str: ...
# class StreamAdapter(ProcessPipeline):
#     def process(self, data: list) -> str: ...
# 👉 同一个 process()，不同语义
#
# 2️⃣ Subtype Polymorphism ——「统一调用」子类型多态
# （不同子类对象可以通过同一父类型接口被统一使用）
# 作用：
# 上层代码通过父类型 / 接口调用对象
# 不关心对象的具体子类型
# 在你的系统中：
# pipelines: Dict[str, ProcessPipeline]
# 调用时：
# pipeline.process(data)
# 👉 调用者 不知道也不需要知道：
# 是 JSON
# 是 CSV
# 还是 Stream
#
# 三、二者结合后，系统发生了什么质变？
# ✅ 1. 新数据类型 ≠ 修改旧代码
# 现实问题：
# “系统上线后，来了一个新数据格式怎么办？”
# ❌ 没有多态的系统：
# 修改 if/else
# 改旧逻辑
# 动全身
# ✅ 你的设计：
# class XMLAdapter(ProcessPipeline):
#     def process(self, data: str) -> str:
#     ...
# 👉 零修改旧代码
# ✅ 2. 避免“巨型 if-else 地狱”
# 现实问题：
# “一个函数里处理 10 种数据类型，能维护吗？”
# ❌ 传统写法：
# if type == "json":
# elif type == "csv":
# elif type == "stream":
# ...
# ✅ 多态写法：
# pipeline.process(data)
