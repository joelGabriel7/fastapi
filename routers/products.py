from fastapi import APIRouter, HTTPException

router = APIRouter(prefix='/products', tags=['products'], responses={404: {"messages": 'no encontrado'}})

product_lists = ['Carrito', 'TV', 'Table', 'PC']

@router.get('/')
async def products():
    return product_lists

@router.get('/{id}')
async def products(id: int):
    return product_lists[id - 1]