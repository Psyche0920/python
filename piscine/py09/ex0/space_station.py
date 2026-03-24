from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: Optional[str] = Field(default=None, max_length=200)


def main() -> None:
    print("Space Station Date Validation")
    print("=" * 40)

    valid_station = SpaceStation(
        station_id="ISS001",
        name="International Space Station",
        crew_size=6,
        power_level=85.5,
        oxygen_level=92.3,
        last_maintenance="2024-01-15T10:30:00",
        is_operational=True,
        notes="Primary orbital research station."
    )
    print("Valid station created:")
    print(f"ID: {valid_station.station_id}")
    print(f"Name: {valid_station.name}")
    print(f"Crew: {valid_station.crew_size} people")
    print(f"Power: {valid_station.power_level}%")
    if valid_station.is_operational:
        print("Status: Operational")
    else:
        print("Status: Not Operational")
    print()

    print("=" * 40)

    try:
        SpaceStation(
            station_id="BAD001",
            name="Broken Station",
            crew_size=25,
            power_level=80.0,
            oxygen_level=90.0,
            last_maintenance="2024-01-15T10:30:00"
        )
    except ValidationError as error:
        print("Expected validation error:")
        print(error)


if __name__ == "__main__":
    main()

#
# ge = greater than or equal to = 大于等于
# le = less than or equal to = 小于等于
#
# [Test]
# create an independent virtual environment
# pip install "pydantic>=2,<3"
# python3 space_station.py
#
# 输入类型	示例
# datetime object	datetime(2024,1,15,10,30)
# ISO string	"2024-01-15T10:30:00"
# timestamp	1705314600
#
#
# Pydantic 在创建模型对象时会做三步：
# ① 检查字段类型
# 你的模型：
# last_maintenance: datetime
# 意思是：
# 这个字段必须是 datetime
#
# ② 如果输入类型不同 → 尝试转换
# 你输入：
# last_maintenance="2024-01-15T10:30:00"
# 类型是：
# str
# 但 Pydantic 会尝试：
# str → parse → datetime
#
# ③ 转换成功
# Pydantic 内部变成：
# datetime(2024, 1, 15, 10, 30, 0)
# 模型创建成功。
#
# ④ 如果转换失败
# 例如：
# last_maintenance="banana"
# 无法解析为时间。
# Pydantic 会抛出：
# ValidationError
