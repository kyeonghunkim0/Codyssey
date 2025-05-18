# door_hacking.py

import zipfile        # ZIP 파일 열기/추출
import string         # 문자열 상수 (ascii_lowercase, digits)
import itertools      # 조합 생성 (product)
import time           # 시간 측정
from datetime import datetime  # 현재 시각 포맷팅

def unlock_zip():
    zip_filename    = 'emergency_storage_key.zip'
    charset         = string.ascii_lowercase + string.digits  # 'a'–'z' + '0'–'9'
    password_length = 6                                      # 비밀번호 자리 수

    # 시작 로그 출력
    start_time = time.time()
    print(f"[START] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    total_attempts = 0  # 시도 횟수

    # ZIP 파일 열기 (컨텍스트 매니저 사용)
    with zipfile.ZipFile(zip_filename) as zf:
        # 압축 내부의 첫 번째 파일 이름을 꺼내서 암호 검증에 사용
        file_to_test = zf.namelist()[0]

        # 모든 조합(36^6)의 순회를 itertools.product로 처리
        for pwd_tuple in itertools.product(charset, repeat=password_length):
            password = ''.join(pwd_tuple)  # 튜플을 문자열로 결합
            total_attempts += 1

            try:
                # 1) 암호 검증: 첫 번째 파일을 일부만 읽어보며 올바른지 확인
                with zf.open(file_to_test, pwd=password.encode()) as f:
                    f.read(1)  # 1바이트만 읽어도 CRC 체크 수행됨

                # 2) 검증 통과 시 전체 파일 추출
                zf.extractall(pwd=password.encode())

                # 성공 메시지 출력
                elapsed_time = time.time() - start_time
                print(f"\n[SUCCESS] Password found: {password}")
                print(f"Total attempts: {total_attempts}")
                print(f"Elapsed time: {elapsed_time:.2f} seconds")

                # 3) 찾은 비밀번호를 텍스트 파일에 기록
                with open("password.txt", "w") as out_f:
                    out_f.write(password)

                return  # 함수 종료

            except Exception:
                # 암호가 틀린 경우: 주기적으로 진행 상황 출력
                if total_attempts % 10000 == 0:
                    elapsed = time.time() - start_time
                    print(f"Attempt: {total_attempts}, Current: {password}, Elapsed: {elapsed:.2f}s")
                continue  # 다음 비밀번호 시도

    # 모든 조합 시도 후에도 못 찾았을 때
    print("[FAILED] Password not found.")

if __name__ == "__main__":
    unlock_zip()
