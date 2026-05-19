from pydantic import BaseModel


class ClientCreate(BaseModel):
    full_name: str
    phone: str
    email: str
    birth_date: str


class PolicyCreate(BaseModel):
    client_id: int
    policy_number: str
    product_type: str
    start_date: str
    end_date: str
    premium: float
    insured_amount: float


class ClaimCreate(BaseModel):
    policy_id: int
    claim_date: str
    description: str
    amount: float
    status: str

