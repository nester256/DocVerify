def page_to_limit_offset(page: int, size: int) -> tuple[int, int]:
    return size, (page - 1) * size


async def get_total_pages(total_items: int, limit: int) -> int:
    return (total_items + limit - 1) // limit
