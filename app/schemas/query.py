from pydantic import BaseModel


class QueryBase(BaseModel):
    user_id: str
    query: str


class QueryResponse(QueryBase):
    response: str
