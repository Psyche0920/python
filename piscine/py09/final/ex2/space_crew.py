from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, ValidationError, model_validator
from typing import List


class Rank(str, Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: List[CrewMember] = Field(min_length=1, max_length=12)
    # list[CrewMember], Field(list_len)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def check_mission_rules(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError('Mission ID must start with "M"')

        if not any(
            member.rank in (Rank.commander, Rank.captain)
            for member in self.crew
        ):
            raise ValueError(
                "Mission must have at least one Commander or Captain"
            )

        if self.duration_days > 365:
            experienced_count = sum(
                member.years_experience >= 5
                for member in self.crew
            )
            if experienced_count / len(self.crew) < 0.5:
                raise ValueError(
                    "Long missions (> 365 days) need 50% experienced "
                    "crew (5+ years)"
                )

        if not all(member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")

        return self


def main() -> None:
    print("Space Mission Crew Validation")
    print("=" * 40)

    valid_mission = SpaceMission(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        launch_date="2025-03-15T08:00:00",
        duration_days=900,
        crew=[
            CrewMember(
                member_id="C01",
                name="Sarah Connor",
                rank=Rank.commander,
                age=42,
                specialization="Mission Command",
                years_experience=15,
                is_active=True
            ),
            CrewMember(
                member_id="C02",
                name="John Smith",
                rank=Rank.lieutenant,
                age=35,
                specialization="Navigation",
                years_experience=8,
                is_active=True
            ),
            CrewMember(
                member_id="C03",
                name="Alice Johnson",
                rank=Rank.officer,
                age=29,
                specialization="Engineering",
                years_experience=4,
                is_active=True
            )
        ],
        mission_status="planned",
        budget_millions=2500.0
    )

    print("Valid mission created:")
    print(f"Mission: {valid_mission.mission_name}")
    print(f"ID: {valid_mission.mission_id}")
    print(f"Destination: {valid_mission.destination}")
    print(f"Duration: {valid_mission.duration_days} days")
    print(f"Budget: ${valid_mission.budget_millions}M")
    print(f"Crew size: {len(valid_mission.crew)}")
    print("Crew members:")
    for member in valid_mission.crew:
        print(
            f"- {member.name} ({member.rank.value}) - "
            f"{member.specialization}"
        )
    print()
    print("=" * 40)

    try:
        SpaceMission(
            mission_id="M2024_FAIL",
            mission_name="Deep Space Survey",
            destination="Europa",
            launch_date="2025-06-01T12:00:00",
            duration_days=100,
            crew=[
                CrewMember(
                    member_id="C10",
                    name="Tom Baker",
                    rank=Rank.officer,
                    age=30,
                    specialization="Science",
                    years_experience=6,
                    is_active=True
                ),
                CrewMember(
                    member_id="C11",
                    name="Emma Davis",
                    rank=Rank.lieutenant,
                    age=33,
                    specialization="Medical",
                    years_experience=7,
                    is_active=True
                )
            ],
            mission_status="planned",
            budget_millions=500.0
        )
    except ValidationError as error:
        print("Expected validation error:")
        print(error)


if __name__ == "__main__":
    main()

# 1. 嵌套模型（nested models）
# crew: List[CrewMember]
# 意思是：
# crew 是一个列表，里面的每一个元素都必须是 CrewMember 模型。
# 所以 SpaceMission 的结构其实是：
# SpaceMission
#  ├─ mission_id
#  ├─ mission_name
#  ├─ destination
#  ├─ launch_date
#  ├─ duration_days
#  └─ crew
#        ├─ CrewMember
#        ├─ CrewMember
#        └─ CrewMember

# #2. Pydantic 会递归验证嵌套模型。
# 当 SpaceMission 包含 CrewMember 列表时，Pydantic 会逐个验证每个 CrewMember。
# 如果其中任何一个 CrewMember 验证失败，
# 整个 SpaceMission 的验证都会失败，
# 并抛出 ValidationError，同时指出错误发生在嵌套结构中的具体位置。
