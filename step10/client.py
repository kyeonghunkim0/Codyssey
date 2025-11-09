import requests
import json

BASE_URL = 'http://127.0.0.1:8000'

# python3 client.py

def pretty_print(res_json):
    """JSON 응답을 예쁘게 출력"""
    print(json.dumps(res_json, indent=2, ensure_ascii=False))


try:
    # 1. GET (전체)
    print("--- 1. 전체 조회 ---")
    response = requests.get(f'{BASE_URL}/todos')
    response.raise_for_status()  # 오류가 있으면 예외 발생
    pretty_print(response.json())

    # 2. POST (추가)
    print("\n--- 2. '기지 청소' 추가 ---")
    new_todo = {'task': '기지 청소', 'priority': 'low'}
    response = requests.post(f'{BASE_URL}/todos', json=new_todo)
    response.raise_for_status()
    new_data = response.json()
    pretty_print(new_data)

    new_id = new_data['id']  # 방금 추가된 ID 저장

    # 3. GET (개별)
    print(f"\n--- 3. ID {new_id}번 조회 ---")
    response = requests.get(f'{BASE_URL}/todos/{new_id}')
    response.raise_for_status()
    pretty_print(response.json())

    # 4. PUT (수정)
    print(f"\n--- 4. ID {new_id}번 우선순위 수정 ---")
    update_data = {'priority': 'medium'}
    response = requests.put(f'{BASE_URL}/todos/{new_id}', json=update_data)
    response.raise_for_status()
    pretty_print(response.json())

    # 5. DELETE (삭제)
    print(f"\n--- 5. ID {new_id}번 삭제 ---")
    response = requests.delete(f'{BASE_URL}/todos/{new_id}')
    response.raise_for_status()
    pretty_print(response.json())

    # 6. GET (최종 확인)
    print("\n--- 6. 최종 전체 조회 ---")
    response = requests.get(f'{BASE_URL}/todos')
    response.raise_for_status()
    pretty_print(response.json())

except requests.exceptions.RequestException as e:
    print(f"\n[에러] 서버에 연결할 수 없거나 요청이 실패했습니다.")
    print(f"서버가 실행 중인지 확인하세요. (uvicorn todo:app --reload)")
    print(f"에러 상세: {e}")