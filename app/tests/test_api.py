from typing import Optional
from fastapi.testclient import TestClient

from app.schemas.query import QueryBase, QueryResponse

from app.main import app
from app.service.rag import RAGService, create_rag_service


class MockRAGService(RAGService):
    def load_documents(self) -> None:
        return None

    def query(self, query: QueryBase) -> Optional[QueryResponse]:
        return QueryResponse(
            user_id=query.user_id,
            query=query.query,
            response="this is a response",
            sources=[],
        )

    def find_similar(self, query: QueryBase) -> Optional[QueryResponse]:
        return QueryResponse(
            user_id=query.user_id,
            query=query.query,
            response="this is a response",
            sources=[],
        )


def override_create_rag_service():
    return MockRAGService()


app.dependency_overrides[create_rag_service] = override_create_rag_service

client = TestClient(app)


def test_api_query():
    response = client.post(
        "/query",
        json={"user_id": "an:id", "query": "was geht?"},
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["user_id"] == "an:id"
    assert data["query"] == "was geht?"
    assert data["response"] == "this is a response"
    assert data["sources"] == []
