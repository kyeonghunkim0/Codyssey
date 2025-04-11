import json
import time
import threading
from collections import defaultdict
from step3.mars_mission_computer import DummySensor

import platform
import psutil

internal_temperature = "mars_base_internal_temperature"      # 화성 기지 내부 온도
external_temperature = "mars_base_external_temperature"     # 화성 기지 외부 온도
internal_humidity = "mars_base_internal_humidity"           # 화성 기지 내부 습도
external_illuminance = "mars_base_external_illuminance"     # 화성 기지 외부 광량
internal_co2 = "mars_base_internal_co2"                     # 화성 기지 내부 이산화탄소 농도
internal_oxygen = "mars_base_internal_oxygen"               # 화성 기지 내부 산소 농도

ENV_KEYS = [
    internal_temperature,
    external_temperature,
    internal_humidity,
    external_illuminance,
    internal_co2,
    internal_oxygen
]

class MissionComputer:
    def __init__(self):
        self.ds = DummySensor()
        self.env_values = {key: None for key in ENV_KEYS}
        self.history = defaultdict(list)
        self.running = True  # 입력 스레드와 공유할 상태값

    def get_sensor_data(self):
        print("환경 모니터링 시작 (중단하려면 콘솔에 'q' 입력)...")
        start_time = time.time()

        while self.running:
            # env_value 설정
            self.ds.set_env()

            self.env_values[internal_temperature] = self.ds.env_values[internal_temperature]
            self.env_values[external_temperature] = self.ds.env_values[external_temperature]
            self.env_values[internal_humidity] = self.ds.env_values[internal_humidity]
            self.env_values[external_illuminance] = self.ds.env_values[external_illuminance]
            self.env_values[internal_co2] = self.ds.env_values[internal_co2]
            self.env_values[internal_oxygen] = self.ds.env_values[internal_oxygen]
            # JSON 형식으로 출력
            print(json.dumps(self.env_values, indent=4))

            for key in ENV_KEYS:
                self.history[key].append(self.env_values[key])
            # 5분에 한번씩 각 환경값에 대한 5분 평균 값을 별도로 출력한다.
            if time.time() - start_time >= 300:
                print("\n===== [5분 평균 환경 데이터] =====")
                avg_values = {
                    key: round(sum(self.history[key]) / len(self.history[key]), 2)
                    for key in ENV_KEYS if self.history[key]
                }
                print(json.dumps(avg_values, indent=4))
                print("==================================\n")

                start_time = time.time()
                self.history = defaultdict(list)

            time.sleep(5)

        print("System stopped...")

    def listen_for_quit(self):
        """콘솔에 'q' 입력 시 루프 종료"""
        while True:
            user_input = input()
            if user_input.strip().lower() == 'q':
                self.running = False
                break
    # 컴퓨터의 정보를 가져오는 메소드
    def get_mission_computer_info(self):
        info = {
            "OS" : platform.system(),   # 운영체계
            "OS_VERSION" : platform.version(),  # 운영체계 버전
            "CPU_TYPE" : platform.processor(),  # CPU의 타입
            "CPU_CORE_COUNT" : psutil.cpu_count(logical=False), # CPU의 코어 수
            "MEMORY" : round(psutil.virtual_memory().total / (1024 ** 3), 2)    # 메모리의 크기
        }
        return info
    # CPU/메모리 사용량을 가져오는 메소드
    def get_mission_computer_load(self):
        cpu_usage = psutil.cpu_percent(interval=1)  # 실시간 CPU 사용량 (1초 측정)
        memory_usage = psutil.virtual_memory().percent    # 메모리 사용량
        info = {
            "CPU_USAGE_PERCENT": f"{cpu_usage}%",
            "MEMORY_USAGE_PERCENT": f"{memory_usage}%"
        }
        return info
    #  setting.txt 파일 생성
    def write_settings(self, settings, file_path="setting.txt"):
        with open(file_path, "w") as f:
            if isinstance(settings, dict):
                for key, value in settings.items():
                    f.write(f"{key}: {value}\n")
            elif isinstance(settings, list):
                for item in settings:
                    f.write(f"{item}\n")
            elif isinstance(settings, str):
                f.write(f"{settings}\n")
            else:
                print("지원하지 않는 타입")
    # setting.txt 파일 읽기
    def read_settings_from_file(self, file_path="setting.txt"):
        try:
            with open(file_path, "r") as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"{file_path} 파일이 존재하지 않습니다.")
            return []

if __name__ == "__main__":
    runComputer = MissionComputer()
    print("#######################################################")    # 구분선
    # 컴퓨터 정보
    computer_info = runComputer.get_mission_computer_info()
    print("get_mission_computer_info()에 가져온 시스템 정보를 JSON 형식으로 출력")
    print(json.dumps(computer_info, indent=4))
    # CPU/메모리 사용량
    computer_load = runComputer.get_mission_computer_load()
    print("get_mission_computer_load()에 해당 결과를 JSON 형식으로 출력")
    print(json.dumps(computer_load, indent=4))
    # 파라미터로 출력되는 정보 설정
    runComputer.write_settings(computer_load["CPU_USAGE_PERCENT"])
    runComputer.read_settings_from_file()