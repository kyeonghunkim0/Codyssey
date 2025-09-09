from step6.calculator import Calculator
import sys
# Python으로 UI를 만들 수 있는 PyQT 라이브러리를 설치한다.
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QVBoxLayout, QLineEdit
from PyQt5.QtCore import Qt

class Calculator:
    def __init__(self):
        self.reset;
    # 초기화
    def reset(self):
        self.current = "0"
        self.operator = None
        self.operand = None
    # 숫자 입력
    def inputNumber(self, num):
        if self.current == 0:
            self.current = num
        else:
            self.current += num
    # 소수점 입력
    def inputDecimal(self):
        if '.' not in self.current:
            self.current += '.'
    # 연산자 설정
    def setOperator(self, op):
        self.operator = op
        try:
            self.operand = float(self.current)
        except ValueError:
            self.operand = 0.0
        self.current = "0"
    # 음수양수
    def negative_positive(self):
        if self.current.startswith('-'):
            self.current = self.current[1:]
        else:
            if self.current != "0":
                self.current = '-' + self.current
    # 퍼센트
    def percent(self):
        try:
            value = float(self.current) / 100
            self.current = str(value)
        except ValueError:
            self.current = "Error"
    # 계산
    def equal(self):
        # 연산자 없으면 return
        if self.operator is None or self.operand is None:
            return

        try:
            right = float(self.current)
            if self.operator == '+':
                result = self.add(self.operand, right)
            elif self.operator == '-':
                result = self.subtract(self.operand, right)
            elif self.operator == "x":
                result = self.multiply(self.operand, right)
            elif self.operator == '÷':
                result = self.divide(self.operand, right)

            # 소수점 6자리 반올림
            result = round(result, 6)
            # 너무 큰 값이면 Overflow 처리
            if abs(result) > 1e100:
                raise OverflowError
            # 결과 문자열 정리
            self.current = str(result).rstrip('0').rstrip('.') if '.' in str(result) else str(result)
            # 계산 완료 후 상태 초기화
            self.operator = None
            self.operand = None
        # 0으로 나누려 했을 때는 ZeroDivisionError 발생시켜서 처리
        except ZeroDivisionError:
            raise
        # 결과가 너무 커서 처리할 수 없을 때 OverflowError 발생
        except OverflowError:
            raise
        except Exception:
            self.current = "Error"

    # 4칙 연산 함수들
    # 더하기
    def add(self, a, b):
        return a + b
    # 빼기
    def subtract(self, a, b):
        return a - b
    # 곱하기
    def multiply(self, a, b):
        return a * b
    # 나누기
    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError
        return a / b


    if __name__ == "__main__":
        app = QApplication(sys.argv)  # PyQt5 객체 생성
        calc = Calculator()  # Calculator 객체 생성
        calc.show()  # 창 띄우기
        sys.exit(app.exec_())  # 이벤트 실행 및 앱 종료 대기