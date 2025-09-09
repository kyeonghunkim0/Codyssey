#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
javis.py

시스템 마이크 인식 후 음성을 녹음하고, records 폴더에
‘YYYYMMDD-HHMMSS.wav’ 형식으로 저장합니다.

또한, 특정 날짜 범위의 녹음 파일을 조회하는 기능을 제공합니다.
마이크 녹음, 녹음 파일 목록, 녹음파일 STT 변환(csv), 키워드 검색까지 지원

'''

import os
import datetime
import argparse
import wave
import csv

import pyaudio
import speech_recognition as sr

# 실행 : ./step10/javis.py record
# 조회 : ./step10/javis.py list 20250501 20250528
# 조합 : ./step10/javis.py stt 20250608-222902.wav

# 녹음 파일이 저장될 디렉터리 이름
RECORDS_DIR = './step10/records'

class AudioRecorder:
    '''시스템 마이크에서 오디오를 녹음하는 클래스'''

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

    def _get_filename(self):
        '''현재 시각을 기반으로 파일 이름 생성'''
        now = datetime.datetime.now()
        return now.strftime('%Y%m%d-%H%M%S') + '.wav'

    def _ensure_records_dir(self):
        '''records 디렉터리가 없으면 생성'''
        if not os.path.isdir(RECORDS_DIR):
            os.makedirs(RECORDS_DIR)

    def start_recording(self):
        '''녹음을 시작'''
        self._ensure_records_dir()
        filename = self._get_filename()
        filepath = os.path.join(RECORDS_DIR, filename)

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
            self.stream.stop_stream()
            self.stream.close()
            self.pyaudio_instance.terminate()

            with wave.open(filepath, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(
                    self.pyaudio_instance.get_sample_size(self.audio_format)
                )
                wf.setframerate(self.rate)
                wf.writeframes(b''.join(frames))

            print(f'파일이 저장되었습니다: {filepath}')


def show_recordings(start_date, end_date):
    '''특정 날짜 범위 내의 녹음파일 조회'''
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


def stt_audiofile(wav_filename):
    '''
    지정한 wav 파일을 STT 변환 후 CSV로 저장
    '''
    filepath = os.path.join(RECORDS_DIR, wav_filename)
    if not os.path.isfile(filepath):
        print(f'파일을 찾을 수 없습니다: {filepath}')
        return

    recognizer = sr.Recognizer()
    with sr.AudioFile(filepath) as source:
        audio = recognizer.record(source)

    print('STT 변환 중... (Google Web Speech API 사용)')

    try:
        # Google Web Speech API 무료 버전 사용 (인터넷 필요)
        text = recognizer.recognize_google(audio, language='ko-KR')
        # 한 문장 전체로 인식됨
        segments = [(0, text)]
    except sr.UnknownValueError:
        print('음성을 인식할 수 없습니다.')
        segments = []
    except sr.RequestError as e:
        print(f'STT 서비스 요청 실패: {e}')
        return

    # csv 파일로 저장
    csv_filename = os.path.splitext(wav_filename)[0] + '.csv'
    csv_path = os.path.join(RECORDS_DIR, csv_filename)
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for segment in segments:
            time_str = f'시간 : {segment[0]}초'
            text_str = f'인식된 텍스트 : {segment[1]}'
            writer.writerow([time_str, text_str])

    print(f'CSV 파일로 저장됨: {csv_path}')


def search_keyword_in_csv(keyword):
    '''
    records 폴더 내 모든 CSV 파일에서 키워드가 포함된 행을 찾아 출력
    '''
    if not os.path.isdir(RECORDS_DIR):
        print('녹음 폴더가 존재하지 않습니다.')
        return

    found = False
    for filename in os.listdir(RECORDS_DIR):
        if not filename.lower().endswith('.csv'):
            continue
        csv_path = os.path.join(RECORDS_DIR, filename)
        with open(csv_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                # row는 ["시간 : 0초", "인식된 텍스트 : 안녕하세요"] 형태
                if len(row) < 2:
                    continue
                time_part = row[0]
                text_part = row[1]
                # "인식된 텍스트 : " 이후의 실제 텍스트만 추출
                if keyword in text_part:
                    print(f'[{filename}] {time_part}, {text_part}')
                    found = True
    if not found:
        print('키워드가 포함된 텍스트를 찾을 수 없습니다.')


def main():
    parser = argparse.ArgumentParser(
        description='마이크 녹음, STT, 목록 조회, 키워드 검색 도구'
    )
    subparsers = parser.add_subparsers(dest='command')

    # 녹음
    subparsers.add_parser('record', help='새 녹음을 시작합니다')

    # 녹음 목록
    list_parser = subparsers.add_parser(
        'list', help='녹음 파일 목록을 조회합니다'
    )
    list_parser.add_argument('start_date', help="시작 날짜 (YYYYMMDD)")
    list_parser.add_argument('end_date', help="종료 날짜 (YYYYMMDD)")

    # STT
    stt_parser = subparsers.add_parser(
        'stt', help='녹음 wav 파일을 STT하여 csv로 저장'
    )
    stt_parser.add_argument('wav_filename', help="녹음된 wav 파일명 (예: 20240607-213215.wav)")

    # 키워드 검색
    search_parser = subparsers.add_parser(
        'search', help='CSV 파일 내 키워드 검색'
    )
    search_parser.add_argument('keyword', help="검색할 키워드")

    args = parser.parse_args()

    if args.command == 'record':
        recorder = AudioRecorder()
        recorder.start_recording()
    elif args.command == 'list':
        show_recordings(args.start_date, args.end_date)
    elif args.command == 'stt':
        stt_audiofile(args.wav_filename)
    elif args.command == 'search':
        search_keyword_in_csv(args.keyword)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
