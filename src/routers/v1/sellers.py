from fastapi import APIRouter, Depends, Response, status
from icecream import ic

from src.schemas import IncomingSeller, ReturnedAllSellers, CertainSeller
from fastapi.responses import ORJSONResponse

sellers_router = APIRouter(tags=["sellers"], prefix="/sellers")

#Временная симуляция хранилища fake_sellers #TODO перенести в формат бд все  
fake_sellers = {}
COUNTER = 0

#Ручка для создания продавца, возвращает созданного продавца
@sellers_router.post("/",response_model=CertainSeller, status_code=status.HTTP_201_CREATED)
async def create_seller(
    seller: IncomingSeller
):
    global COUNTER
    new_sellers = {
        "id": COUNTER,
        "password": seller.password,
        "first_name": seller.first_name,
        "last_name": seller.last_name,
        "email": seller.email
    }

    fake_sellers[COUNTER] = new_sellers
    COUNTER += 1

    return fake_sellers[COUNTER - 1]
    # return ORJSONResponse(
    #     new_sellers
    # )

#Ручка для получения списка всех продавцов
@sellers_router.get("/", response_model=ReturnedAllSellers)
async def get_all_sellers():
    sellers = list(fake_sellers.values())
    return {"sellers": sellers}

#Ручка для получения конретного продавца
@sellers_router.get("/{seller_id}", response_model=CertainSeller)
async def get_seller(seller_id: int):
    return fake_sellers[seller_id]

#Ручка для обновления данных о продавце
@sellers_router.put("/{seller_id}", response_model=CertainSeller)
async def update_seller(seller_id: int, seller: CertainSeller):
    if _ := fake_sellers.get(seller_id, None):
        fake_sellers[seller_id] = seller

    return fake_sellers[seller_id]

#Ручка для удаления продавцов
#TODO надо также при удаление продавца реализовать удаление соотвествующих книг
@sellers_router.delete("/{seller_id}")
async def delete_seller(seller_id: int):
    deleted_seller = fake_sellers.pop(seller_id, -1)
    ic(deleted_seller)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
