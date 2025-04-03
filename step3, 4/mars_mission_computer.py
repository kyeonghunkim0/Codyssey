import random
import csv
import json
import time

internal_temperature = "mars_base_internal_temperature"      # 화성 기지 내부 온도
external_temperature = "mars_base_external_temperature"     # 화성 기지 외부 온도
internal_humidity = "mars_base_internal_humidity"           # 화성 기지 내부 습도
external_illuminance = "mars_base_external_illuminance"     # 화성 기지 외부 광량
internal_co2 = "mars_base_internal_co2"                     # 화성 기지 내부 이산화탄소 농도
internal_oxygen = "mars_base_internal_oxygen"               # 화성 기지 내부 산소 농도

# 더미 센서에 해당하는 클래스를 생성한다. 클래스의 이름은 DummySensor로 정의한다.
class DummySensor:
    # DummySensor의 멤버로 env_values라는 사전 객체를 추가한다. 사전 객체에는 다음과 같은 항목들이 추가 되어 있어야 한다
    def __init__(self):
       self.env_values = {
           internal_temperature : None,
           external_temperature : None,
           internal_humidity : None,
           external_illuminance : None,
           internal_co2 : None,
           internal_oxygen : None
       }
    # DummySensor 클래스에 set_env() 메소드를 추가한다.
    # set_env() 메소드는 random으로 주어진 범위 안의 값을 생성해서 env_values 항목에 채워주는 역할을 한다.
    def set_env(self):
        self.env_values[internal_temperature] = random.randint(18, 30)       # 18 ~ 30(도)
        self.env_values[external_temperature] = random.randint(0, 21)       # 0 ~ 21(도)
        self.env_values[internal_humidity] = random.randint(50, 60)         # 50 ~ 60(%)
        self.env_values[external_illuminance] = random.randint(500, 715)    # 500 ~ 715(W/m2)
        self.env_values[internal_co2] = random.uniform(0.02, 0.1)           # 0.02 ~ 0.1(%)
        self.env_values[internal_oxygen] = random.randint(4, 7)             # 4 ~ 7 (%)
    # DummySensor 클래스는 get_env() 메소드를 추가하는데 get_env() 메소드는 env_values를 return 한다.
    def get_env(self):
        return self.env_values

    def create_csv_file(self, data):
        with open('Mars_Base_Inventory_danger.csv', 'w', encoding='utf-8') as f:
            for row in data:
                f.write(row + '\n')
# # DummySensor 클래스를 ds라는 이름으로 인스턴스(Instance)로 만든다.
# ds = DummySensor()
# # 인스턴스화 한 DummySensor 클래스에서 set_env()와 get_env()를 차례로 호출해서 값을 확인한다.
# ds.set_env()
# env_data = ds.get_env()
# csv_data = []
# 값 출력
# for key, value in env_data.items():
#     if(key == interal_temperature or key == external_temperature): # 내부 온도, 외부 온도
#         print(f"{key} : {value}°C")
#         csv_data.append(f"{key} : {value}°C")
#     elif(key == internal_humidity): # 내부 습도
#         print(f"{key} : {value}%")
#         csv_data.append(f"{key} : {value}%")
#     elif(key == external_illuminance or key == internal_oxygen):  # 외부 광량, 내부 산소 농도
#         print(f"{key} : {value} W/m2")
#         csv_data.append(f"{key} : {value} W/m2")
#     elif(key == internal_co2): # 내부 이산화탄소 농도(소수점 둘째자리까지 반올림)
#         print(f"{key} : {value: .2f}%")
#         csv_data.append(f"{key} : {value: .2f}%")
#     else:
#         print("")
#         csv_data.append("")
# ds.create_csv_file(csv_data)


class MissionComputer:
    def __init__(self):
        # DummySensor 인스턴스 생성
        self.ds = DummySensor()

        # 환경 값을 저장할 딕셔너리 초기화
        self.env_values = {
            internal_temperature: None,
            external_temperature: None,
            internal_humidity: None,
            external_illuminance: None,
            internal_co2: None,
            internal_oxygen: None
        }

    def get_sensor_data(self):
        while True:
            # 센서의 값을 가져와서 env_values에 담는다.
            self.ds.set_env()
            # DummySensor에서 각 항목의 센서 값을 받아 env_values에 저장
            self.env_values[internal_temperature] = self.ds.env_values[internal_temperature]
            self.env_values[external_temperature] = self.ds.env_values[external_temperature]
            self.env_values[internal_humidity] = self.ds.env_values[internal_humidity]
            self.env_values[external_illuminance] = self.ds.env_values[external_illuminance]
            self.env_values[internal_co2] = self.ds.env_values[internal_co2]
            self.env_values[internal_oxygen] = self.ds.env_values[internal_oxygen]
            # env_values의 값을 출력한다. 이때 환경 정보의 값은 json 형태로 화면에 출력한다.
            print(json.dumps(self.env_values, indent=4))
            # 5초 대기
            time.sleep(5)
# MissionComputer 클래스 인스턴스 생성
RunComputer = MissionComputer()

# get_sensor_data 메소드 호출로 지속적인 환경 데이터 출력 시작
RunComputer.get_sensor_data()