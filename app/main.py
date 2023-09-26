from fastapi import FastAPI

from app.api.api import router

from app.core.config import settings

app = FastAPI(title="RAG backend service")

app.include_router(router)


@app.on_event("startup")
def startup_event():
    """
    Load all the necessary models and data once the server starts.
    """
    print(settings.CHROMADB_HOST)
    # app.directory = '/app/content/'
    # app.documents = load_docs(app.directory)
    # app.docs = split_docs(app.documents)

    # app.embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    # app.persist_directory = "chroma_db"

    # app.vectordb = Chroma.from_documents(
    #     documents=app.docs,
    #     embedding=app.embeddings,
    #     persist_directory=app.persist_directory
    # )
    # app.vectordb.persist()

    # app.model_name = "gpt-3.5-turbo"
    # app.llm = ChatOpenAI(model_name=app.model_name)

    # app.db = Chroma.from_documents(app.docs, app.embeddings)
    # app.chain = load_qa_chain(app.llm, chain_type="stuff", verbose=True)


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
