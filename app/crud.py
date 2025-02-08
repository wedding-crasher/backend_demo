from sqlalchemy.orm import Session
from .models import User
from .schemas import UserRegister
from passlib.context import CryptContext


#비밀번호 해싱 및 검증을 위한 컨텍스트(bcrypt 사용)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def get_user_by_email(db: Session, email:str):
    """
    이메일에 해당하는 사용자를 조회합니다. 
    """
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserRegister):
    """
    회원 가입 유저 데이터 바탕으로 새 사용자 생성
    비밀번호는 해싱해 저장
    """
    hashed_password = pwd_context.hash(user.password)
    #db에 들어갈 유저 객체 
    db_user = User(email = user.email, hashed_password = hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    입력된 비밀번호가 해싱된 비밀번호와 일치하는지 검증
    """
    return pwd_context.verify(plain_password,hashed_password)


def authenticate_user(db:Session, email:str, password:str):
    """
    주어진 이메일과 비밀번호로 사용자를 인증합니다. 
    인증에 실패하면  False, 성공하면 User 객체 던져주기
    """


    #검증로직: 1) 유저있나 체크 2) 패스워드 검증 3) 유저 리턴
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


