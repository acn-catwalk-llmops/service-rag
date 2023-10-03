from fastapi import Depends, FastAPI

from app.api.api import router
from app.rag.rag import RAGService, create_rag_service

app = FastAPI(title="RAG backend service")

app.include_router(router)


@app.on_event("startup")
def startup_event(rag_service: RAGService = Depends(create_rag_service)):
    """
    Load all the necessary models and data once the server starts.
    """


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
