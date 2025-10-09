# 라이브러리 불러오기

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# 개인 정보 입력(email, 앱 비밀번호)
my_email = "kimkhuna@dongyang.ac.kr"
password = "PASSWORD"


# 메일 구성
msg = MIMEMultipart()
msg["From"] = my_email
msg["To"] = "kimkhuna@naver.com"
msg["Subject"] = "제목제목제목"

# 본문 추가
body = "내용내용내용"
msg.attach(MIMEText(body, "plain"))

# 첨부 파일 추가
filename = "index.html"  # 첨부할 파일명
with open(filename, "rb") as attachment:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

encoders.encode_base64(part)
part.add_header("Content-Disposition", f"attachment; filename={filename}")
msg.attach(part)

# SMTP 설정 및 전송
connection = smtplib.SMTP("smtp.gmail.com", 587)
connection.starttls()
connection.login(user=my_email, password=password)
connection.sendmail(my_email, "kimkhuna@naver.com", msg.as_string())
connection.close()
