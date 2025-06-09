import pandas as pd
import pymysql

# 1. CSV 파일 읽기
csv_file = 'mars_weathers_data.csv'
df = pd.read_csv(csv_file)
print("CSV 데이터 미리보기:\n", df.head())

class MySQLHelper:
    """MySQL 데이터베이스 연결 및 쿼리 실행을 도와주는 클래스"""

    def __init__(self, host, user, password, db, charset='utf8'):
        """초기화: 연결 정보 설정 및 DB 연결"""
        self.conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=db,
            charset=charset
        )
        self.cursor = self.conn.cursor()

    def execute(self, query, params=None):
        """INSERT, UPDATE, DELETE 등 쿼리 실행"""
        self.cursor.execute(query, params or ())
        self.conn.commit()

    def fetchall(self, query, params=None):
        """SELECT 쿼리 실행 후 모든 결과 반환"""
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall()

    def fetchone(self, query, params=None):
        """SELECT 쿼리 실행 후 한 개 결과 반환"""
        self.cursor.execute(query, params or ())
        return self.cursor.fetchone()

    def close(self):
        """DB 연결 종료"""
        self.cursor.close()
        self.conn.close()


# 사용 예시
if __name__ == '__main__':
    # 연결 정보 입력
    db_helper = MySQLHelper(
        host='127.0.0.1',
        user='root',  # 본인의 MySQL 유저명
        password='root',  # 본인의 MySQL 비밀번호
        db='sys',  # 데이터베이스 이름 (예시: sys, mars, test 등)
        charset='utf8'
    )

    # SELECT
    results = db_helper.fetchall("SELECT * FROM mars_weather;")
    for row in results:
        print(row)

    # INSERT
    # insert_sql = """
    #     INSERT INTO mars_weather (mars_date, temp, storm)
    #     VALUES (%s, %s, %s)
    # """
    #
    # for _, row in df.iterrows():
    #     db_helper.execute(insert_sql, (row['mars_date'], int(row['temp']), int(row['storm'])))

    # DELETE
    # db_helper.execute("TRUNCATE TABLE mars_weather;")

    db_helper.close()

