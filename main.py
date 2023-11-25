from fastapi import FastAPI
from routers import users,products
app = FastAPI()
#Routers
app.include_router(users.router)
app.include_router(products.router)

@app.get('/')
async def hi():
    return {"Saludo": "Hola Mundo"}
