# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# (수행과제 5) SQLite 데이터베이스 설정
# ./test.db 라는 파일명으로 데이터베이스가 생성됩니다.
SQLALCHEMY_DATABASE_URL = 'sqlite:///./test.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # SQLite는 FastAPI 환경에서 check_same_thread=False가 필요합니다.
    connect_args={'check_same_thread': False}
)

# (수행과제 5) autocommit=False (기본값)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ORM 모델의 기본 클래스가 될 Base
Base = declarative_base()