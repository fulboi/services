import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Form, Header
from typing import Annotated
from keycloak import KeycloakOpenID
from sqlalchemy.orm import Session

from database import student_database as database
from database.student_database import StudentDB, QuestionDB

from model.student import Student

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

KEYCLOAK_URL = "http://keycloak:8080/"
KEYCLOAK_CLIENT_ID = "testClient"
KEYCLOAK_REALM = "testRealm"
KEYCLOAK_CLIENT_SECRET = "**********"

keycloak_openid = KeycloakOpenID(server_url=KEYCLOAK_URL,
                                  client_id=KEYCLOAK_CLIENT_ID,
                                  realm_name=KEYCLOAK_REALM,
                                  client_secret_key=KEYCLOAK_CLIENT_SECRET)

from prometheus_fastapi_instrumentator import Instrumentator
Instrumentator().instrument(app).expose(app)

@app.post("/get_jwt_token")
async def login(username: str = Form(...), password: str = Form(...)):
    try:
        token = keycloak_openid.token(grant_type=["password"],
                                      username=username,
                                      password=password)
        global user_token
        user_token = token
        return token
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Не удалось получить токен")

def chech_for_role_test(token):
    try:
        token_info = keycloak_openid.introspect(token["access_token"])
        if "test" not in token_info["realm_access"]["roles"]:
            raise HTTPException(status_code=403, detail="Access denied")
        return token_info
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token or access denied")

@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive(token:str = Header()):
    if (chech_for_role_test(token)):
        return {'message': 'service alive'}
    else:
        raise HTTPException(status_code=401, detail="Invalid token or access denied")

@app.get("/login")
async def login(name: str, db: db_dependency):
    if (chech_for_role_test()):
        try:
            student_db = db.query(StudentDB).filter(StudentDB.name == name).first()
            global student
            student = Student(
                id=0,
                name=student_db.name,
                current_question=student_db.current_question,
                points=student_db.points
            )
            return f"You logged in as {name}"
        except Exception as e:
            raise HTTPException(status_code=404, detail="Student not found")
    else:
        return "Wrong JWT Token"

@app.get("/get_question")
async def get_question(db: db_dependency):
    try:
        global student
        question_db = db.query(QuestionDB).filter(QuestionDB.id == student.current_question).first()
        return question_db.question_text
    except Exception as e:
        return "Test completed"


@app.post("/send_the_answer")
async def send_the_answer(answer: int, db: db_dependency):
    try:
        global student
        question_db = db.query(QuestionDB).filter(QuestionDB.id == student.current_question).first()
        student.current_question += 1

        if answer == question_db.question_answer:
            try:
                student_db = db.query(StudentDB).filter(StudentDB.name == student.name).first()
                student.points += 1
                student_db.points += 1
                student_db.current_question += 1
                db.commit()
                return "Correct!"
            except Exception as e:
                raise HTTPException(status_code=404, detail="Can't access students")
        else:
            try:
                student_db = db.query(StudentDB).filter(StudentDB.name == student.name).first()
                student_db.current_question += 1
                db.commit()
                return "Incorrect!"
            except Exception as e:
                raise HTTPException(status_code=404, detail="Can't access students")
            return "Wrong!"
    except Exception as e:
        raise HTTPException(status_code=404, detail="Test completed")


@app.post("/get_points")
async def get_points():
    try:
        return student.points
    except Exception as e:
        raise HTTPException(status_code=404, detail="You are not logged in")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))
