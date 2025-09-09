import csv
import struct

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

# 인화성 지수가 0.7 이상되는 목록을 뽑아서 별도로 출력
dangerous_data = filter_data_by_dangerous(sort_data)
print('====== dangerous_data ======')
print(dangerous_data)

def create_csv_file(filePath, header, data):
    data = filter_data_by_dangerous(sort_data)
    with open(filePath, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)  # 헤더 추가
        writer.writerows(data)   # 데이터 추가

# 인화성 지수가 0.7 이상되는 목록을 CSV 포멧(Mars_Base_Inventory_danger.csv)으로 저장
create_csv_file('filtered_data.csv', header, dangerous_data)

# 인화성 순서로 정렬된 데이터를 이진파일형태로 저장
def save_as_binary_file(filename, data):
    with open(filename, 'wb') as bin_file:
        for row in data:
            encoded_row = ','.join(row).strip()
            encoded_data = encoded_row.encode('utf-8')
            bin_file.write(struct.pack('I', len(encoded_data)))  # 데이터 길이 저장
            bin_file.write(encoded_data)  # 데이터 저장
# 함수 실행
save_as_binary_file('Mars_Base_Inventory_List.bin', sort_data)

# 저장된 Mars_Base_Inventory_List.bin 의 내용을 다시 읽어 들여서 화면에 내용을 출력
def load_from_binary_file(filename):
    data = []
    with open(filename, 'rb') as bin_file:
        while True:
            # 데이터 길이 읽기
            length_bytes = bin_file.read(4)
            if not length_bytes:  # EOF 체크
                break
            length = struct.unpack('I', length_bytes)[0] # 데이터 길이

            # 해당 길이만큼 데이터 읽기
            encoded_data = bin_file.read(length)
            decoded_row = encoded_data.decode('utf-8').split(',')
            data.append(decoded_row)
    print(data)

# 함수 실행
print('====== load_from_binary_file ======')
load_from_binary_file('Mars_Base_Inventory_List.bin')
