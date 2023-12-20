from fastapi import FastAPI
from routers import users,products,jwt_auth_users

from fastapi.staticfiles import StaticFiles
app = FastAPI()
#Routers
app.include_router(users.router)
app.include_router(products.router)
app.include_router(jwt_auth_users.router)
#statics
app.mount("/static", StaticFiles(directory="static"), name='static')

@app.get('/')
async def hi():
    return {"Saludo": "Hola Mundo"}
