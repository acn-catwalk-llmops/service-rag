from __future__ import annotations

from langchain.schema.document import Document
from pydantic import BaseModel


class DocumentModel(BaseModel):
    page_content: str
    metadata_source: str | None = None

    @classmethod
    def from_object(cls, doc: Document) -> DocumentModel:
        return DocumentModel(
            page_content=doc.page_content,
            metadata_source=doc.metadata["source"],
        )


class QueryBase(BaseModel):
    user_id: str
    query: str


class QueryResponse(QueryBase):
    response: str
    sources: list[DocumentModel]
