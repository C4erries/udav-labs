from dataclasses import dataclass


@dataclass(frozen=True)
class Client:
    id: int | None
    full_name: str
    phone: str
    email: str
    birth_date: str


@dataclass(frozen=True)
class Policy:
    id: int | None
    client_id: int
    policy_number: str
    product_type: str
    start_date: str
    end_date: str
    premium: float
    insured_amount: float


@dataclass(frozen=True)
class Claim:
    id: int | None
    policy_id: int
    claim_date: str
    description: str
    amount: float
    status: str

