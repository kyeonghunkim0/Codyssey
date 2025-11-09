# todo.py

# python3 -m venv venv
# source .venv/bin/activate
# pip install "fastapi[all]"

# curl -X GET "http://127.0.0.1:8000/todos"

# curl -X POST 'http://127.0.0.1:8000/todos' \
# -H 'Content-Type: application/json' \
# -d '{"task": "이건 급한 일이야", "priority": "high"}'

# curl -X POST 'http://127.0.0.1:8000/todos' \
# -H 'Content-Type: application/json' \
# -d '{"task" : "", "priority" : ""}'


from fastapi import FastAPI, APIRouter, HTTPException, status
from typing import Dict, List, Any

#  리스트 객체를 todo_list라는 이름으로 추가
todo_list: List[Dict[str, Any]] = []

# APIRouter 클래스를 이용해서 라우트 추가
router = APIRouter()


@router.post('/todos')
def add_todo(todo: Dict[str, Any]):
    """
    새로운 할 일(todo)을 todo_list에 추가합니다.
    입력값은 Dict 타입입니다.
    """

    # (보너스 과제) 입력되는 Dict 타입이 빈값이면 400 에러.
    is_empty = (not todo)
    if is_empty:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Input dictionary cannot be empty'
        )

    todo_list.append(todo)

    # 입출력은 Dict 타입
    return {'message': 'Todo added successfully'}


# (수행과제 8) retrieve_todo()
# GET 방식, todo_list를 가져옴
@router.get('/todos')
def retrieve_todo():
    """
    전체 todo_list를 반환합니다.
    """
    return todo_list


# FastAPI 앱 생성 및 라우터 포함
app = FastAPI()
app.include_router(router)