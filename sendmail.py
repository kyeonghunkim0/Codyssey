# 라이브러리 불러오기
import smtplib

# 개인 정보 입력(email, 앱 비밀번호)
my_email = "kimkhuna@dongyang.ac.kr"
password = "PASSWORD"

# 방법 1(with 사용 X)
connection = smtplib.SMTP("smtp.gmail.com") #보내는 메일의 SMTP 주소입력
connection.starttls() # Transport Layer Security : 메시지 암호화 기능
connection.login(user=my_email, password=password)
connection.sendmail(
	from_addr=my_email,
    to_addrs="kimkhuna@naver.com",
    msg="Subject:Hello\n\nThis is the body of my email."
)
connection.close()