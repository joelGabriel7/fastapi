from fastapi import FastAPI
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
@app.get('/users')
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


def search_users(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0] 
    except Exception as e:
        return {"error": 'Usuario no encontrado'}
