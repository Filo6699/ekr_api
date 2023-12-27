from pydantic import BaseModel


class UpdateBalanceRequest(BaseModel):
    owner_username: str
    new_balance: int
