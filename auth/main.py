from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, status
from auth import models, schemas, utils
from auth.auth_database import get_db
from jose import jwt, JWTError
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRY_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


app = FastAPI()


@app.post("/signup")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # check user exist or not
    existing_user = (
        db.query(models.User).filter(models.User.username == user.username).first()
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )

    # hash the password
    hashed_pass = utils.hash_password(user.password)

    # New user
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pass,
        role=user.role,
    )

    # save user to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Return the value (excluding password)
    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "role": new_user.role,
    }


@app.post("/login")
def user_login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = (
        db.query(models.User).filter(models.User.username == form_data.username).first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username"
        )

    if not utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
        )

    token_data = {"sub": user.username, "role": user.role}
    token = create_access_token(token_data)
    return {"access_token": token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username = payload.get("sub")
        role = payload.get("role")
        if username is None or role is None:
            raise credential_exception
    except JWTError:
        raise credential_exception
    return {"username": username, "role": role}


@app.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {
        "message": f"Hello, {current_user["username"]} | you accessed a protected route"
    }


def require_roles(allowed_roles: list[str]):
    def role_checker(current_user: dict = Depends(get_current_user)):
        user_role = current_user.get("role")
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="No permission"
            )
        return current_user

    return role_checker


@app.get("/profile")
def user_profile(current_user: dict = Depends(require_roles(["user", "admin"]))):
    return {
        "message": f"Profile of {current_user["username"]} ({current_user["role"]})"
    }


@app.get("/user/dashboard")
def user_dashboard(current_user: dict = Depends(require_roles(["user"]))):
    return {"message": "Welcome User"}


@app.get("/admin/dashboard")
def admin_dashboard(current_user: dict = Depends(require_roles(["admin"]))):
    return {"message": "Welcome Admin"}
