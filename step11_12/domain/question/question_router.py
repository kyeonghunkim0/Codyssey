from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
# step11 폴더 내의 database.py 및 models.py를 참조
from database import SessionLocal
from models import Question


# 데이터베이스 세션 관리를 위한 제너레이터 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 라우터 정의 및 prefix 설정
router = APIRouter(
    prefix = '/api/question',
)


# 목록을 가져오는 question_list() 함수 (GET 메소드)
@router.get('/')
def question_list(db: Session = Depends(get_db)):
    """
    SQLite에 저장된 전체 질문 목록을 최신순(create_date 기준 내림차순)으로 가져옵니다. (ORM 사용)
    """
    # ORM을 사용하여 Question 모델의 모든 데이터를 create_date 내림차순으로 조회
    # PEP 8 규칙에 따라 함수 이름은 소문자 및 언더라인(_) 사용
    question_list = db.query(Question).order_by(Question.create_date.desc()).all()
    
    # 쿼리 결과를 반환
    return question_list