from fastapi import APIRouter, Response, status
from src.db.sqlAlchemyOrm import deletePosition, listPositions

router = APIRouter()


@router.get("/api/positions")
def listPositionsRoute(title: str, page: int = 1, per_page: int = 10):
    positions = listPositions(title, page, per_page)
    result = list(
        map(
            lambda position: {"id": str(position.id), "title": position.title},
            positions,
        )
    )

    return result


@router.delete("/api/positions/{position_id}")
def deletePositionRoute(position_id: str):
    deletePosition(position_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
