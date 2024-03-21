from sqlalchemy import create_engine, Column, String,  Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL = 'postgresql://secUREusER:StrongEnoughPassword)@51.250.26.59:5432/query'

engine = create_engine(URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class QuestionDB(Base):
    __tablename__ = 'questions_baranov'

    id = Column(Integer, primary_key=True)
    question_text = Column(String, nullable=False)
    question_answer = Column(Integer, nullable=False)


class StudentDB(Base):
    __tablename__ = 'students_baranov'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    current_question = Column(Integer, nullable=False)
    points = Column(Integer, nullable=False)