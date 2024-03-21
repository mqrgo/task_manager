from pydantic import BaseModel



class UserTask(BaseModel):
    topic: bytes
    user_id: int
    is_done: bool = False