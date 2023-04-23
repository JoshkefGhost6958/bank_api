from fastapi import Depends,APIRouter
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from schema import Login
from auth import *

router = APIRouter(
  prefix="/login",
  tags=["Login"],
)

@router.post("/",response_model=Token)
async def login(form_data:OAuth2PasswordRequestForm=Depends()):
  user = authenticate_user(form_data.username,form_data.password)
  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid credentials")
  user_data = Login(**user)
  access_token = create_access_token(data={"sub":user_data.username})
  return {"access_token":access_token,"token_type":"bearer"}
