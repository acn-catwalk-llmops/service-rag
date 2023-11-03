from abc import ABC, abstractmethod
from typing import Optional

import weaviate
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.document_loaders import S3DirectoryLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import VectorStore, Weaviate
import boto3

from app.core.config import settings
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
    def __init__(
        self,
        embedding_model: OpenAIEmbeddings,
        vectorstore_client: weaviate.Client,
        vectorstore_schema_name: str,
        langchain_vectorstore: VectorStore,
        langchain_qa_chain: RetrievalQAWithSourcesChain,
    ) -> None:
        self.embedding_model: OpenAIEmbeddings = embedding_model
        self.vectorstore_client = vectorstore_client
        self.langchain_vectorstore: VectorStore = langchain_vectorstore
        self.langchain_qa_chain: RetrievalQAWithSourcesChain = langchain_qa_chain
        self.schema_name = vectorstore_schema_name

    def load_documents(self) -> bool:
        # self._reset_schema()
        chunked_docs = self._load_documents()
        self.langchain_vectorstore.add_documents(chunked_docs)
        return True

    def _reset_schema(self):
        doc_schema = {
            "class": self.schema_name,
            "vectorizer": "text2vec-openai",
            "vectorIndexConfig": {
                "distance": "cosine",
            },
            "properties": [
                {"name": "text", "dataType": ["text"], "tokenization": "word"},
                {"name": "source", "dataType": ["text"]},
            ],
        }

        self.vectorstore_client.schema.delete_class(
            self.schema_name
        )  # TODO thasan catch exception if not existent
        self.vectorstore_client.schema.create_class(doc_schema)

    def _load_documents(self):
        # TODO thasan abstract document loading
        session = boto3.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        sts = session.client("sts")
        response = sts.assume_role(
            RoleArn=settings.AWS_ROLE_ARN_TO_ASSUME, RoleSessionName="service-rag-session"
        )
        loader = S3DirectoryLoader(
            bucket=settings.S3_BUCKET_DOCUMENTS,
            prefix="",
            region_name=settings.AWS_REGION,
            aws_access_key_id=response["Credentials"]["AccessKeyId"],
            aws_secret_access_key=response["Credentials"]["SecretAccessKey"],
            aws_session_token=response["Credentials"]["SessionToken"],
        )
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunked_docs = text_splitter.split_documents(docs)
        return chunked_docs

    def query(self, query: QueryBase) -> Optional[QueryResponse]:
        # response = self.langchain_qa_chain({"query": query.query})  # this is for RetrievalQA
        response = self.langchain_qa_chain({"question": query.query})
        answer = response["answer"]
        sources = response["source_documents"]
        sources_model = [DocumentModel.from_object(similar_doc) for similar_doc in sources]

        return QueryResponse(
            user_id=query.user_id,
            query=query.query,
            response=answer,
            sources=sources_model,
        )

    def find_similar(self, query: QueryBase) -> Optional[QueryResponse]:
        # similar_docs = self.vector_store.similarity_search(query.query, k=3)
        similar_docs = self.langchain_vectorstore.similarity_search(query.query, by_text=False)
        sources_model = [DocumentModel.from_object(similar_doc) for similar_doc in similar_docs]
        return QueryResponse(
            user_id=query.user_id,
            query=query.query,
            response="similarity search, nothing to see here",
            sources=sources_model,
        )


def create_rag_service():
    WEAVIATE_SCHEMA_NAME = "Document"
    embedding_model = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
    # note that we also specify 'text2vec-openai' in the Weaviate Document schema.
    # Consequences of diverging values are unknown.
    # TODO thasan activate weaviate authentication
    weaviate_client = weaviate.Client(
        url=f"http://{settings.VECTORSTORE_HOST}:{settings.VECTORSTORE_PORT}",
        additional_headers={"X-OpenAI-Api-Key": settings.OPENAI_API_KEY},
    )
    langchain_vectorstore = Weaviate(
        weaviate_client,
        index_name=WEAVIATE_SCHEMA_NAME,
        text_key="text",
        attributes=["source"],
        embedding=embedding_model,
    )

    qa_chain = RetrievalQAWithSourcesChain.from_chain_type(
        llm=OpenAI(),
        chain_type="stuff",
        retriever=langchain_vectorstore.as_retriever(search_kwargs={"k": 1}),
        return_source_documents=True,
    )

    return LangChainRAGService(
        embedding_model=embedding_model,
        vectorstore_client=weaviate_client,
        vectorstore_schema_name=WEAVIATE_SCHEMA_NAME,
        langchain_vectorstore=langchain_vectorstore,
        langchain_qa_chain=qa_chain,
    )


# def create_rag_service_chroma():
#     embedding_model = OpenAIEmbeddings()
#     vectorstore_client = chromadb.HttpClient(
#         host=settings.VECTORSTORE_HOST,
#         port=settings.VECTORSTORE_PORT,
#         settings=Settings(
#             chroma_client_auth_provider="chromadb.auth.basic.BasicAuthClientProvider",
#             chroma_client_auth_credentials=f"{settings.VECTORSTORE_USER}:{settings.VECTORSTORE_PASSWORD}",
#         )
#         if settings.VECTORSTORE_USER and settings.VECTORSTORE_PORT
#         else Settings(),
#     )
#     langchain_vectorstore = Chroma(
#         client=vectorstore_client,
#         collection_name="my_collection",
#         embedding_function=embedding_model,
#     )

#     qa_chain = RetrievalQA.from_chain_type(
#         llm=OpenAI(),
#         chain_type="stuff",
#         retriever=langchain_vectorstore.as_retriever(search_kwargs={"k": 1}),
#         return_source_documents=True,
#     )
#     return LangChainRAGService(
#         embedding_model=embedding_model,
#         vectorstore_client=vectorstore_client,
#         vector_store=langchain_vectorstore,
#         qa_chain=qa_chain,
#     )
