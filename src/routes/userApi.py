from fastapi import APIRouter
from src.models import CreateUserRequestDTO
from src.db.sqlAlchemyOrm import createUser, listUsers
from fastapi import Response
import json

router = APIRouter()

@router.get("/api/users")
async def listUsersRoute(email: str, position: str, page: int, per_page: int):
    users = listUsers(email, position, page, per_page)
    result = list(map(lambda user: {"id": str(user.id), "email": user.email, "position": str(user.position_id)}, users))

    return Response(content=json.dumps(result), media_type="application/json")

@router.post("/api/users")
async def createUserRoute(request: CreateUserRequestDTO):
    user_id = createUser(request.email, request.position, request.permissions)
    return {"id": user_id, "email": request.email, "position": request.position, "permissions": request.permissions}