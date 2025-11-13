# models.py
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
import datetime

# database.py에서 정의한 Base 클래스를 가져옴
from database import Base


# (수행과제 6) Question 모델
class Question(Base):
    __tablename__ = 'question'

    # (수행과제 6) id (PK), subject, content, create_date
    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False, default=datetime.datetime.now)

    # Question 모델에서 Answer 모델을 참조하기 위한 관계 설정
    # 'answers'는 Question 객체에서 .answers 로 답변 목록에 접근하게 해줌
    # back_populates='question'은 Answer 모델의 'question' 속성과 연결됨
    answers = relationship('Answer', back_populates='question')

    def __repr__(self):
        return f'<Question {self.id}: {self.subject}>'


# (수행과제 6) Answer 모델
class Answer(Base):
    __tablename__ = 'answer'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False, default=datetime.datetime.now)

    # Question 테이블의 id 컬럼을 참조하는 외래 키
    question_id = Column(Integer, ForeignKey('question.id'))

    # Answer 모델에서 Question 모델을 참조하기 위한 관계 설정
    # back_populates='answers'는 Question 모델의 'answers' 속성과 연결됨
    question = relationship('Question', back_populates='answers')

    def __repr__(self):
        return f'<Answer {self.id}>'