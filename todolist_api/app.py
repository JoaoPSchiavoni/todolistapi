from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from todolist_api.database import get_session
from todolist_api.models import User
from todolist_api.schemas import (
    Message,
    UserList,
    UserPublic,
    UserSchema,
)

app = FastAPI(title='FastAPI de To Do List')


# GET
@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Ola mundo!'}


# POST
@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
async def create_user(user: UserSchema, session=Depends(get_session)):

    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )
    if db_user:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already registered',
        )
    new_user = User(**user.model_dump())

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user


# GET
@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
async def read_users(
    skip: int = 0, limit: int = 100, session=Depends(get_session)
):
    users = session.scalars(select(User).limit(limit).offset(skip))
    return {'users': users}


# PUT
@app.put(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
async def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    try:
        db_user.email = user.email
        db_user.username = user.username
        db_user.password = user.password

        session.commit()
        session.refresh(db_user)

        return db_user

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already exists',
        )


# DELETE
@app.delete(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=Message
)
async def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    session.delete(db_user)
    session.commit()

    return {'message': 'User deleted'}


# GET
@app.get(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
async def get_user_by_id(
    user_id: int, session: Session = Depends(get_session)
):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return db_user
