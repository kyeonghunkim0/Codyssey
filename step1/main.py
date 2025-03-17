# Tool : PyCharm
# 설치가 잘 되었는지 확인 하기 위해서 ‘Hello Mars’를 출력해 본다.
print("Hello Mars")
#  log 파일을 열기
log_data = []
log = open('mission_computer_main.log', 'r', encoding='utf-8')
try:
    for line in log:
        print(line) # 로그 출력
        if line.strip().startswith("timestamp"):  # 헤더 줄 제외
            continue
        parts = line.strip().split(',')
        if len(parts) >= 3:  # 예상 데이터 구조 검증
            log_data.append({
                'timestamp': parts[0],
                'event': parts[1],
                'message': parts[2]
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
markdown_content = f"## 사고 원인 분석\n\n"
markdown_content += f"**사고 원인:** {cause if cause else '원인 미상'}\n\n" # 원인이 없다며
markdown_content += "## 로그 타임라인\n\n"

# 로그 타임라인 생성
for log in reversed(incident_logs):
    markdown_content += f"- **[{log['timestamp']}]** {log['event']} - {log['message']}\n"

# Markdown 파일로 저장
file = open('log_analysis.md', 'w', encoding='utf-8')
try:
    file.write(markdown_content)
    print('✅ Markdown 파일 생성 성공!')
finally:
    file.close()



