from fastapi import Depends, APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt,JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_tOKEN_DURATION = 1
SECRET_KEY = "7496adc39cfd16b6010d32b164b6284fc4264a6ac868a317b369c6c16e428bb6"
router = APIRouter(prefix='/auth', tags=['Authenticate'])
oauth2 = OAuth2PasswordBearer(tokenUrl='login')

crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
    username: str
    fullname: str
    email: str
    disabled: bool


class UserDB(User):
    password:str    

users_db = {
    "joelG":{
        "username":"joelG",
        "fullname":"Joel Germán",
        "email":"joelgerman671@gmail.com",
        "disabled":False,
        "password":"$2a$12$5j3pV/BYT1pk2YuE200/eOVJDQxhqFzXuZvXuAkali2fDe7BuErLq"
    },

    "gabrielV":{
        "username":"gabrielV",
        "fullname":"Gabriel Valdez",
        "email":"Gabrielvaldez671@gmail.com",
        "disabled":True,
        "password":'$2a$12$OyOxKn8QLlXWoNCW5ayV4uhZ5dULI96njtfne5H1HfkAEk6opWYgq'
    },
}


def search_user_db(username:str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username:str):
    if username in users_db:
        return User(**users_db[username])    
        
async def auth_user(token:str = Depends(oauth2)):
    exception = HTTPException(
        status_code=401,
        detail="No fue posible validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )    
    try:
        username = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM]).get('sub')
        if username is None:
            raise exception   
    except JWTError:
        raise exception
  

    return search_user(username)
    
async def current_user(user:User= Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=400,
            detail="Usuario inactivo",
        )
    return user

@router.post("/login")
async def login_access_token(form: OAuth2PasswordRequestForm = Depends()): 
    user_db = users_db.get(form.username)
    if not user_db:
         raise HTTPException(
             status_code=404, detail='El usuario no es correcto')
    user = search_user_db(form.username)
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=400, detail='La contraseña no es correcta')
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_tOKEN_DURATION)
    access_token = {"sub": user.username, "exp": expire}
    encode_token = jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHM)
    
    return {"access_token": encode_token, "token_type" : "bearer"}    

@router.get('/users/me')
async def me(user:User = Depends(current_user)):
    return user
