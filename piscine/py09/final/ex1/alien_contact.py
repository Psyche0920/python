from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, ValidationError, model_validator


class ContactType(str, Enum):
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = False

    @model_validator(mode="after")
    def check_business_rules(self):
        if not self.contact_id.startswith("AC"):
            raise ValueError('contact_id must start with "AC"')
        if (
            self.contact_type == ContactType.physical
            and not self.is_verified
        ):
            raise ValueError("Physical contact must be verified")
        if (
            self.contact_type == ContactType.telepathic
            and self.witness_count < 3
        ):
            raise ValueError("Telepathic contact needs at least 3 witnesses")
        if self.signal_strength > 7 and not self.message_received:
            raise ValueError("Strong signal requires a message")
        return self


def main() -> None:
    print("Alien Contact Log Validation")
    print("=" * 40)
    valid = AlienContact(
        contact_id="AC_2024_001",
        timestamp="2024-06-01T21:15:00",
        location="Area 51, Nevada",
        contact_type=ContactType.radio,
        signal_strength=8.5/10,
        duration_minutes=45,
        witness_count=5,
        message_received="Greetings from Zeta Reticuli",
        is_verified=False
    )

    print("Valid contact report:")
    print(f"ID: {valid.contact_id}")
    print(f"Type: {valid.contact_type.value}")
    print(f"Location: {valid.location}")
    print(f"Signal: {valid.signal_strength}/10")
    print(f"Duration: {valid.duration_minutes} minutes")
    print(f"Witnesses: {valid.witness_count}")
    print(f"Message: '{valid.message_received}'")
    print()
    print("=" * 40)

    try:
        AlienContact(
            contact_id="AC_2024_002",
            timestamp="2024-06-01T21:15:00",
            location="Mars Base",
            contact_type=ContactType.telepathic,
            signal_strength=6.0,
            duration_minutes=15,
            witness_count=2
        )
    except ValidationError as e:
        print("Expected validation error:")
        print(e)


if __name__ == "__main__":
    main()

# Field 主要负责“单字段约束”，model_validator 负责“跨字段逻辑”。
