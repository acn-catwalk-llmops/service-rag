from fastapi import APIRouter, Depends, Response, status

from app.rag.rag import RAGService, create_rag_service
from app.schemas.query import QueryBase, QueryResponse

router = APIRouter()


@router.post("/query", status_code=201, response_model=QueryResponse)
def query(query: QueryBase, rag_service: RAGService = Depends(create_rag_service)):
    """
    Query the Service
    """
    return rag_service.query(query)


@router.post("/find_similar", status_code=201, response_model=QueryResponse)
def find_similar(query: QueryBase, rag_service: RAGService = Depends(create_rag_service)):
    """
    Find similar documents
    """
    return rag_service.find_similar(query)


@router.get("/load_docs", status_code=200)
def load_docs(response: Response, rag_service: RAGService = Depends(create_rag_service)):
    """
    Load the documents from S3 into the VectorStore
    """
    loaded = rag_service.load_documents()
    if not loaded:
        response.status_code = status.HTTP_204_NO_CONTENT
