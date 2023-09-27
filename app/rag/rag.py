from abc import ABC, abstractmethod
from typing import Optional

from app.core.config import settings

from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import S3DirectoryLoader

import chromadb
from chromadb.config import Settings

from app.schemas.query import DocumentModel, QueryBase, QueryResponse


class RAGService(ABC):  # Interface
    @abstractmethod
    def load_documents(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def query(self, query: QueryBase) -> Optional[QueryResponse]:
        raise NotImplementedError()

    @abstractmethod
    def find_similar(self, query: QueryBase) -> Optional[QueryResponse]:
        raise NotImplementedError()


class LangChainRAGService(RAGService):
    def __init__(self, embedding_model: OpenAIEmbeddings, vector_store: Chroma) -> None:
        self.embedding_model: OpenAIEmbeddings = embedding_model
        self.vector_store: Chroma = vector_store
        self.qa_chain: RetrievalQA = RetrievalQA.from_chain_type(
            llm=OpenAI(),
            chain_type="stuff",
            retriever=vector_store.as_retriever(search_kwargs={"k": 1}),
            return_source_documents=True,
        )

    def load_documents(self) -> bool:
        if self.vector_store._collection.count() > 0:
            return False

        loader = S3DirectoryLoader(
            bucket=settings.S3_BUCKET_DOCUMENTS,
            prefix="",
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCES_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        # TODO thasan add metadatas here...
        chunks_docs = text_splitter.split_documents(docs)
        chuncs_str = [doc.page_content for doc in chunks_docs]
        self.vector_store.add_texts(chuncs_str)
        return True

    def query(self, query: QueryBase) -> Optional[QueryResponse]:
        response = self.qa_chain(query.query)
        answer = response["result"]
        sources = response["source_documents"]
        sources_model = [DocumentModel.from_object(similar_doc) for similar_doc in sources]

        return QueryResponse(
            user_id=query.user_id,
            query=query.query,
            response=answer,
            sources=sources_model,
        )

    def find_similar(self, query: QueryBase) -> Optional[QueryResponse]:
        similar_docs = self.vector_store.similarity_search(query.query, k=3)
        sources_model = [DocumentModel.from_object(similar_doc) for similar_doc in similar_docs]
        return QueryResponse(
            user_id=query.user_id,
            query=query.query,
            response="similarity search, nothing to see here",
            sources=sources_model,
        )


def create_rag_service():
    embedding_model = OpenAIEmbeddings(disallowed_special=())
    chroma_http_client = chromadb.HttpClient(
        host=settings.CHROMADB_HOST,
        port=settings.CHROMADB_PORT,
        settings=Settings(
            chroma_client_auth_provider="chromadb.auth.basic.BasicAuthClientProvider",
            chroma_client_auth_credentials=f"{settings.CHROMADB_USER}:{settings.CHROMADB_PASSWORD}",
        )
        if settings.CHROMADB_USER and settings.CHROMADB_PORT
        else Settings(),
    )
    langchain_chroma = Chroma(
        client=chroma_http_client,
        collection_name="my_collection",
        embedding_function=embedding_model,
    )
    return LangChainRAGService(embedding_model=embedding_model, vector_store=langchain_chroma)
