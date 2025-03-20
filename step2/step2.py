import csv

# csv 파일을 읽는 함수
def read_csv_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file) # csv 파일 읽기
        # for row in reader:
            # print(row)         # Mars_Base_Inventory_List.csv 의 내용을 읽어 들어서 출력
        header = next(reader)  # 첫 번째 행의 헤더로 저장
        data = list(reader)    # 리스트(List) 객체로 변환
    return header, data

# 배열 내용을 적제 화물 목록을 인화성이 높은 순으로 정렬
def sort_data_by_flammability(data):
    # 인화성 지수는 마지막에 위치
    return sorted(data, key=lambda x: float(x[-1]), reverse=True)

# 인화성 지수가 0.7 이상되는 목록을 뽑아서 별도로 출력
def filter_data_by_dangerous(data):
    return [row for row in data if float(row[-1]) >= 0.7]


header, csv_data = read_csv_file('Mars_Base_Inventory_List.csv')
# 배열 내용을 적제 화물 목록을 인화성이 높은 순으로 정렬
sort_data = sort_data_by_flammability(csv_data)

# 인화성 지수가 0.7 이상되는 목록을 뽑아서 별도로 출력한다.
dangerous_data = filter_data_by_dangerous(sort_data)
print(dangerous_data)

def create_csv_file(filePath, header, data):
    data = filter_data_by_dangerous(sort_data)
    with open(filePath, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)  # 헤더 추가
        writer.writerows(data)   # 데이터 추가

# 인화성 지수가 0.7 이상되는 목록을 CSV 포멧(Mars_Base_Inventory_danger.csv)으로 저장한다.
create_csv_file('filtered_data.csv', header, dangerous_data)

