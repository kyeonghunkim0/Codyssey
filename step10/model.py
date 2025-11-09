# model.py
from pydantic import BaseModel
from typing import Optional

# TodoItem 모델 추가
class TodoItem(BaseModel):
    """
    Todo 항목 수정을 위한 Pydantic 모델.
    모든 필드는 선택적(Optional)입니다.
    """
    task: Optional[str] = None
    priority: Optional[str] = None