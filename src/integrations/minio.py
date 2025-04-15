import json
from io import BytesIO
from uuid import uuid4

import aiohttp
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from miniopy_async import Minio, S3Error

from conf.config import settings
from src.integrations.logger import logger

minio_client = Minio(
    endpoint=settings.minio.container_endpoint,
    access_key=settings.minio.login,
    secret_key=settings.minio.password,
    secure=False,
)


async def download_document_from_minio(filename: str) -> StreamingResponse:
    """
    Возвращает PDF-документ из MinIO как StreamingResponse.
    Бросает HTTPException(404), если файл не найден.
    """
    try:
        bucket = settings.minio.docs_bucket
        async with aiohttp.ClientSession() as minio_session:
            response = await minio_client.get_object(bucket, filename, session=minio_session)
            file_data = await response.read()
            file_stream = BytesIO(file_data)

        logger.info(f"📤 Документ из MinIO успешно получен: {filename}")

        return StreamingResponse(
            content=file_stream,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )

    except S3Error as e:
        logger.warning(f"❌ Документ не найден в MinIO: {filename}, ошибка: {e}")
        raise HTTPException(status_code=404, detail="Документ не найден")

    except Exception as e:
        logger.error(f"💥 Ошибка при получении документа из MinIO: {e}")
        raise HTTPException(status_code=400, detail="Не удалось получить документ")


async def create_bucket_if_not_exists(bucket_name: str) -> bool:
    try:
        exists = await minio_client.bucket_exists(bucket_name)
        if not exists:
            await minio_client.make_bucket(bucket_name)
            logger.info(f"Bucket '{bucket_name}' created.")
            policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {"AWS": "*"},
                        "Action": ["s3:GetObject"],
                        "Resource": [f"arn:aws:s3:::{bucket_name}/*"],
                    }
                ],
            }

            policy_json = json.dumps(policy)
            await minio_client.set_bucket_policy(bucket_name, policy_json)
            logger.info(f"Public policy set for bucket '{bucket_name}'.")
            return True
        else:
            logger.info(f"Bucket '{bucket_name}' already exists.")
            return False
    except S3Error as e:
        logger.error(f"Error while creating bucket '{bucket_name}': {e}")
        raise Exception("Error creating bucket")


async def upload_document_to_minio(data: BytesIO, content_type: str = "application/pdf") -> str:
    try:
        bucket = settings.minio.docs_bucket
        await create_bucket_if_not_exists(bucket)

        storage_key = f"{uuid4()}.pdf"
        length = data.getbuffer().nbytes

        await minio_client.put_object(
            bucket_name=bucket,
            object_name=storage_key,
            data=data,
            length=length,
            content_type=content_type,
            metadata={"original-name": storage_key},
        )

        logger.info(f"PDF документ загружен в MinIO: {storage_key}")
        return storage_key

    except S3Error as e:
        logger.error(f"Ошибка загрузки PDF в MinIO: {e}")
        raise RuntimeError(f"MinIO error: {e.message}") from e


def get_document_public_url(storage_key: str) -> str:
    return f"http://{settings.minio.outside_endpoint}/{settings.minio.docs_bucket}/{storage_key}"
