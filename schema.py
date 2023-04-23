from pydantic import BaseModel
from typing import Union,Optional

class account(BaseModel):
  acc_id: int
  acc_no: int
  card_no: int
  balance: int
  card_is_valid: Union[bool,None] = None

class AccountOut(account):
  pass

class User(BaseModel):
  fname:str
  lname:str
  age:int
  national_id:int
  kra_pin: str


class userOut(BaseModel):
  fname:str
  lname:str


class Login(BaseModel):
  id:int or None=None
  username:str
  password: str
  disabled: bool

class CreateAccount(User):
  pin: int

class NewUserAccount(User,account):
  id:int
  Message:str="Please set up an online account to access your bank"
  

class CreatedAccount(BaseModel):
  owner:userOut
  account:account


class Transaction(BaseModel):
  account:int
  amount:int
  recipient: int
  pin:int
  transaction_type:int
  class Config:
    schema_extra={
      "example":{
        "amount":4999,
        "recipient":1120019,
        "pin":0000,
        "transaction_type":1
      }
    }

class Reciept(BaseModel):
  account:int
  amount:int
  recipient: int
  transaction_type: int
  time:str
  


class CashDeposit(BaseModel):
  acc_no: int
  amount: int
  class Config:
    schema_extra={
      "example":{
        "account no":2231100,
        "amount": 400000
      }
    }

class UserCashDeposit(BaseModel):
  account:int
  amount: int

class CashWithdrawal(BaseModel):
  account: int
  amount: int
  pin: int

class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  username:str or None = None