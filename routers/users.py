from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(tags=['users'], responses={404: {"messages": "Usuario no encotrado"}})

# Entidad User
class User(BaseModel):
    id: int
    name: str
    surname: str | None = None
    username: str
    age: int

users_list = [User(id=1,name='Joel', surname='German', username='JoelG', age=20),
                User(id=2,name='Gabriel', surname='Valdez', username='GabrielV', age=20), 
                User(id=3,name='Juan', surname='Martinez', username='JuanM', age=19)]
#get all
@router.get('/users',status_code=200)
async def users():
    return users_list

#Parameters
@router.get('/users/{id}/') 
async def user(id: int):
   return search_users(id)

#Query
@router.get('/user/')
async def user(id: int):
    return search_users(id)


# Post
@router.post('/user/',response_model=User,status_code=201)
async def new_user(user: User):
    if type(search_users(user.id)) == User:
        raise HTTPException(status_code=204, detail='El usuario ya existe')
    else:
        users_list.append(user)
    return user    


@router.put('/user/')
async def user(user:User):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True  
    if not found:
         raise HTTPException(status_code=404, detail='Usuario no existe')

#Delete

@router.delete('/user/{id}')
async def user_delete(id: int):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index] 
            found = True
            break
    if not found:
         raise HTTPException(status_code=404, detail='Usuario no existe')

def search_users(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0] 
    except Exception as e:
        return {"error": 'Usuario no encontrado'}