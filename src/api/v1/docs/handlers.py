from typing import Annotated

from fastapi import Depends, HTTPException, Query, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.docs.router import docs_router
from src.db.postgres import get_session
from src.integrations.minio import download_document_from_minio
from src.schema.base import Page
from src.schema.info.doc import (
    DocumentCreatedResponse,
    DocumentCreateDTO,
    DocumentFilters,
    DocumentGetDTO,
    DocumentSignedResponse,
    DocumentValidationResponse,
)
from src.services.doc import DocumentService


# Просмотреть все
@docs_router.get("/list", response_model=Page[DocumentGetDTO])
async def get_documents(
    query_filters: Annotated[DocumentFilters, Query()],
    session: AsyncSession = Depends(get_session),
) -> Page[DocumentGetDTO]:
    return await DocumentService.get_all(query_filters, session)


# Скачать файлик из minio
@docs_router.get("/download/{filename}", summary="Скачать PDF-документ")
async def download_document(filename: str) -> StreamingResponse:
    return await download_document_from_minio(filename)


# Создание нового документа (пока что mock)
@docs_router.post("/generate", response_model=DocumentCreatedResponse)
async def generate_document(dto: DocumentCreateDTO, session: AsyncSession = Depends(get_session)) -> DocumentCreatedResponse:
    return await DocumentService.create(dto, session)


# Подписывание документа
@docs_router.post("/sign", response_model=DocumentSignedResponse)
async def sign_document(
    original_file: UploadFile,
    signed_file: UploadFile,
    session: AsyncSession = Depends(get_session),
) -> DocumentSignedResponse:
    try:
        return await DocumentService.sign(original_file, signed_file, session)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Проверка документа
@docs_router.post("/verify", response_model=DocumentValidationResponse)
async def verify_document(file: UploadFile, session: AsyncSession = Depends(get_session)) -> DocumentValidationResponse:
    try:
        return await DocumentService.verify(file, session)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
