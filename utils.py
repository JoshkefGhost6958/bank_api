from schema import *
from database import conn,cursor
import random

def hash_passwd(passwd:str):
  return hashlib.blake2s(passwd.encode()).hexdigest()

def get_user(username:str):
  sql = "select * from login where username = %s"
  value = (username,)
  cursor.execute(sql,value)
  user = cursor.fetchone()
  return user


def get_all_accounts():
  sql = "select acc_no from account"
  cursor.execute(sql)
  accounts = cursor.fetchall()
  return accounts

def get_account(owner_id:int):
  user_account = "select acc_no from account where owner_id = %s"
  id = (owner_id,)
  cursor.execute(user_account,id)
  account = cursor.fetchone()
  return account["acc_no"]

def get_balance(account):
  sql = "select balance from account where acc_no = %s"
  val = (account,)
  cursor.execute(sql,val)
  balance = cursor.fetchone()
  return balance["balance"]

def get_pin(account):
  sql = "select pin from account where acc_no= %s"
  val = (account,)
  cursor.execute(sql,val)
  pin = cursor.fetchone()
  return pin["pin"]

def update_balance(bal:int,account:int,owner_id:int):
  sql = "update account set balance = %s where acc_no = %s and owner_id=%s and is_active=1"
  vals = (bal,account,owner_id)
  cursor.execute(sql,vals)
  conn.commit()
  return {"Message":"Balance updated succesfully"}

def create_user(user:User):
  sql= "insert into user(fname,lname,age,national_id,kra_pin) values(%s,%s,%s,%s,%s)"
  values = (user.fname,user.lname,user.age,user.national_id,user.kra_pin,)
  cursor.execute(sql,values)
  conn.commit()
  user_data = "select * from user where id = last_insert_id()"
  cursor.execute(user_data)
  user_dict = cursor.fetchone()
  return user_dict

def created_user_id():
  user = "select id from user where id = last_insert_id()"
  cursor.execute(user)
  user_id = cursor.fetchone()
  id = user_id["id"]
  return id


def register_online_banking(login):
  online_log = "insert into login values(%s,%s,%s,%s)"
  disabled = 1
  hashed_pass = hash_passwd(login.password)
  log_cred = (login.id,str(login.username),str(hashed_pass),disabled,)
  cursor.execute(online_log,log_cred)
  conn.commit()
  return {"username":login.username}
  

def create_account(id,pin):
  card_no = random.randint(3367773333,5003344455)
  acc_no = random.randint(1000000,4000000)
  sql2 = "insert into account(owner_id,acc_no,card_no,pin,balance,card_is_valid) values(%s,%s,%s,%s,%s,%s)"
  pin = hash_passwd(str(pin))
  vals = (id,acc_no,card_no,pin,0.0,True,)
  cursor.execute(sql2,vals)
  conn.commit()
  return 201


def created_account():
  acc = "select * from account where acc_id = last_insert_id()"
  cursor.execute(acc)
  account = cursor.fetchone()
  return account

def lock_account(account):
  sql= "Update account set is_active = false where acc_no = %s"
  val = (account,)
  cursor.execute(sql,account)
  conn.commit()
  return {"Message":"account has been locked"}

def get_reciept():
  recieptQuery = "select * from transaction where transaction_id = last_insert_id()"
  cursor.execute(recieptQuery)
  reciept = cursor.fetchone()
  return reciept

def record_transaction(account,transaction:Transaction,balance):
  postEvent = "insert into transaction(account,recipient,amount,type,balance) values(%s,%s,%s,%s,%s)" 
  values = (account,transaction.recipient,transaction.amount,transaction.transaction_type,balance,)
  cursor.execute(postEvent,values)
  conn.commit()

