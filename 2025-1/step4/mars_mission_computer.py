import json
import time
import threading
from collections import defaultdict
from step3.mars_mission_computer import DummySensor

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


if __name__ == "__main__":
    RunComputer = MissionComputer()

    # 특정 키를 입력할 경우 반복적으로 출력되던 화성 기지의 환경에 대한 출력을 멈추고 ‘Sytem stoped….’ 를 출력 할 수 있어야 한다.
    listener_thread = threading.Thread(target=RunComputer.listen_for_quit)
    listener_thread.daemon = True
    listener_thread.start()

    # 센서 루프 실행
    RunComputer.get_sensor_data()