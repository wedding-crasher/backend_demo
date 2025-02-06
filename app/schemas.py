from pydantic import BaseModel, EmailStr
from typing import Opitonal 

# 클라이언트가 보내는 회원가입 요청 데이터 검증 모델 
class UserRegister(BaseModel):
    email: EmailStr
    password: str


#클라이언트에 반환할 사용자 정보 모델
class UserOut(BaseModel):
    id: int
    email: EmailStr


    class Config: 
        orm_mode : True


#JWT 토큰 응답 모델: 로그인 성공시 응답
class Token(BaseModel):
    access_token: str
    token_type : str

