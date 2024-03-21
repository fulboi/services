import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from typing import Annotated

from sqlalchemy.orm import Session

from database import teacher_database as database
from database.teacher_database import StudentDB, QuestionDB

from model.teacher import Student, Question

app = FastAPI()
database.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

current_question = 0
student = 0

@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive():
    return {'message': 'service alive'}


@app.get("/get_questions")
async def get_questions(db: db_dependency):
    try:
        questions_db = db.query(QuestionDB).all()
        return questions_db
    except Exception as e:
        raise HTTPException(status_code=404, detail="Connection error")


@app.get("/get_question_by_id")
async def get_question_by_id(question_id: int, db: db_dependency):
    try:
        question_db = db.query(QuestionDB).filter(QuestionDB.id == question_id).first()
        return question_db
    except Exception as e:
        raise HTTPException(status_code=404, detail="Question not found")


@app.post("/add_question")
async def add_question(question: Question, db: db_dependency):
    try:
        question_db = QuestionDB(
            id=question.id,
            question_text=question.question_text,
            question_answer=question.question_answer
        )
        db.add(question_db)
        db.commit()
        return question_db
    except Exception as e:
        raise HTTPException(status_code=404, detail="Failed to add question")


@app.delete("/delete_question")
async def delete_question(question_id: int, db: db_dependency):
    try:
        question_db = db.query(QuestionDB).filter(QuestionDB.id == question_id).first()
        if question_db:
            db.delete(question_db)
            db.commit()
            return "Item deleted successfully"
        else:
            raise HTTPException(status_code=404, detail="Question not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/get_students")
async def get_students(db: db_dependency):
    try:
        students_db = db.query(StudentDB).all()
        return students_db
    except Exception as e:
        raise HTTPException(status_code=404, detail="Connection error")

@app.post("/add_student")
async def add_student(name: str, db: db_dependency):
    try:
        student_db = StudentDB(
            name=name,
            current_question=0,
            points=0
        )
        db.add(student_db)
        db.commit()
        return student_db
    except Exception as e:
        raise HTTPException(status_code=404, detail="Failed to add student")

@app.delete("/reset_student")
async def reset_student(name: str, db: db_dependency):
    student_db = db.query(StudentDB).filter(StudentDB.name == name).first()
    student_db.current_question = 0
    student_db.points = 0
    db.commit()
    return f"{student_db.name} score was cleared"

@app.delete("/delete_student")
async def delete_student(name: str, db: db_dependency):
    try:
        student_db = db.query(StudentDB).filter(StudentDB.name == name).first()
        if student_db:
            db.delete(student_db)
            db.commit()
            return "Student deleted successfully"
        else:
            raise HTTPException(status_code=404, detail="Student not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))
