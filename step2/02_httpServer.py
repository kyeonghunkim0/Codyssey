# server.py

import http.server
import socketserver
import datetime

# 서버가 사용할 포트 번호를 정의합니다.
PORT = 8080


class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    HTTP 요청을 처리하는 커스텀 핸들러 클래스.

    http.server.SimpleHTTPRequestHandler를 상속받아 정적 파일(HTML, 이미지 등)을
    서빙하는 기본 기능을 활용합니다. 여기에 추가적으로 사용자 접속 정보를
    로그로 출력하는 기능을 구현합니다.
    """

    def do_GET(self):
        """
        GET 요청을 처리하는 메소드.

        클라이언트가 서버에 GET 방식으로 페이지나 파일을 요청할 때마다 호출됩니다.
        이 메소드 내에서 클라이언트 접속 시간과 IP 주소를 확인하고 출력합니다.

        참고: do_GET()은 HTTP GET 요청에 대한 응답을 처리하기 위해 http.server 모듈에서
              미리 정의된 약속된 메소드 이름입니다.
        """

        # 현재 접속 시간 정보를 'YYYY-MM-DD HH:MM:SS' 형식으로 포맷팅합니다.
        access_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 접속한 클라이언트의 IP 주소를 가져옵니다.
        # self.client_address는 (IP, Port) 형태의 튜플입니다.
        client_address = self.client_address[0]

        # 접속 시간과 IP 주소를 터미널에 출력하여 로그를 남깁니다.
        print(f'[{access_time}] Client connected from: {client_address}')

        # 부모 클래스(SimpleHTTPRequestHandler)의 do_GET() 메소드를 호출하여
        # 실제 파일 서빙 작업을 수행합니다.
        # 이 부분이 없으면 웹 페이지가 클라이언트에 전송되지 않습니다.
        super().do_GET()


def run_server():
    """
    지정된 포트로 HTTP 서버를 실행하는 함수.

    TCPServer를 생성하고 MyHTTPRequestHandler를 요청 처리기로 지정하여
    클라이언트의 요청을 대기하고 처리합니다.
    """

    # with 문을 사용하여 서버 소켓을 열고, 블록이 끝나면 자동으로 닫히도록 합니다.
    # 첫 번째 인자는 서버의 IP 주소로, ''는 모든 네트워크 인터페이스를 의미합니다.
    # 두 번째 인자는 서버 핸들러 클래스입니다.
    with socketserver.TCPServer(('', PORT), MyHTTPRequestHandler) as httpd:
        # 서버가 성공적으로 시작되었음을 알리는 메시지를 출력합니다.
        print(f'Serving at port {PORT}')

        # 서버가 종료될 때까지 지속적으로 클라이언트의 요청을 처리하도록 합니다.
        httpd.serve_forever()


if __name__ == '__main__':
    # 이 스크립트가 직접 실행될 때만 run_server() 함수를 호출하도록 합니다.
    # 다른 스크립트에서 이 파일을 모듈로 import할 때는 실행되지 않습니다.
    run_server()