# todo.py
from fastapi import FastAPI, APIRouter, HTTPException, status
from typing import Dict, List, Any
import csv
import os

# model.py에서 TodoItem 모델 가져오기
from model import TodoItem

# --- CSV 파일 설정 ---
CSV_FILE = 'todos.csv'
# (제약사항 C3) CSV 파일의 헤더(필드 이름)
FIELDNAMES = ['id', 'task', 'priority']

# uvicorn todo_10:app --reload

# 첫 번째 할 일 추가 (급한 일)
# curl -X POST 'http://127.0.0.1:8000/todos' \
# -H 'Content-Type: application/json' \
# -d '{"task": "화성 토양 샘플 분석", "priority": "high"}'

# 두 번째 할 일 추가 (보통 일)
# curl -X POST 'http://127.0.0.1:8000/todos' \
# -H 'Content-Type: application/json' \
# -d '{"task": "탐사 로버 배터리 점검", "priority": "medium"}'

# 전체 조회
# curl -X GET "http://127.0.0.1:8000/todos"

# 개별 조회
# curl -X GET "http://127.0.0.1:8000/todos/1"

# 수정
# curl -X PUT 'http://127.0.0.1:8000/todos/1' \
# -H 'Content-Type: application/json' \
# -d '{"task": "화성 토양 샘플 분석 (완료)"}'

# 삭제
# curl -X DELETE "http://127.0.0.1:8000/todos/2"

# 최종 조회
# curl -X GET "http://127.0.0.1:8000/todos"

# --- CSV 헬퍼 함수 ---

def init_csv():
    """CSV 파일이 없으면 헤더와 함께 새로 생성합니다."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()


def load_todos() -> List[Dict[str, Any]]:
    """todos.csv 파일에서 모든 할 일을 읽어옵니다."""
    init_csv()  # 파일이 없으면 생성
    todos = []
    with open(CSV_FILE, mode='r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # id는 정수(int) 타입으로 변환
            row['id'] = int(row['id'])
            todos.append(row)
    return todos


def save_todos(todos: List[Dict[str, Any]]):
    """모든 할 일 목록을 todos.csv 파일에 덮어씁니다."""
    with open(CSV_FILE, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(todos)


def get_next_id(todos: List[Dict[str, Any]]) -> int:
    """새로운 todo 항목에 사용할 id를 반환합니다."""
    if not todos:
        return 1
    # 현재 ID 중 가장 큰 값 + 1
    max_id = max(todo['id'] for todo in todos)
    return max_id + 1


# --- API 라우터 설정 ---

router = APIRouter()


# (수행과제 7, C8) - CSV 사용하도록 수정
@router.post('/todos')
def add_todo(todo: Dict[str, Any]):
    """
    새로운 할 일(todo)을 CSV 파일에 추가합니다.
    """
    is_empty = (not todo)
    if is_empty:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Input dictionary cannot be empty'
        )

    todos = load_todos()

    new_todo = {
        'id': get_next_id(todos),
        'task': todo.get('task'),  # Dict에서 'task' 키 값을 가져옴
        'priority': todo.get('priority')  # Dict에서 'priority' 키 값을 가져옴
    }

    todos.append(new_todo)
    save_todos(todos)

    return {'message': 'Todo added successfully', 'id': new_todo['id']}


# (수행과제 8) - CSV 사용하도록 수정
@router.get('/todos')
def retrieve_todo():
    """
    CSV 파일에서 전체 todo_list를 반환합니다.
    """
    return load_todos()


# (수행과제 1) get_single_todo ()
# (수행과제 2) 경로 매개변수로 아이디(todo_id)
# (수행과제 3) GET 방식
@router.get('/todos/{todo_id}')
def get_single_todo(todo_id: int):
    """
    지정된 id의 todo 항목을 반환합니다.
    """
    todos = load_todos()
    for todo in todos:
        if todo['id'] == todo_id:
            return todo

    # 항목을 찾지 못한 경우 404 에러
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Todo not found'
    )


# (수행과제 4) update_todo ()
# (수행과제 5) 경로 매개변수로 아이디(todo_id)
# (수행과제 6) PUT 방식
# (수행과제 7) TodoItem 모델 사용
@router.put('/todos/{todo_id}')
def update_todo(todo_id: int, todo_update: TodoItem):
    """
    지정된 id의 todo 항목을 수정합니다. (부분 수정 지원)
    """
    todos = load_todos()

    todo_to_update = None
    index = -1

    # 수정할 항목 찾기
    for i, todo in enumerate(todos):
        if todo['id'] == todo_id:
            todo_to_update = todo
            index = i
            break

    if todo_to_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Todo not found'
        )

    # (수행과제 7) 모델의 입력값을 Dict로 변환 (입력된 필드만)
    # exclude_unset=True: 사용자가 입력하지 않은 (None) 필드는 제외
    update_data = todo_update.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No fields to update'
        )

    # 기존 딕셔너리 업데이트
    updated_todo = todo_to_update.copy()
    updated_todo.update(update_data)

    # 리스트에서 항목 교체
    todos[index] = updated_todo
    save_todos(todos)

    return updated_todo


# (수행과제 9) delete_single_todo ()
# (수행과제 10) 경로 매개변수로 아이디(todo_id)
# (수행과제 11) DELETE 방식
@router.delete('/todos/{todo_id}')
def delete_single_todo(todo_id: int):
    """
    지정된 id의 todo 항목을 삭제합니다.
    """
    todos = load_todos()

    todo_to_delete = None
    for todo in todos:
        if todo['id'] == todo_id:
            todo_to_delete = todo
            break

    if todo_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Todo not found'
        )

    # 리스트에서 항목 제거
    todos.remove(todo_to_delete)
    save_todos(todos)

    return {'message': 'Todo deleted successfully'}


# FastAPI 앱 생성 및 라우터 포함
app = FastAPI()
app.include_router(router)

# (제약사항 C3) 서버 시작 시 CSV 파일 초기화
if __name__ == '__main__':
    init_csv()
    # uvicorn으로 실행 시 이 부분은 직접 실행되지 않지만,
    # python todo.py로 직접 실행할 경우를 대비
else:
    # uvicorn이 모듈로 로드할 때 이 부분이 실행됨
    init_csv()