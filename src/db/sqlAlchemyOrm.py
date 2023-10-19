from sqlalchemy import and_, create_engine
from sqlalchemy.orm import sessionmaker
from src.db.entities import Position, Role_permission, User
from src.utils.generatePassword import generatePassword

# CONNECTION_STRING не скрыт, потому что это тестовая база данных для тестового задания.
CONNECTION_STRING = "postgresql://sievqepz:r8th5fzNnMNOrjsJ67T74HkNRzE4xcec@cornelius.db.elephantsql.com"

engine = create_engine(CONNECTION_STRING)
Session = sessionmaker(autoflush=True, expire_on_commit=False, bind=engine)


def createUser(email, position, permissions):
    with Session() as session, session.begin():
        position_id = (
            session.query(Position).filter(Position.title == position).first().id
        )

        newUser = User(
            email=email, password=generatePassword(), position_id=position_id
        )
        session.add(newUser)

    with Session() as session, session.begin():
        for permission in permissions:
            role_permission = Role_permission(user_id=newUser.id, permission=permission)
            session.add(role_permission)

    return newUser.id


def listUsers(email: str, position: str, page: int, per_page: int):
    with Session() as session, session.begin():
        position_id = (
            session.query(Position).filter(Position.title == position).first().id
        )
        search = "%{}%".format(email)
        users = (
            session.query(User)
            .filter(and_(User.email.like(search), User.position_id == position_id))
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

    return users


def listPositions(title: str, page: int = 1, per_page: int = 10):
    with Session() as session, session.begin():
        search = "%{}%".format(title)
        positions = (
            session.query(Position)
            .filter(Position.title.like(search))
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

    return positions


def getUserById(user_id: str):
    with Session() as session, session.begin():
        user = session.query(User).filter(User.id == user_id).first()
        position = (
            session.query(Position).filter(Position.id == user.position_id).first()
        )
        permissions = (
            session.query(Role_permission)
            .filter(Role_permission.user_id == user_id)
            .all()
        )
        mappedPermissions = list(map(lambda p: p.permission, permissions))
        result = {
            "id": user_id,
            "email": user.email,
            "position": position.title,
            "permissions": mappedPermissions,
        }

    return result


def deleteUser(user_id: str):
    with Session() as session, session.begin():
        session.query(User).filter(User.id == user_id).delete()
        session.query(Role_permission).filter(
            Role_permission.user_id == user_id
        ).delete()

    return None


def deletePosition(position_id: str):
    with Session() as session, session.begin():
        session.query(User).filter(User.position_id == position_id).update(
            {User.position_id: None}
        )
        session.query(Position).filter(Position.id == position_id).delete()

    return None


def changeUser(user_id, email, position, permissions):
    with Session() as session, session.begin():
        position_id = (
            session.query(Position).filter(Position.title == position).first().id
        )
        session.query(User).filter(User.id == user_id).update(
            {User.email: email, User.position_id: position_id}
        )
        oldPermissions = (
            session.query(Role_permission)
            .filter(Role_permission.user_id == user_id)
            .all()
        )
        mappedOldPermissions = list(map(lambda p: p.permission, oldPermissions))

        for newPermission in permissions:
            if newPermission not in mappedOldPermissions:
                role_permission = Role_permission(
                    user_id=user_id, permission=newPermission
                )
                session.add(role_permission)

        for oldPermission in mappedOldPermissions:
            if oldPermission not in permissions:
                session.query(Role_permission).filter(
                    Role_permission.permission == oldPermission,
                    Role_permission.user_id == user_id,
                ).delete()

    return None
