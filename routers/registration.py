from fastapi import APIRouter
from schema import *
from database import *
import random
from auth import *
from utils import create_user,created_user_id,create_account,created_account,register_online_banking

router = APIRouter(
  prefix="/register",
  tags=["Registration"]
)


@router.post("/",status_code=status.HTTP_201_CREATED)
async def regster(user:CreateAccount):
  user_data = create_user(user)
  id = created_user_id()
  create_account(id,user.pin)
  account = created_account()
  return NewUserAccount(**user_data,**account)

@router.post("/online_banking",status_code=status.HTTP_201_CREATED)
async def online_banking(login:Login):
  user = register_online_banking(login)
  user.update({"Message":"Account created succesfully log in"})
  return user