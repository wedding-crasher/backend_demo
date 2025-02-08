from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#MY SQL 접속설정 

SQLALCHEMY_DATABASE_URL = (
    "mssql+pyodbc://mw_team:Supermw!@tcp:car-rental-db.database.windows.net,1433/"
    "car_rental_db?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no"
    "&Connection Timeout=30"
)


#SQLALCHEMY 엔진 설정(MY SQL과 연결)
engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_recycle = 3600, # 일정시간 마다 연결을 재활용
        echo = True # 쿼리 로그 출력 ( 디버깅시 권장하니까 씀)
)

#데이터베이스 세션 생셩기 설정(세션: CLIENT-DATABASE 서버간 연결 및 대화, 쿼리의 컨텍스트와 보안, 분리를 보장하는 운영의 일련의 상태, 하나의 세션에 쿼리 여러개, 세션이 여러개일 수 있음)
SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind= engine)

# 모든 모델 클래스가 상속할 베이스 클래스
Base = declarative_base()

# yield가 들어가면 generator 함수. 제너레이터 객체를 생성할때는 값 반환 X, next는 generator나 iterator에서 다음값을 가져오는 함수. 
# Depends없이 쓰면 제너레이터 close호출 못할 수 있음. Finally가 실행되지 않을 수도 있단 소리 
def get_db():
    """
    데이터베이스 세션을 생성하여 반환하는 의존성 함수
    앱 전체에서 재사용 하려고 여기다가 선언
    """
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()