from fastapi import FastAPI,Request
from routers import transactions,user,authentication,registration
from fastapi.security.cors import CORSMiddleware
app = FastAPI()

app.title = "Banking"
app.include_router(transactions.router)
app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(registration.router)
origins=[
  "http://localhost"
]

app.add_middleware(CORSMiddleware,
                  allowed_origins=origins)


@app.get("/")
def home(request:Request):
  return {"message":"root"}


