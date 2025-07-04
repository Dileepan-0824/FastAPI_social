from fastapi import status,HTTPException,Depends,APIRouter,responses
from fastapi.security import OAuth2PasswordRequestForm
from .. import models,schemas,utils,oauth2
from ..database import get_db
from sqlalchemy.orm import Session

router=APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/login",response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    #OAuth2PasswordRequestForm is a class that is used to get the username and password from the request
    #username is the email and password is the password
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user or not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    return {"access_token": oauth2.create_access_token(data={"user_id": user.id}), "token_type": "bearer"} #the data to be in payload is created by the create_access_token function and it can be given whatever be it user_id,email,etc.