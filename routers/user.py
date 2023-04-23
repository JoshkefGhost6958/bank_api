from fastapi import FastAPI,Form,Depends,APIRouter
from auth import *
from schema import *
from utils import *
import random

router = APIRouter(
  prefix="/user",
  tags=["User"],
)

attempt = []
count = 3

@router.get("/myaccount")
async def user_acount(user=Depends(get_current_user)):
  sql = "Select * from account where owner_id = %s"
  value = (user["id"],)
  cursor.execute(sql,value)
  user_account = cursor.fetchall()
  accounts = []
  for acc in user_account:
    accounts.append(account(**acc))
  return accounts
@router.get("/createnewaccount",status_code=status.HTTP_201_CREATED)
def create_new_account(pin:int,user=Depends(get_current_user)):
  success = create_account(id=user["id"],pin=pin)
  detail = created_account()
  return account(**detail)

@router.get("/checkbalance")
def check_bal(user=Depends(get_current_user)):
  sql = "select balance from account where owner_id = %s"
  val = (user["id"],)
  cursor.execute(sql,val)
  balance = cursor.fetchone()
  return balance

@router.get("/profile")
def user_credentials(user=Depends(get_current_user)):
  sql = "select * from user where id = %s"
  value = (user["id"],)
  cursor.execute(sql,value)
  user = cursor.fetchone()
  return User(**user)

@router.put("/withdraw")
def withdraw(withdraw:CashWithdrawal,user = Depends(get_current_user)):
  bal = get_balance(withdraw.account)
  if bal is None:
    return {"Error": "account has been locked"}
  new_balance = bal - withdraw.amount
  pin = get_pin(withdraw.account)
  if not verify_passwd(str(withdraw.pin),pin):
    attempt.append(1)
    while(len(attempt) <= 3):
      #break
      global count
      count-=1
      return {"Error":"Pin is incorrect","Attempt":len(attempt),"attempts left":count}
    lock_account(withdraw.account)
    return {"Error":"Pin is incorrect","Attempt":3,"attempts left":0,"State":"Account is locked"}  
  update_balance(new_balance,withdraw.account,user["id"])
  return {"Message":"withdrawal succesfull","balance":new_balance}
  
@router.put("/deposit")
def deposit_cash(deposit:UserCashDeposit,user=Depends(get_current_user)):
  bal = get_balance(deposit.account)
  new_balance = bal + deposit.amount
  update_balance(new_balance,deposit.account,user["id"],)
  return {"Message":"Funds Deposited succesfully","balance":new_balance}

@router.post("/user_to_user_transaction")
def transact(transaction:Transaction,user=Depends(get_current_user)):
  user_account = get_account(transaction.account)
  accounts = get_all_accounts()
  acc_balance = get_balance(user_account)
  pin = get_pin(user["id"])
  if not verify_passwd(transaction.pin,pin):
    attempt.append(1)
    while(len(attempt) <= 3):
      #break
      global count
      count-=1
      return {"Error":"Pin is incorrect","Attempt":len(attempt),"attempts left":count}
    lock_account(transaction.account)
    return {"Error":"Pin is incorrect","Attempt":3,"attempts left":0,"State":"Account is locked"} 
  for i in accounts:
    if transaction.recipient == i["acc_no"]:
      bal1 = get_balance(transaction.recipient)
      nb = acc_balance - transaction.amount
      recipient_bal = bal1 + transaction.amount
      update_balance(nb,user_account,user["id"])
      update_balance(recipient_bal,transaction.recipient,user["id"])
  acc = get_balance(user_account)
  record_transaction(transaction.account,transaction,acc)
  reciept = get_reciept()
  return Reciept(**reciept)



@router.get("/transactions")
def transactions(user=Depends(get_current_user)):
  acc = get_account(user.id)
  query = "select * from transaction where account = %s"
  val = (acc,)
  cursor.execute(query,val)
  reciept = cursor.fetchall()
  return reciept

@router.get("/transactions/{trans_id}")
def get_transaction_by_id(trans_id:int,user=Depends(get_current_user)):
  query = "select * from transaction where transaction_id = %s"
  val = (trans_id,)
  cursor.execute(query,val)
  reciept = cursor.fetchall()
  return reciept
