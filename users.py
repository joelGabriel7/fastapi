from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

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
@app.get('/users',status_code=200)
async def users():
    return users_list

#Parameters
@app.get('/users/{id}/') 
async def user(id: int):
   return search_users(id)

#Query
@app.get('/user/')
async def user(id: int):
    return search_users(id)


# Post

@app.post('/user/',response_model=User,status_code=201)
async def new_user(user: User):
    if type(search_users(user.id)) == User:
        raise HTTPException(status_code=204, detail='El usuario ya existe')
    else:
        users_list.append(user)
    return user    


@app.put('/user/')
async def user(user:User):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    return user        
    if not found:
         return {"error": 'Usuario no encontrado'}

#Delete

@app.delete('/user/{id}')
async def user_delete(id: int):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index] 
            found = True
            break
    if not found:
        return {"error": 'No se ha eliminado el usuario'}

def search_users(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0] 
    except Exception as e:
        return {"error": 'Usuario no encontrado'}