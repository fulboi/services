import requests

student_url = 'http://localhost:8000'
student_login_url = f'{student_url}/login'

teacher_url = 'http://localhost:8001'
add_student_url = f'{teacher_url}/add_student'
get_students_url = f"{teacher_url}/get_students"
add_question_url = f'{teacher_url}/add_question'
get_question_by_id_url = f'{teacher_url}/get_question_by_id'
get_questions_url = f'{teacher_url}/get_questions'
delete_question_url = f'{teacher_url}/delete_question'
delete_student_url = f'{teacher_url}/delete_student'
reset_student_url = f'{teacher_url}/reset_student'

new_question = {
    "id": 666,
    "question_text": "What is 99/9?",
    "question_answer": 11
}


def test_1_add_student():
    res = requests.post(f"{add_student_url}?name=test1")
    assert res.status_code == 200


def test_2_find_student():
    res = requests.get(f"{student_login_url}?name=test1")
    assert res.status_code == 200


def test_3_add_question():
    res = requests.post(f"{add_question_url}", json=new_question)
    assert res.status_code == 200


def test_4_check_question():
    res = requests.get(f"{get_questions_url}").json()
    assert new_question in res


def test_5_find_question_by_id():
    res = requests.get(f"{get_question_by_id_url}?question_id=666").json()
    assert res == new_question


def test_6_delete_question():
    res = requests.delete(f"{delete_question_url}?question_id=666")
    assert res.status_code == 200

def test_7_check_question_deletion():
    res = requests.get(f"{get_questions_url}").json()
    assert new_question not in res

def test_8_reset_student():
    res = requests.delete(f"{reset_student_url}?name=test1")
    assert res.status_code == 200

def test_9_delete_student():
    res = requests.delete(f"{reset_student_url}?name=test1")
    assert res.status_code == 200