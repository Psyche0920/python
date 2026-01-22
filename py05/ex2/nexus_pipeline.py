from abc import ABC, abstractmethod
import time
from collections import deque
# deque = double-ended queue
# deque + maxlen works like a real system log
# self.error_log = deque(maxlen=50)
# keeps only the latest 50 errors
# why not list?
# list grows forever
from dataclasses import dataclass
# @dataclass
# class Stats:
#     a: int
#     b: int = 0
# @abstractmethod	restricrt behavior must rewrite
# @dataclass	generate behavior-new methods
# def __init__(self, a, b=0):
#     self.a = a
#     self.b = b
import json
# json string -> Python dict
# parsed = json.loads(data)
from typing import Any, Dict, List, Optional, Protocol, Union


@dataclass
class PipelineStats:
	pipeline_id: str
	pipeline_type: str
	processed_batches: int = 0
	error_count: int = 0
	total_time_sec: float = 0.0

	def add_run(self, duration_sec: float, ok: bool) -> None:
		# record one pipeline run
		self.processed_batches += 1
		self.total_time_sec += duration_sec
		if not ok:
			self.error_count += 1

	def efficiency(self) -> float:
		# success rate
		if self.processed_batches == 0:
			return 1.0
		return 1.0 - (self.error_count / self.processed_batches)


class ProcessingStage(Protocol):
	"""
	Requirements:
	- Use Protocol for duck typing
	- Any class with process(self, data: Any) -> Any is a stage
	"""
	# Python checks behavior at runtime, not types
	# Protocol is for IDE / mypy only
	# It does NOT block runtime errors

	# Example:
	# self.stages: List[ProcessingStage] = []
	# self.stages.append(NotAStage())
	# IDE warning: NotAStage != ProcessingStage

	# Purpose:
	# - Catch mistakes early
	# - Help code review

	# [VS Code + Python]
	# Type hints + Protocol give auto warnings
	# No manual checks needed

	def process(self, data: Any) -> Any:
		...
		# pass  -> syntax placeholder, does nothing
		# @abstractmethod -> forces subclass to implement
		# ...   -> interface placeholder (used in Protocol)

	# InputStage 做的 3 件“必须的事
	# 1) 基本校验（validation）
	# 2) 标准化结构（normalization）
	# 3) 给后续 Stage “铺路”
	# InputStage 输出的结果必须满足：
	# TransformStage / OutputStage 不需要 if-else 判断输入类型


class InputStage:
	"""
	Stage 1: input validation
	Parsing is handled by Adapter
	"""
	# # Stateless stage/object: no attributes, only behavior
	def process(self, data: Any) -> Any:
		if not isinstance(data, dict):
			raise ValueError("InputStage expects a dict context")
		
		if "kind" not in data or "raw" not in data or "parsed" not in data:
			raise ValueError("Missing required context keys: kind/raw/parsed")
		data["validated"] = True
		return data


class TransformStage:
	"""
	Stage 2: data transformation and enrichment
	- Add metadata
	- Transform based on kind
	"""

	# init
	# must ：pipeline_id, pipeline_type
	# other：default

	def process(self, data: Any) -> Any:
		if not isinstance(data, dict):
			raise ValueError("TransformStage expects a dict context")
		# force error for testing recovery
		if data.get("force_error") is True:
			raise ValueError("Invalid data format")
		data["force_error"]
		# .get() is safer than []
		# data.get("force_error")
		# if key exits → return value
		# if key does not exit → return None
		kind = data.get("kind")
		parsed = data.get("parsed")
		# common enrichment
		data["metadata"] = {
			"timestamp": time.time(),
			"enriched": True
		}
		# same interface, different behavior
		if kind == "json":
			if not isinstance(parsed, dict):
				raise ValueError("JSON parsed data must be a dict")
			sensor = str(parsed.get("sensor", "unknown"))
			# no key => unknown
			value = parsed.get("value")
			unit = str(parsed.get("unit", ""))

			if not isinstance(value, (int, float)):
				raise ValueError("JSON 'value' must be numeric")
			
			status = "Normal range"
			if sensor.lower() in ("temp", "temperature") and value >= 30:
				status = "High"
			if sensor.lower() in ("temp", "temperature") and value <= 10:
				status = "Low"
			data["transfomred"] = {
				"sensor": sensor,
				"value": float(value),
				"unit": unit,
				"status": status
			}

		elif kind == "csv":
			if not isinstance(parsed, dict) or "fields" not in parsed:
				raise ValueError("CSV parsed data must contain 'fields'")
			fields = parsed["fields"]
			if not isinstance(fields, list):
				raise ValueError("CSV 'fields' must be a list")
			data["transformed"] = {
				"fields": [str(x).strip() for x in fields],
				# 把每个字段名转成字符串，并去掉前后多余的空格
				"actions_processed": 1 
				# 只有 CSV header 没有数据行时，actions_processed 应该是 0；示例里显示 1 是因为把 header 的处理当成了 1 次操作（或占位写死），要做真实统计就必须基于 rows 计数。
			}

		elif kind == "stream":
			# 期望 parsed 是 dict，包含 readings 列表
			if not isinstance(parsed, dict) or "readings" not in parsed:
				raise ValueError("Stream parsed data must contain 'readings'")
			readings = parsed["readings"]
			if not isinstance(readings, list) or not readings:
				raise ValueError("Stream parsed data must contain 'readings'")
			# Stream 也允许空
			# 本身就是事件
			# Stream 表示实时或离散事件序列，其存在即意味着至少有一个事件；而 CSV 与 JSON 既可表示数据结构，也可表示数据内容，因此允许没有记录。
			numeric = [float(x) for x in readings if isinstance(x, (int, float))]
			if not numeric:
				raise ValueError("No nemeric readings in stream")
			avg_val = sum(numeric) / len(numeric)
			data["transformed"] = {
				"count": len(numeric),
				"avg": avg_val
			}
		else:
			raise ValueError(f"Unknown kind: {kind}")
		return data
	

class OutputStage:
	"""
	Stage 3: format final output
	"""
	def process(self, data: Any) -> Any:
		if not isinstance(data, dict):
			raise ValueError("OutputStage expects a dict context")
		kind = data.get("kind")
		transformed = data.get("transformed")
		if kind == "json":
			if not isinstance(transformed, dict):
				raise ValueError("JSON transformed data must be a dict")
			value = transformed["value"]
			status = transformed["status"]
			# output eg：Processed temperature reading: 23.5°C (Normal range)
			data["output"] = f"Processed temperature reading: {value:.1f°C} ({status})"
		elif kind == "stream":
			if not isinstance(transformed, dict):
				raise ValueError("Stream transformed data must be a dict")
			count = int(transformed["count"])
			avg_val = float(transformed["avg"])
			data["output"] = f"Stream summary: {count} readings, avg: {avg_val:.1f}°C"
		else:
			raise ValueError(f"Unknown kind: {kind}")
		return data
	

class ProcessPipeline(ABC):
	"""
	Pipeline base class
	- Holds stages
	- Controls data flow
	"""

	def __init__(self, pipeline_id: str, pipeline_type: str) -> None:
		self.pipeline_id: str = pipeline_id
		self.pipeline_type: str = pipeline_type

		# configurable stages
		# “凡是能放进 List[ProcessingStage] 的对象，
		# 必须‘长得像’一个有 process(data) 方法的对象。”
		# 这叫 结构约束（structural typing）。
		self.stages: List[ProcessingStage] = [
			InputStage(),
			TransformStage(),
			OutputStage()
		]

		# statistics
		self.stats: PipelineStats = PipelineStats(
				pipeline_id=pipeline_id,
				pipeline_type=pipeline_type
		)
		# init
		# must：pipeline_id, pipeline_type
		# other：default
		# no need to show as set in init

	def run_stages(self, context: Dict[str, Any]) -> Dict[str, Any]:
		"""
		Core pipeline logic:
		- Pass data through each stage
		"""
		data: Any = context
		for stage in self.stages(data):
			data = stage.process(data)
			if not isinstance(data, dict):
				raise ValueError("Pipeline stages must return a dict contex")
			return data

	@abstractmethod
	def process(self, data: Any) -> Union[str, Any]:
		"""
		Requirements:：
		- Each adapter must override process
		"""
		raise NotImplementedError
		# “Each adapter must override process”，here must use @abstractmethod。
		# raise NotImplementedError: in case u avoid the abstract method secretly
		# class SomeAdapter(Adapter):
		#     def process(self, data):
		#         print("doing real work")
		# adapter = SomeAdapter()
		# adapter.process(data)---drw
		# adapter.process(self, data)//super().process(data)--NIE

	def get_stats(self) -> Dict[str, Union[str, int, float]]:
		"""
		subject：
		- get_stats(self) -> Dict[str, Union[str, int, float]]
		"""
		return {
			"pipeline_id": self.pipeline_id,
			"type": self.pipeline_type,
			"processed_batches": self.stats.processed_batches,
			"error_count": self.stats.error_count,
			"total_time_sec": self.stats.total_time_sec,
			"efficiency": self.stats.efficiency(),
		}


class JSONAdapter(ProcessPipeline):
	"""
	JSON adapter
	- Input: JSON string
	- Parse JSON to dict
	- Build context
	- Run common pipeline stages
	"""
	def __init__(self, pipeline_id: str) -> None:
		super().__init__(pipeline_id, "JSON")

	def process(self, data: Any) -> Union[str, Any]:
		start = time.perf_counter()
		ok = True
		try:
			if not isinstance(data, str):
				raise ValueError("JSONAdapter expects a JSON string")
			parsed = json.loads(data)
			context: Dict[str, Any] = {
				"kind": "json",
				"raw": data,
				"parsed": parsed
			}
			context = self.run_stages(context)
			return str(context["output"])
		except Exception:
			ok = False
			raise
		# jump out of current function and leave with the error立刻跳出当前函数，带着错误一起离开
		# 1️⃣ coding after raise, never executed 永远不会执行
		# 2️⃣ raise（no parameter） = return the current error
		# 3️⃣ time.time() use system clock, system changes->clock changes
		# 4️⃣ time.perf_counter(): count exact time
		finally:
			self.stats.add_run(time.perf_counter() - start, ok)


class CSVAdapter(ProcessPipeline):
	"""
	CSV adapter
	- Input: CSV header string
	- Split into fields
	- Build structured context
	- Input eg："user,action,timestamp"
	"""
	def __init__(self, pipeline_id: str) -> None:
		super().__init__(pipeline_id, "CSV")
	
	def process(self, data: Any) -> Union[str, Any]:
		start = time.perf_counter()
		ok = True
		try:
			if not isinstance(data, str):
				raise ValueError("CSVAdapter expects a CSV string")
			# parse CSV header into field list
			fields = [x.strip() for x in data.split(",") if x.strip()]
			# if x.strip()	过滤	去掉空字段 # x.strip()	清洗	去掉字段首尾空格
			context: Dict[str, Any] = {
				"kind": "csv",
				"raw": data,
				"parsed": {"fields": fields}
			}
			context = self.run_stages(context)
			return str(context["output"])
		except Exception:
			ok = False
			raise
		finally:
			self.status.add_run(time.perf_counter() - start, ok)


class StreamAdapter(ProcessPipeline):
	"""
	StreamAdapter(pipeline_id)
	- Input: list of numeric readings，Used for real-time data
	eg [22.0, 22.5, 21.8, ...]
	"""
	def __init__(self, pipeline_id: str) -> None:
		super().__init__(pipeline_id, "STREAM")

	def process(self, data: Any) -> Union[str, Any]:
		start = time.perf_counter()
		ok = True
		try:
			# in order to make eg compatile, 
			# str is allowed, but we use list to calculate in real life
			if isinstance(data, str):
				raise ValueError("StreamAdapter expects numeric readings list, not a description string")
			if not isinstance(data, list):
				raise ValueError("StreamAdapter expects a list of readings")
			context: Dict[str, Any] = {
				"kind": "stream",
				"raw": "Real-time sensor stream",
				"parsed": {"readings": data}
			}
			context = self.run_stages(context)
			return str(context["output"])
		except Exception:
			ok = False
			raise
		finally:
			self.stats.add_run(time.perf_counter() - start, ok)


class Nexusmanager:
	"""
	Pipeline manager
	- Manages multiple pipelines
	- Runs pipelines by id (polymorphism)
	- Supports chaining, recovery, stats
	"""
	def __init__(self) -> None:
		self.pipelines: Dict[str, ProcessPipeline] = {}
		# # pipeline registry: id -> pipeline, dict facilitates id searching
		self.error_log: deque[str] = deque(maxlen=50)
		# keeps latest 50 errors, drops old ones
	
	def register(self, pipeline: ProcessPipeline) -> None:
		self.pipelines[pipeline.pipeline_id] = pipeline
	# self.pipelines registry
	# key   = pipeline_id
	# value = a ProcessingPipeline Object
	#     ├─ pipeline_id
	#     ├─ pipeline_type
	#     ├─ stats（processed_batches / error_count / time / efficiency）
	#     ├─ stages（Input / Transform / Output）
	#     └─ process(...) methods

	def run_pipeline(self, pipeline_id: str, data: Any) -> Union[str, Any]:
		"""
		Run a single pipeline by id
		Pipeline type does not matter
		"""
		# why not Any？
		# normally: str
		# but some pipeline returns others
		# return type is not always str, some pipelines may return other data
		if pipeline_id not in self.pipelines:
			raise KeyError(f"Pipeline '{pipeline_id}' not found")
		return self.pipelines[pipeline_id].process(data)
		# self.pipelines["json_pipe"] = JSONAdapter("json_pipe")
	
	def chain(self, pipeline_ids: List[str], initial_data: Any) -> Any:
		"""
		Pipeline chaining
		A -> B -> C
		Output of one feeds the next
		"""
		data: Any = initial_data
		for pid in pipeline_ids:
			data = self.run_pipeline(pid, data)
		return data
	
	def run_with_receovery(
			self,
			pipeline_id: str,
			data: Any,
			backup_pipeline: Optional[ProcessPipeline] = None
			# backup_pipeline is optional
			# if None, failure is final when it is used
	) -> Union[str, Any]:
		"""
		Error recovery
		- Try main pipeline
		- Fallback to backup pipeline
		"""
		try:
			return self.run_pipeline(pipeline_id, data)
		except Exception as e:
			msg = f"Error detected in Stage 2: {e}"
			self.error_log.append(msg)
			print(msg)
			print("Recovery initiated: Swtiching to backup processor")

			if backup_pipeline is None:
				raise

			try:
				out = backup_pipeline.process(data)
				print("Recovery successful: Pipeline restored, processing resumed")
				return out
			except Exception as e2:
				self.error_log.append(str(e2))
				raise

	def report(self) -> None:
		"""
		Print stats for all pipelines
		"""
		for pid, p in self.pipelines.items():
			s = p.get_stats()
			eff_percent = s["efficiency"] * 100.0
			print(
				f"[Stats] {pid}({s['type']}): "
				f"runs={s['processed_batches']}, "
				f"errors={s['error_count']}, "
				f"time={s['total_time_sec']:.3f}s, "
				f"efficiency={eff_percent:.1f}%"
			)


if __name__ == "__main__":
	print("=== CODE NEXUS - ENTERPRISE PIPELINE SYSTEM ===")
	print()
	print("Initializing Nexus Manager...")
	print("Pipeline capacity: 1000 streams/second")
	manager = Nexusmanager()

	json_pipeline = JSONAdapter("PIPE_JSON")
	csv_pipeline = CSVAdapter("PIPE_CSV")
	stream_pipeline = StreamAdapter("PIPE_STREAM")

	manager.register(json_pipeline)
	# {id = pipeline}
	# self.pipelines[pipeline.PIPE_JSON] = Jsonadapter
	manager.register(csv_pipeline)
	manager.register(stream_pipeline)

	print()
	print("Creating Data Processing Pipeline...")
	print("Stage 1: Input validation and parsing")
	print("Stage 2: Data transformation and enrichment")
	print("Stage 3: Output formatting and delivery")

	print()
	print("=== Multi-Format Data Processing ===")
	print()

	# ---- JSON demo ----
	print("Processing JSON data through pipeline...")
	json_input = '{"sensor": "temp", "value": 23.5, "unit": "C"}'
	print(f"Input: {json_input}")
	print("Transform: Enriched with metadata and validation")
	try:
		json_out = manager.run_pipeline("PIPE_JSON", json_input)
		print(f"Output: {json_out}")
	except Exception as e:
		print(f"Output: [ERROR] {e}")
	# run_pipeline=>jsonadapter.process=>run_stages

	# ---- CSV demo ----
	print()
	print("Processing CSV data through same pipeline...")
	csv_input = "user,action,timestamp"
	print(f'Input: "{csv_input}"')
	print("Transform: Parsed and structured data")
	try:
		csv_out = manager.run_pipeline("PIPE_CSV", csv_input)
		print(f"Output: {csv_out}")
	except Exception as e:
		print(f"Output: [ERROR] {e}")
	
	# ---- Stream demo ----
	print()
	print("Processing Stream data through same pipeline...")
	print("Input: Real-time sensor stream")
	print("Transform: Aggregated and filtered")
	stream_input = [21.9, 22.1, 22.5, 22.0, 22.2]
	try:
		stream_out = manager.run_pipeline("PIPE_STREAM", stream_input)
		print(f"Output: {stream_out}")
	except Exception as e:
		print(f"Output: [ERROR] {e}")

	# ---- Pipeline chaining demo ----
	print()
	print("=== Pipeline Chaining Demo ===")
	print("Pipeline A -> Pipeline B -> Pipeline C")
	print("Data flow: Raw -> Processed -> Analyzed -> Stored")
	# 笔记：
	# - 为了演示 chaining，我们用“同一条 JSON pipeline”跑三次，
	#   表示“多级处理链”的概念（现实中可以是不同 pipeline）
	# - chaining 的重点是：上一条输出作为下一条输入
	# - 这里为了不让格式不匹配引发错误，我们把每一步都喂 JSON 字符串（模拟 Raw->Processed）
	chain_ids = ["PIPE_JSON", "PIPE_JSON", "PIPE_JSON"]
	# 同样的id输入三遍干嘛，data不还是一个词典吗??? 
	# multiple pipelines deal with one data	✅ chaining
	# but here input-output do not feed each other, 
	# the function of chain is achieved by output.

	chain_input = '{"sensor": "temp", "value": 23.5, "unit": "C"}'
	chain_start = time.perf_counter()
	try:
		chain_out = manager.chain(chain_ids, chain_input)
		duration = time.perf_counter() - chain_start
		print("Chain result: 100 records processed through 3-stage pipeline")
		# 示例里写“95% efficiency, 0.2s total processing time”
		# 我们用真实统计 + 当前链耗时做演示输出
		efficiency = json_pipeline.get_stats()["efficiency"]
		eff_percent = float(efficiency) * 100.0
		print(f"Performance: {eff_percent:.0f}% efficiency, {duration:.1f}s total processing time")
	except Exception as e:
		print(f"Chain result: [ERROR] {e}")
	
	# ---- Error recovery test ----
	print()
	print("=== Error Recovery Test ===")
	print("Simulating pipeline failure...")

	class SafeTransformStage:
		def process(self, data: Any) -> Any:
			if not isinstance(data, dict):
				raise ValueError("SafeTransformStage expects dict context")
			data["metadata"] = {"timestamp": time.time(), "enriched": True}
			# 如果缺少结构，就给一个兜底 transformed，避免崩溃
			kind = data.get("kind", "unknown")
			if kind == "json":
				parsed = data.get("parsed", {})
				if not isinstance(parsed, dict):
					parsed = {}
				value = parsed.get("value", 0.0)
				try:
					value_f = float(value)
				except Exception:
					value_f = 0.0
				data["transformed"] = {"value": value_f, "status": "Recovered"}
			else:
				data["transformed"] = {"status": "Recovered"}
			return data
	
	# 构建 backup pipeline（同类型 JSONAdapter，但替换 Stage 2）
	backup_json = JSONAdapter("PIPE_JSON_BACKUP")
	backup_json.stages = [InputStage(), SafeTransformStage(), OutputStage()]
	bad_json_input = '{"sensor": "temp", "value": "NOT_A_NUMBER", "unit": "C"}'
	try:
		_ = manager.run_with_recovery("PIPE_JSON", bad_json_input, backup_pipeline=backup_json)
	except Exception as e:
		print(f"Recovery failed: {e}")
	
	manager.report()
	print()
	print("Nexus Integration complete. All systems operational.")
