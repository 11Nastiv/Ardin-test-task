from sqlalchemy import and_, create_engine
from sqlalchemy.orm import sessionmaker
from src.db.entities import Position, Role_permission, User
from src.utils.generatePassword import generatePassword
from paginate_sqlalchemy import SqlalchemyOrmPage

CONNECTION_STRING = "postgresql://sievqepz:r8th5fzNnMNOrjsJ67T74HkNRzE4xcec@cornelius.db.elephantsql.com"

engine = create_engine(CONNECTION_STRING)
Session = sessionmaker(autoflush = True, expire_on_commit=False, bind=engine)

def createUser(email, position, permissions): 
    with Session() as session, session.begin():
        position_id = session.query(Position).filter(Position.title == position).first().id

        newUser = User(email = email, password = generatePassword(), position_id = position_id)
        session.add(newUser)

    with Session() as session, session.begin():
        for permission in permissions:
            role_permission = Role_permission(user_id = newUser.id, permission = permission)
            session.add(role_permission)

    return newUser.id

def listUsers(email: str, position: str, page: int, per_page: int): 
    with Session() as session, session.begin():
        position_id = session.query(Position).filter(Position.title == position).first().id
        search = "%{}%".format(email)
        users = session.query(User)\
        .filter(and_(User.email.like(search), User.position_id == position_id))\
        .offset((page-1)*per_page)\
        .limit(per_page)\
        .all()

    return users
