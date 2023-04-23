from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status
from cryptography.hazmat.primitives import serialization,padding
from datetime import datetime,timedelta
from schema import Token,TokenData,Login
from config import settings
from utils import get_user
import hashlib
import jwt

ALGORITHM = settings.JWT_ALGORITHM 
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_passwd(passwd:str):
  return hashlib.blake2s(passwd.encode()).hexdigest()

with open('keys/private.pem','rb') as private_key_data:
  private_key = private_key_data.read()

with open('keys/public.pem','r') as public_key_data:
  public_key = public_key_data.read()

password = settings.API_PASSWORD.encode()
private_key_pem = serialization.load_pem_private_key(private_key, password)

api_private_key = private_key_pem.private_bytes(
  encoding=serialization.Encoding.PEM,
  format=serialization.PrivateFormat.PKCS8,
  encryption_algorithm=serialization.NoEncryption()
)

def verify_passwd(plain_passwd,hashed_passwd):
  plain_hash = hash_passwd(plain_passwd)
  if plain_hash == hashed_passwd:
    return True
  else:
    return False
  
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def authenticate_user(username:str,passwd:str):
  user = get_user(username)
  if user is None:
    return False
  if not verify_passwd(passwd,user["password"]):
    return False
  return user


def create_access_token(data:dict):
  to_encode = data.copy()
  expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({"exp":expire})
  encoded_jwt = jwt.encode(to_encode,api_private_key,algorithm=ALGORITHM)
  return encoded_jwt

def decode_access_token(token):
  try:
    payload = jwt.decode(token,public_key,algorithms=[ALGORITHM])
  except jwt.ExpiredSignatureError:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token has expired")
  except jwt.InvalidTokenError:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detai="Token is invalid")
  return payload

async def get_current_user(token:str=Depends(oauth2_scheme)):
  user_data = decode_access_token(token)
  username:str = user_data.get('sub')
  if username is None:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token is invalid")
  token_data = TokenData(username=username)
  user = get_user(username=token_data.username)
  return user

async def get_current_active_user(current_user:Login=Depends(get_current_user)):
  if current_user.disabled:
    raise HTTPException(status_code=400,detail="inactive user")
  return current_user
