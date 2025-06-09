import pandas as pd
import pymysql

# 1. CSV 파일 읽기
csv_file = 'mars_weathers_data.csv'
df = pd.read_csv(csv_file)
print("CSV 데이터 미리보기:\n", df.head())

# 2. MySQL 연결 정보 입력
conn = pymysql.connect(
    host='127.0.0.1',
    user='root',    # 본인의 MySQL 유저명
    password='root',          # 본인의 MySQL 비밀번호
    db='sys',                # 데이터베이스 이름 (예시: sys, mars, test 등)
    charset='utf8'
)
cursor = conn.cursor()

# 3. 테이블이 이미 생성되어 있다고 가정 (없으면 위 쿼리 참고해서 생성)

# 4. 데이터 INSERT
insert_sql = """
INSERT INTO mars_weather (mars_date, temp, storm)
VALUES (%s, %s, %s)
"""

for idx, row in df.iterrows():
    cursor.execute(insert_sql, (row['mars_date'], int(row['temp']), int(row['storm'])))

conn.commit()
print(f"{cursor.rowcount}개 레코드가 삽입되었습니다.")

# 5. 연결 종료
cursor.close()
conn.close()
