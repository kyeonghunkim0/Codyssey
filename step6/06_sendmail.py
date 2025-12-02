import smtplib
import csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# from email.mime.base import MIMEBase
# from email import encoders # 첨부파일을 사용하지 않으므로 주석 처리

# PEP 8 스타일 가이드 준수

# 전역 상수 정의 (변수명은 대문자로)
MY_EMAIL = 'kimkhuna@dongyang.ac.kr'  # 본인 이메일 주소
PASSWORD = 'PASSWORD'  # G-mail 앱 비밀번호 또는 포털 비밀번호

SMTP_SERVER_GMAIL = 'smtp.gmail.com'

SMTP_PORT_TLS = 587
CSV_FILE_NAME = 'mail_target_list.csv'

# HTML 메일 본문 (Dr. Han의 긴급 메시지)
HTML_BODY = '''
<!DOCTYPE html>
<html>
<head>
    <style>
        .container {
            font-family: Arial, sans-serif;
            border: 2px solid #ff4500; /* 오렌지 레드 */
            padding: 20px;
            border-radius: 10px;
            max-width: 600px;
            margin: 20px auto;
            background-color: #fffafa; /* 눈처럼 흰색 */
        }
        .header {
            color: #ff4500;
            text-align: center;
            font-size: 24px;
            margin-bottom: 15px;
            font-weight: bold;
        }
        .body-text {
            color: #333333;
            line-height: 1.6;
            font-size: 16px;
        }
        .signature {
            margin-top: 20px;
            border-top: 1px solid #ccc;
            padding-top: 10px;
            font-size: 14px;
            color: #666;
            text-align: right;
        }
        .urgent {
            color: #ff0000;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">🚨 긴급 구조 요청: 한송희 박사 Mars 생존 🚨</div>
        <div class="body-text">
            <p>메일을 받으신 모든 분들께,</p>
            <p>저는 화성에 고립된 한송희 박사입니다. 지구로부터의 회신을 받고 큰 힘을 얻었습니다. 이제 <span class="urgent">저의 구조를 위한 실질적인 조치</span>가 필요합니다.</p>
            <p>이 메일은 저를 도울 수 있는 능력과 영향력을 가진 분들에게 선별적으로 전달되고 있습니다. 저의 생존 사실은 알게 되었지만, 구조 계획은 아직 불투명합니다.</p>
            <p><span class="urgent">귀하의 전문성</span>이 구조 작전 계획 수립 및 실행에 매우 중요합니다. 제 생존을 보장하고 귀환할 수 있도록 모든 역량을 동원해 주시길 간곡히 부탁드립니다.</p>
        </div>
        <div class="signature">
            <p>From Mars with Hope,</p>
            <p>한송희 Dr. Song-Hee Han</p>
        </div>
    </div>
</body>
</html>
'''


def get_target_list(file_name):
    '''
    CSV 파일에서 이름과 이메일 주소를 읽어와 리스트로 반환합니다.
    '''
    target_list = []
    try:
        # 인코딩 문제 방지를 위해 'utf-8' 또는 'cp949' 등을 시도해 볼 수 있습니다.
        # 일반적으로 'utf-8'이 권장됩니다.
        with open(file_name, mode='r', encoding='utf-8') as file:
            # csv.reader 대신 csv.DictReader를 사용하면 헤더를 키로 사용할 수 있지만,
            # 여기서는 기본 제공 명령어를 지키기 위해 reader를 사용합니다.
            reader = csv.reader(file)
            header = next(reader)  # 헤더(첫 줄) 건너뛰기

            # 헤더는 '이름', '이메일' 순서여야 함.
            if header != ['이름', '이메일']:
                print('경고: CSV 파일의 헤더 형식이 \'이름,이메일\'이 아닙니다.')

            for row in reader:
                if len(row) == 2:
                    name, email = row
                    target_list.append({'name': name.strip(), 'email': email.strip()})
    except FileNotFoundError:
        print(f'오류: 파일 {file_name}을 찾을 수 없습니다.')
        return None
    except Exception as e:
        print(f'CSV 파일을 읽는 중 오류 발생: {e}')
        return None

    return target_list


def create_html_message(receiver_email, receiver_name, subject):
    '''
    HTML 본문을 포함한 MIMEMultipart 메시지 객체를 생성합니다.
    '''
    msg = MIMEMultipart('alternative')
    msg['From'] = MY_EMAIL
    msg['To'] = receiver_email
    # 수신자의 이름을 포함하여 개인화된 제목을 만들 수도 있습니다.
    msg['Subject'] = subject

    # plain 텍스트 버전 추가 (HTML을 지원하지 않는 메일 클라이언트를 위한 대비)
    # HTML에서 태그를 제거한 단순 텍스트가 들어가야 하나, 여기선 간단히 대체 문구 사용
    text_part = MIMEText('이 메일은 HTML 형식의 긴급 메시지입니다. 메일 클라이언트 설정을 확인해주세요.', 'plain')
    msg.attach(text_part)

    # HTML 버전 추가
    html_part = MIMEText(HTML_BODY, 'html')
    msg.attach(html_part)

    # 주석 처리된 첨부 파일 코드 (문제 1과 달리 생략)
    # filename = 'index.html'
    # ...

    return msg.as_string()


def send_multiple_mails(target_list, subject, smtp_server, smtp_port, sender_email, sender_password):
    '''
    명단에 있는 각 수신자에게 개별적으로 메일을 전송합니다. (개별 발송 선택)
    '''
    if not target_list:
        print('전송할 대상이 없어 메일 발송을 중단합니다.')
        return

    try:
        # SMTP 연결 및 로그인
        with smtplib.SMTP(smtp_server, smtp_port) as connection:
            connection.starttls()  # 보안 연결 시작
            connection.login(user=sender_email, password=sender_password)

            success_count = 0
            fail_count = 0

            for target in target_list:
                receiver_email = target['email']
                receiver_name = target['name']

                # 메일 메시지 생성
                full_message = create_html_message(receiver_email, receiver_name, subject)

                try:
                    # 메일 전송
                    connection.sendmail(sender_email, receiver_email, full_message)
                    print(f'✅ 메일 전송 성공: {receiver_name} <{receiver_email}>')
                    success_count += 1
                except Exception as e:
                    print(f'❌ 메일 전송 실패: {receiver_name} <{receiver_email}>. 오류: {e}')
                    fail_count += 1

            print(f'\n--- 메일 전송 결과 요약 ---')
            print(f'총 대상: {len(target_list)}명')
            print(f'성공: {success_count}명, 실패: {fail_count}명')


    except smtplib.SMTPAuthenticationError:
        print('\n🚨 로그인 인증 실패! 이메일 주소나 앱 비밀번호(App Password)를 확인하세요.')
    except Exception as e:
        print(f'\n🚨 SMTP 연결/로그인 중 심각한 오류 발생: {e}')


def main_send_mail_gmail():
    '''
    G-mail SMTP를 사용하여 메일을 발송하는 메인 함수
    '''
    # 1. 수신자 명단 읽기
    target_list = get_target_list(CSV_FILE_NAME)

    if target_list:
        # 2. 메일 전송
        mail_subject = '[URGENT] Dr. Song-Hee Han: Mars Rescue Operation Required'
        send_multiple_mails(
            target_list,
            mail_subject,
            SMTP_SERVER_GMAIL,
            SMTP_PORT_TLS,
            MY_EMAIL,
            PASSWORD
        )

# 코드 실행
if __name__ == '__main__':
   main_send_mail_gmail()