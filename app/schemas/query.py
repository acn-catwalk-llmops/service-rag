from __future__ import annotations

from pydantic import BaseModel


class DocumentModel(BaseModel):
    page_content: str
    metadata_page: int | None = None
    metadata_source: str | None = None

    @classmethod
    def from_object(cls, doc) -> DocumentModel:
        return DocumentModel(
            page_content=doc.page_content,
            # TODO thasan add once chroma is filled with metadata set
            # metadata_page=similar_doc.metadata["page"],
            # metadata_source=similar_doc.metadata["source"],
        )


class QueryBase(BaseModel):
    user_id: str
    query: str


class QueryResponse(QueryBase):
    response: str
    sources: list[DocumentModel]
