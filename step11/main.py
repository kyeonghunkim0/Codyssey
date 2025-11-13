# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def read_root():
    """
    기본 루트 엔드포인트.
    """
    return {'message': '한송희 박사의 화성 Q&A 게시판'}

# (참고) 나중에 이 파일에서 database.py와 models.py를 import하여
# API 엔드포인트를 구현하게 됩니다.