from fastapi import APIRouter

router = APIRouter()

@router.get("api/positions")
async def read_item(title: str, page: int = 1, per_page: int = 10):
    return []

