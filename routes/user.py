from fastapi import APIRouter, HTTPException, status,Depends
from models.user import BaseUser
from typing import List,Annotated
from passlib.context import CryptContext
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials,OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models.sessions import Session
from datetime import timedelta,datetime
from jose import JWTError, jwt

user_router = APIRouter(prefix="/users",tags=["User"])

users=dict()
mycontext = CryptContext(schemes=["sha256_crypt", "md5_crypt"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@user_router.get('/', response_model=List[BaseUser])
def get_users():
    return list(users.values())



@user_router.post('/', status_code=status.HTTP_201_CREATED)

def create_user(user: BaseUser):

    if user.username in users:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    user.password=mycontext.hash(user.password)
    users[user.username]=user
    return user


@user_router.get('/{username}', response_model=BaseUser)

def get_user(username: str):

    user=users.get(username)

    if not user: 

        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return user


@user_router.put('/{username}')

def update_user(username: str, user_new):

    user_pr=users.get(username)

    if not user_pr: 

        raise HTTPException(status.HTTP_404_NOT_FOUND)

    users[user_new.username]=user_new

    return {'message':'User updated'}


@user_router.delete('/{username}')
def delete_post(username: str):
    user=users.get(username)
    if not user: 
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    users.pop(username)
    return {'message':'user deleted'}   

def encode_access_token(data:dict):
    SECRET_KEY = "YOUR-SECRET-KEY"
    ALGORITHM = "HS256"
    expire = datetime.utcnow() + timedelta(minutes=60)    
    data.update({'expire_date':datetime.strftime(expire, '%Y %m %d')})
    encoded_token = jwt.encode(data,str(SECRET_KEY),algorithm=ALGORITHM)
    return encoded_token


def decode_access_token(token:str):
    SECRET_KEY = "YOUR-SECRET-KEY"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    try:
        decoded_token=jwt.decode(token,str(SECRET_KEY),ALGORITHM)
        username=decoded_token.get("username")
        # role=decoded_token.get("role")
    except Exception:
        raise HTTPException(status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},)
    else:
        return username

def get_current_user(token:str=Depends(oauth2_scheme)):
    
    username=decode_access_token(token)
    if not username in users:
        raise HTTPException(status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},)
    else:
        return users[username]

# @user_router.post("/")

# @user_router.post('/', status_code=status.HTTP_201_CREATED)

# def login(user: BaseUser):

#     session = Session(1,'Ali')

def authenticate_user(username,password):
    user = get_user(username)
    if mycontext.verify(password,user.password) :
        return user
    else : 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect password")

@user_router.post("/Login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password)
    access_token = encode_access_token(data={'sub': user.username})
    return {"access_token": access_token, "token_type": "bearer"}


