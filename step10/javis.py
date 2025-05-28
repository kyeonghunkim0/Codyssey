#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
javis.py

시스템 마이크 인식 후 음성을 녹음하고, records 폴더에
‘YYYYMMDD-HHMMSS.wav’ 형식으로 저장합니다.
또한, 특정 날짜 범위의 녹음 파일을 조회하는 기능을 제공합니다.
'''

import os
import datetime
import argparse
import wave

import pyaudio


# 녹음 파일이 저장될 디렉터리 이름
RECORDS_DIR = './step10/records'

# 실행 : ./step10/javis.py record
# 조회 : ./step10/javis.py list 20250501 20250528

class AudioRecorder:

    def __init__(self,
                 channels=1,
                 rate=44100,
                 chunk_size=1024,
                 audio_format=pyaudio.paInt16):
        self.channels = channels
        self.rate = rate
        self.chunk_size = chunk_size
        self.audio_format = audio_format
        self.pyaudio_instance = pyaudio.PyAudio()
        self.stream = None
    # 현재시간(YYYYMMDD-HHMMSS) 파일 이름 생성
    def _get_filename(self):
        now = datetime.datetime.now()
        return now.strftime('%Y%m%d-%H%M%S') + '.wav'
    # records 디렉터리가 없으면 생성
    def _ensure_records_dir(self):
        if not os.path.isdir(RECORDS_DIR):
            os.makedirs(RECORDS_DIR)
    # 녹음 시작 후 [Ctrl + C] 입력 시 녹음 종료 후에 파일 저장
    def start_recording(self):
        self._ensure_records_dir()
        filename = self._get_filename()
        filepath = os.path.join(RECORDS_DIR, filename)

        # 스트림 오픈
        self.stream = self.pyaudio_instance.open(
            format=self.audio_format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )

        frames = []
        print('녹음을 시작합니다. 중지하려면 Ctrl+C를 누르세요.')

        try:
            while True:
                data = self.stream.read(self.chunk_size)
                frames.append(data)
        except KeyboardInterrupt:
            print('\n녹음을 중지합니다.')
        finally:
            # 스트림 정리
            self.stream.stop_stream()
            self.stream.close()
            self.pyaudio_instance.terminate()
            # WAV 파일로 저장
            with wave.open(filepath, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(
                    self.pyaudio_instance.get_sample_size(self.audio_format)
                )
                wf.setframerate(self.rate)
                wf.writeframes(b''.join(frames))

            print(f'파일이 저장되었습니다: {filepath}')

def show_recordings(start_date, end_date):
    '''
    지정한 날짜 범위의 녹음 파일 목록을 출력합니다.

    Args:
        start_date (str): 시작 날짜 'YYYYMMDD'
        end_date (str): 종료 날짜 'YYYYMMDD'
    '''
    if not os.path.isdir(RECORDS_DIR):
        print('녹음 폴더가 존재하지 않습니다.')
        return

    try:
        start = datetime.datetime.strptime(start_date, '%Y%m%d').date()
        end = datetime.datetime.strptime(end_date, '%Y%m%d').date()
    except ValueError:
        print('날짜 형식이 올바르지 않습니다. YYYYMMDD로 입력하세요.')
        return

    files = os.listdir(RECORDS_DIR)
    matched = []

    for filename in files:
        if not filename.lower().endswith('.wav'):
            continue

        basename = os.path.splitext(filename)[0]
        try:
            file_dt = datetime.datetime.strptime(
                basename, '%Y%m%d-%H%M%S'
            ).date()
        except ValueError:
            continue

        if start <= file_dt <= end:
            matched.append(filename)

    if matched:
        print('범위 내 녹음 파일:')
        for fname in sorted(matched):
            print(f'  - {fname}')
    else:
        print('해당 범위에 녹음 파일이 없습니다.')


def main():
    '''명령행 인터페이스: 녹음(record) 또는 목록 조회(list)'''
    parser = argparse.ArgumentParser(
        description='마이크 녹음 및 녹음 파일 목록 조회 도구'
    )
    subparsers = parser.add_subparsers(dest='command')

    # record 서브커맨드
    subparsers.add_parser('record', help='새 녹음을 시작합니다')

    # list 서브커맨드
    list_parser = subparsers.add_parser(
        'list', help='녹음 파일 목록을 조회합니다'
    )
    list_parser.add_argument(
        'start_date', help="시작 날짜 (YYYYMMDD)"
    )
    list_parser.add_argument(
        'end_date', help="종료 날짜 (YYYYMMDD)"
    )

    args = parser.parse_args()

    if args.command == 'record':
        recorder = AudioRecorder()
        recorder.start_recording()
    elif args.command == 'list':
        show_recordings(args.start_date, args.end_date)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
