from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from todolist_api.schemas import (Message, 
                                  UserDB, 
                                  UserPublic, 
                                  UserSchema, 
                                  UserList)

app = FastAPI(title='FastAPI de To Do List')

db = []


@app.get('/',
         status_code=HTTPStatus.OK,
         response_model=Message)
def read_root():
    return {'message': 'Ola mundo!'}


@app.post('/users/',
          status_code=HTTPStatus.CREATED,
          response_model=UserPublic)
async def create_user(user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(db) + 1)
    db.append(user_with_id)
    return user_with_id


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
async def read_users():
    return {'users': db}

@app.put('/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
async def update_user(user_id: int, user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=user_id)
    
    if user_id < 1 or user_id > len(db):
        raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND, 
                    detail='Nao encontrado'
                      )
    
    db[user_id - 1] = user_with_id

    return user_with_id

@app.delete('/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
async def delete_user(user_id: int):
    if user_id < 1 or user_id > len(db):
        raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND, 
                    detail='Nao encontrado'
                      )
    return db.pop(user_id - 1)

@app.get('/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
async def get_user(user_id: int):
    if user_id < 1 or user_id > len(db):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuario nao encontrado'
        )
    user = db[user_id - 1]
    return user
    