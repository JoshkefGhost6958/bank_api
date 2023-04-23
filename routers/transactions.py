from fastapi import FastAPI,Form,Depends,APIRouter
from schema import *
from database import conn,cursor
from typing import Annotated
#from fastapi.security import OAuth2PasswordBearer
import random
from auth import *
from utils import *


router = APIRouter(
  tags=["Transactions"]
)

attempt = []
count = 3

@router.put("/deposit")
def deposit_cash(deposit:CashDeposit):
  balance = "select balance from account where acc_no = %s"
  bal_val = (deposit.acc_no,)
  cursor.execute(balance,bal_val)
  bal = cursor.fetchone()
  new_balance = bal["balance"] + deposit.amount
  sql = "update account set balance = %s where acc_no = %s"
  val = (new_balance,deposit.acc_no)
  cursor.execute(sql,val)
  conn.commit()
  return {"Message":"Funds Deposited succesfully","balance":new_balance}
#/files/{file_path:path}


