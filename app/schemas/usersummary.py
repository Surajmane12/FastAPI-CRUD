


from pydantic import BaseModel, ConfigDict


class UserSummary(BaseModel):
    
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: str
