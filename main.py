from fastapi import FastAPI,Request
from routers import transactions,user,authentication,registration

app = FastAPI()

app.title = "Banking"
app.include_router(transactions.router)
app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(registration.router)

@app.get("/")
def home(request:Request):
  return {"message":"root"}


