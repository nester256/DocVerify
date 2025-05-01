import hashlib
import logging
import tempfile
import time
from io import BytesIO

from src.db.postgres import async_session
from src.integrations.minio import upload_document_to_minio
from src.repositories.doc import DocumentRepository
from src.utils.broker import broker
from src.utils.templates.mock_pdf import (  # type: ignore[attr-defined]
    generate_pdf_version_0,
    generate_pdf_version_1,
)

logger = logging.getLogger("docs.generate")


@broker.task(timeout=900)
async def generate_pdf_from_data_async(
    data: dict,  # type: ignore
    version: int,
    doc_id: int,
) -> None:
    async with async_session() as session:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                path = tmp.name

            match version:
                case 0:
                    start = time.monotonic()
                    generate_pdf_version_0(data, path)
                case 1:
                    start = time.monotonic()
                    generate_pdf_version_1(data, path)
                case _:
                    raise ValueError(f"Unsupported version: {version}")

            duration = time.monotonic() - start
            logger.info(f"⏱ Генерация PDF (version={version}) заняла {duration:.3f} сек.")

            with open(path, "rb") as f:
                file_data = f.read()

            file_hash = hashlib.sha256(file_data).hexdigest()

            # Проверка на дубликат
            existing = await DocumentRepository.get_by_hash(file_hash, session)
            if existing:
                logger.warning(f"❗Повтор документа — id: {existing.id}")
                await DocumentRepository.update_generated_data(
                    session=session,
                    doc_id=doc_id,
                    new_hash=None,
                    new_path=None,
                    status="error duplicate",
                )
                await session.commit()
                return

            # Загрузка в MinIO
            buffer = BytesIO(file_data)
            storage_key = await upload_document_to_minio(buffer)

            # Обновление записи
            await DocumentRepository.update_generated_data(
                session=session, doc_id=doc_id, new_hash=file_hash, new_path=storage_key, status="created"
            )
            await session.commit()

        except Exception as e:
            logger.error(f"❌ Ошибка генерации PDF: {e}")
            await session.rollback()
            try:
                await DocumentRepository.update_generated_data(
                    session=session,
                    doc_id=doc_id,
                    new_hash=None,
                    new_path=None,
                    status="error",
                )
                await session.commit()
            except Exception as commit_fail:
                logger.error(f"⚠️ Ошибка при сохранении статуса ошибки: {commit_fail}")
