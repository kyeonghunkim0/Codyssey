# 설치가 잘 되었는지 확인 하기 위해서 ‘Hello Mars’를 출력해 본다.
print("Hello Mars")
#  log 파일을 열기
log_data = []
log = open('mission_computer_main.log', 'r', encoding='utf-8')
try:
    next(log)
    for line in log:
        parts = line.strip().split(',')
        log_data.append({
            'timestamp' : parts[0],
            'event' : parts[1],
            'message' : parts[2]
        })
finally:
    log.close()

# 산소 탱크 관련 이벤트 필터링
    incident_logs = [entry for entry in log_data if 'Oxygen tank' in entry['message']]

# 사고 원인 분석
cause = ""
if any("unstable" in entry['message'] for entry in incident_logs):
    cause = "Oxygen tank unstable"
if any("explosion" in entry['message'] for entry in incident_logs):
    cause = "Oxygen tank explosion"

# Markdown 작성
    markdown_content = f"사고 원인: {cause}\n\n"

# 로그 타임라인 생성(
    for log in reversed(log_data):
        markdown_content += f"[{log['timestamp']}] - {log['event']}: {log['message']}\n"

# Markdown 파일로 저장
    file = open('log_analysis.md', 'w', encoding='utf-8')
    try:
        file.write(markdown_content)
    finally:
        file.close()

    print('Save markdown file success!')
