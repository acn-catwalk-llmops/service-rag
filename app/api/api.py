from fastapi import APIRouter

from app.schemas.query import QueryBase, QueryResponse

router = APIRouter()


@router.post("/query", status_code=201, response_model=QueryResponse)
def query(query: QueryBase):
    """
    Query the Service
    """
    print(query)
    return QueryResponse(
        user_id=query.user_id,
        query=query.query,
        response="Yes, it works!",
    )
