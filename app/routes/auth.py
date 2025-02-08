from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from jose import jwt
from app import crud, schemas
from app.database import SessionLocal
from app.database import get_db

router = APIRouter()

#JWT 설정 (실제 서비스에선 절대 이렇게 하면 안됨. 나중에 고도화 필욯하면 디플로이에서 심자)
SECRET_KEY = "KT_IS_BETTER_THAN_SKT"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 2400

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    주어진 데이터를 바탕으로 JWT 엑세스 토큰을 생성합니다. 
    만료시간은 expires_delta -> 데모환경이어서 길게줌
    -> | 형태는 union type hinting. 
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    
    else:
        expire = datetime.utcnow() + timedelta(minutes =2400)
    
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt




# 함수 파라미터가 pydantic -> 본문에 있어야, 함수파라미터가 Depends -> 자동으로 의존성 주입
@router.post("/register", response_model = schemas.UserOut, status_code = status.HTTP_201_CREATED)
def register(user: schemas.UserRegister, db: Session = Depends(get_db)):
    """
    회원가입 엔드포인트:
    - 요청으로 받은 이메일과 비밀번호를 바탕으로 사용자를 생성
    - 중복된 이메일이 있으면 400 에러 반환
    """
    
    db_user = crud.get_user_by_email(db, user.email)

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = "해당 이메일은 이미 등록되어 있습니다."
        )

    new_user = crud.create_user(db,user)
    return new_user





@router.post("/login", response_model = schemas.Token)
def login(user: schemas.UserRegister, db: Session = Depends(get_db)):
    db_user = crud.authenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "이메일 또는 비밀번호가 올바르지 않습니다"
        )    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data = {"sub": db_user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}