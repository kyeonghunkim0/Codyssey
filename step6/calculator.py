import sys
# Python으로 UI를 만들 수 있는 PyQT 라이브러리를 설치한다.
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QVBoxLayout, QLineEdit
from PyQt5.QtCore import Qt

class Calculator(QWidget):  # QWidget 상속 받아 하나의 창으로 구성
    def __init__(self):
        super().__init__()
        self.setFixedSize(320, 420)     # 320x420 으로 창 크기 고정
        self.initUI()                   # UI 구성
        self.current_expression = ""    # 현재 입력된 수식 문자열을 저장하는 변수
    # UI 구성
    def initUI(self):
        # 계산기 상단의 계산 결과 출력 창
        self.display = QLineEdit()
        self.display.setReadOnly(True)                                  # 사용자 입력 제한
        self.display.setAlignment(Qt.AlignRight)                        # 텍스트 오른쪽 정렬
        self.display.setStyleSheet("font-size: 30px; padding: 10px;")   # 스타일 설정
        self.display.setText("0")                                       # 처음은 0으로 설정
        # 버튼 배열
        buttons = [
            ['AC', '%', '+/-', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]
        # 버튼 배치하는 GridLayout
        grid = QGridLayout()

        # for 문으로 버튼을 만들고 Layout에 추가
        for row, row_values in enumerate(buttons):
            col_offset = 0                                  # 0 버튼이 가로로 두칸을 차지하게 열 위치 조정하기 위해 선언
            for col, btn_text in enumerate(row_values):
                button = QPushButton(btn_text)              # 버튼 생성
                button.setFixedSize(70, 60)                 # 버튼 사이즈
                button.setStyleSheet("font-size: 18px;")    # 버튼 글자 크기
                # 0 버튼 인 경우
                if btn_text == '0':
                    button.setFixedSize(140, 60) # 두 칸으로 설정
                    grid.addWidget(button, row + 1, 0, 1, 2)    # 행 + 1 (출력창 다음줄부터), 열=0, rowspan=1, colspan=2
                    col_offset = 1    # 이후 열 위치 조정
                else:
                    # 나머지 버튼은 1칸씩 차지
                    grid.addWidget(button, row + 1, col + col_offset)
                # 버튼 액션 추가
                button.clicked.connect(self.buttonClicked)
        # 전체 레이아웃 구성: 결과 출력 창 + 버튼 그리드
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.display) # 결과 출력 창 추가
        main_layout.addLayout(grid)         # 버튼 그리드 추가
        self.setLayout(main_layout)         # 최종 레이아웃 적용
    # 4칙 연산이 가능하도록 코드를 추가한다.
    def buttonClicked(self):
        sender = self.sender()  # 어떤 버튼이 눌렸는지 확인
        text = sender.text()    # 버튼의 텍스트
        # AC
        if text == 'AC':
            self.current_expression = "" # 초기화
            self.display.setText("0")    # 결과 출력 창의 결과를 0으로 변경
        # 더하기, 빼기
        elif text == '+/-':
            if self.current_expression:
                try:
                    value = str(-1 * float(eval(self.current_expression.replace('×', '*').replace('÷', '/'))))
                    self.current_expression = value
                    self.display.setText(value)
                except:
                    self.display.setText("Error")
                    self.current_expression = ""
        # 백분율
        elif text == '%':
            try:
                value = str(float(eval(self.current_expression.replace('×', '*').replace('÷', '/'))) / 100)
                self.current_expression = value
                self.display.setText(value)
            except:
                self.display.setText("Error")
                self.current_expression = ""
        # 결과 표시
        elif text == '=':
            try:
                result = str(eval(self.current_expression.replace('×', '*').replace('÷', '/')))
                self.display.setText(result)
                self.current_expression = result
            except:
                self.display.setText("Error")
                self.current_expression = ""
        else:
            # 숫자나 연산자 버튼
            if self.display.text() == "0" and text not in ['+', '-', '×', '÷', '.']:    # 첫 입력이 숫자일 때 0 제거
                self.display.setText(text)
                self.current_expression = text
            else:
                # 기존 수식에 버튼 텍스트를 추가
                self.current_expression += text
                self.display.setText(self.current_expression)


if __name__ == "__main__":
    app = QApplication(sys.argv) # PyQt5 객체 생성
    calc = Calculator()          # Calculator 객체 생성
    calc.show()                  # 창 띄우기
    sys.exit(app.exec_())        # 이벤트 실행 및 앱 종료 대기