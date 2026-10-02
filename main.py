from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

students = {}
next_id = 1


class Student(BaseModel):
    name: str
    id_number: str
    gpa: float


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    gpa: Optional[float] = None


@app.get("/students")
def get_all_students():
    return students


@app.post("/students", status_code=201)
def create_student(student: Student):
    global next_id
    students[next_id] = student.dict()
    result = {"id": next_id, "student": student}
    next_id += 1
    return result


@app.put("/students/{student_id}")
def update_student(student_id: int, update: StudentUpdate):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")

    data = students[student_id]

    if update.name:
        data["name"] = update.name

    if update.gpa is not None:
        data["gpa"] = update.gpa

    return data


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")

    del students[student_id]

    return {
        "message": f"Student {student_id} deleted successfully"
    }