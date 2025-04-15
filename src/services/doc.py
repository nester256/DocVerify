import asyncio
import tempfile
from io import BytesIO

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.integrations.logger import logger
from src.integrations.minio import get_document_public_url, upload_document_to_minio

from ..models.document import Document
from ..repositories.doc import DocumentRepository
from ..schema.base import Page
from ..schema.info.doc import (
    DocumentCreatedResponse,
    DocumentCreateDTO,
    DocumentFilters,
    DocumentGetDTO,
    DocumentSignedResponse,
    DocumentValidationResponse,
)
from ..utils.generate_pdf import generate_pdf_from_data
from ..utils.pagination import get_total_pages, page_to_limit_offset


class DocumentService:
    @staticmethod
    async def create(dto: DocumentCreateDTO, session: AsyncSession) -> DocumentCreatedResponse:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            path = tmp_file.name
            await asyncio.to_thread(generate_pdf_from_data, dto.model_dump(), path)

        hash_ = await DocumentRepository.calculate_sha256(path)

        with open(path, "rb") as f:
            file_data = BytesIO(f.read())

        storage_key = await upload_document_to_minio(file_data)
        link_to_download = get_document_public_url(storage_key)

        doc = await DocumentRepository.create(session, hash_, storage_key)

        return DocumentCreatedResponse(
            id=doc.id,
            original_document_hash=doc.original_document_hash,
            link_to_download=link_to_download,
        )

    @staticmethod
    async def sign(original_file: UploadFile, signed_file: UploadFile, session: AsyncSession) -> DocumentSignedResponse:
        try:
            logger.info("📥 Получен оригинальный и подписанный файл на подпись")

            # 1. Проверка MIME-типов
            if original_file.content_type != "application/pdf":
                logger.warning(f"⛔ Неверный формат оригинального файла: {original_file.content_type}")
                raise ValueError("Оригинальный файл должен быть в формате PDF")

            if signed_file.content_type != "application/pdf":
                logger.warning(f"⛔ Неверный формат подписанного файла: {signed_file.content_type}")
                raise ValueError("Подписанный файл должен быть в формате PDF")

            # --- ORIGINAL FILE ---
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as original_tmp:
                original_path = original_tmp.name
                original_content = await original_file.read()
                original_tmp.write(original_content)

            logger.info(f"📄 Оригинал сохранён: {original_path}")
            original_hash = await DocumentRepository.calculate_sha256(original_path)
            logger.info(f"🔍 Хеш оригинала: {original_hash}")

            doc = await DocumentRepository.get_by_hash(original_hash, session)
            if not doc:
                logger.warning("❌ Оригинальный документ не найден")
                raise ValueError("Оригинальный документ не зарегистрирован")

            # 2. Запрещаем повторную подпись
            if doc.is_signed:
                logger.warning(f"🚫 Попытка повторной подписи уже подписанного документа (id={doc.id})")
                raise ValueError("Этот документ уже был подписан ранее")

            # --- SIGNED FILE ---
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as signed_tmp:
                signed_path = signed_tmp.name
                signed_content = await signed_file.read()
                signed_tmp.write(signed_content)

            logger.info(f"📄 Подписанный файл сохранён: {signed_path}")
            signed_hash = await DocumentRepository.calculate_sha256(signed_path)
            logger.info(f"🔐 Хеш подписанного файла: {signed_hash}")

            # 3. Проверка дубликата среди уже подписанных
            existing = await DocumentRepository.get_by_signed_hash(signed_hash, session)
            if existing:
                logger.warning(f"❌ Подписанный документ уже существует (id={existing.id})")
                raise ValueError("Этот подписанный файл уже зарегистрирован")

            # 4. Загрузка в MinIO
            signed_io = BytesIO(signed_content)
            storage_key = await upload_document_to_minio(signed_io)
            logger.info(f"☁️ Загружен в MinIO: {storage_key}")

            updated = await DocumentRepository.add_signature(session, doc, storage_key, signed_hash)
            logger.info(f"✅ Успешно обновлён документ (id={updated.id})")

            return DocumentSignedResponse(
                id=updated.id,
                signed_document_hash=signed_hash,
            )

        except ValueError as ve:
            logger.warning(f"⚠️ Ошибка в логике подписи: {ve}")
            raise ve

        except Exception as e:
            logger.error(f"❌ Неизвестная ошибка при подписи: {e}")
            raise ValueError("Не удалось завершить процесс подписи. Повторите позже или проверьте данные.")

    @staticmethod
    async def verify(uploaded_file: UploadFile, session: AsyncSession) -> DocumentValidationResponse:
        try:
            logger.info(f"📥 Загружен файл для проверки подписи: {uploaded_file.filename}")

            # 1. Проверка типа файла
            if uploaded_file.content_type != "application/pdf":
                logger.warning(f"⛔ Неверный формат файла: {uploaded_file.content_type}")
                raise ValueError("Файл должен быть в формате PDF")

            # 2. Сохраняем во временный файл
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp_path = tmp.name
                content = await uploaded_file.read()
                tmp.write(content)

            logger.info(f"📄 Временный файл сохранён как {tmp_path}")

            # 3. Считаем хеш
            hash_ = await DocumentRepository.calculate_sha256(tmp_path)
            logger.info(f"🔍 Хеш файла: {hash_}")

            # 4. Ищем по signed_document_hash
            doc = await DocumentRepository.get_by_signed_hash(hash_, session)

            if doc is not None:
                logger.info(f"✅ Документ валиден: найден в базе (id={doc.id})")
                return DocumentValidationResponse(valid=True)
            else:
                logger.warning("❌ Документ не найден: подпись не зарегистрирована")
                return DocumentValidationResponse(valid=False)

        except ValueError as ve:
            logger.warning(f"⚠️ Ошибка валидации: {ve}")
            raise ve

        except Exception as e:
            logger.error(f"❌ Неизвестная ошибка при проверке подписи: {e}")
            raise ValueError("Не удалось проверить подпись. Убедитесь, что файл корректный.")

    @classmethod
    async def get_all(
        cls,
        query_filters: DocumentFilters,
        session: AsyncSession,
    ) -> Page[DocumentGetDTO]:
        limit, offset = page_to_limit_offset(query_filters.page, Document.__page_size__)
        docs, total = await DocumentRepository.get_all(
            query_filters=query_filters,
            limit=limit,
            offset=offset,
            session=session,
        )
        return Page(
            data=[DocumentGetDTO.model_validate(doc) for doc in docs],
            total_pages=await get_total_pages(total, Document.__page_size__),
        )
