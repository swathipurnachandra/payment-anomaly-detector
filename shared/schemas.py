from dataclasses import dataclass, asdict, field
from typing import Optional


@dataclass
class UserProfile:
    user_id: int
    home_city: str
    preferred_payment: str
    average_amount: int
    favorite_merchants: list[str]


@dataclass
class Transaction:
    transaction_id: str
    user_id: int
    amount: float
    merchant: str
    city: str
    payment_method: str
    timestamp: str

    is_anomaly: bool = False
    anomaly_reason: Optional[str] = None

    def to_dict(self):
        return asdict(self)