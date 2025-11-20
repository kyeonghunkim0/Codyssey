# main.py
from fastapi import FastAPI
from domain.question.question_router import router as question_router

app = FastAPI()

@app.get('/')
def read_root():
    """
    기본 루트 엔드포인트.
    """
    return {'message': '한송희 박사의 화성 Q&A 게시판'}

app.include_router(question_router)

# uvicorn main:app --reload