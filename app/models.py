from sqlalchemy import Column, Integer, String
from .database import Base


# User 테이블 정의하는 SQLALchemy 모델
# Base를 상속받아, SqlAlchemy의 ORM (객체-관계 매핑)기능을 사용함함
class User(Base):
    __tablename__ = "users"

    #컬럼에 Index를 적용하여 검색기능 높임
    id = Column(Integer, primary_key=True, index = True)
    email = Column(String(255), unique=True, index = True, nullable = False)
    hashed_password = Column(String(255), nullable = False)

    