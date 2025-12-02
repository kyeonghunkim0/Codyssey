from fastapi import APIRouter, Depends
import datetime
from sqlalchemy.orm import Session
# step11 폴더 내의 database.py 및 models.py를 참조
from database import get_db
from models import Question as QuestionModel
from domain.question import question_schema

# 라우터 정의 및 prefix 설정
router = APIRouter(
    prefix = '/api/question',
)


# 목록을 가져오는 question_list() 함수 (GET 메소드)
@router.get('/', response_model=list[question_schema.Question])
def question_list(db_manager=Depends(get_db)):
    """
    SQLite에 저장된 전체 질문 목록을 최신순(create_date 기준 내림차순)으로 가져옵니다. (ORM 사용)
    """
    # contextlib을 사용한 의존성 주입
    with db_manager as db:
        # ORM을 사용하여 Question 모델의 모든 데이터를 create_date 내림차순으로 조회
        # PEP 8 규칙에 따라 함수 이름은 소문자 및 언더라인(_) 사용
        _question_list = db.query(QuestionModel).order_by(QuestionModel.create_date.desc()).all()
        
        # 쿼리 결과를 반환
        return _question_list


@router.post("/create", status_code=204)
def question_create(_question_create: question_schema.QuestionCreate, db_manager=Depends(get_db)):
    """
    질문 등록
    """
    with db_manager as db:
        question = QuestionModel(subject=_question_create.subject,
                                 content=_question_create.content,
                                 create_date=datetime.datetime.now())
        db.add(question)
        db.commit()