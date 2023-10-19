from fastapi import APIRouter, Response, status
from src.models import ChangeUserRequestDTO, CreateUserRequestDTO
from src.db.sqlAlchemyOrm import (
    changeUser,
    createUser,
    deleteUser,
    getUserById,
    listUsers,
)

router = APIRouter()


@router.get("/api/users")
def listUsersRoute(email: str, position: str, page: int, per_page: int):
    users = listUsers(email, position, page, per_page)
    result = list(
        map(
            lambda user: {
                "id": str(user.id),
                "email": user.email,
                "position": position,
            },
            users,
        )
    )

    return result


@router.post("/api/users")
def createUserRoute(request: CreateUserRequestDTO):
    user_id = createUser(request.email, request.position, request.permissions)

    return {
        "id": user_id,
        "email": request.email,
        "position": request.position,
        "permissions": request.permissions,
    }


@router.get("/api/users/{user_id}")
def getUserByIdRoute(user_id: str):
    user = getUserById(user_id)

    return user


@router.delete("/api/users/{user_id}")
def deleteUserRoute(user_id: str):
    deleteUser(user_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/api/users/{user_id}")
def changeUserRoute(user_id: str, request: ChangeUserRequestDTO):
    changeUser(user_id, request.email, request.position, request.permissions)

    return {
        "id": user_id,
        "email": request.email,
        "position": request.position,
        "permissions": request.permissions,
    }
