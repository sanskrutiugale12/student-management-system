from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

@app.post("/students")
def create_student(name: str, course: str, marks: int):

    # Data to be inserted into Supabase
    student = {
        "name": name,
        "course": course,
        "marks": marks
    }

    # Insert student into Supabase
    response = (
        supabase
        .table("Students")
        .insert(student)
        .execute()
    )

    # Return database response
    return {
        "message": "Student created successfully",
        "data": response.data
    }
@app.get("/students")
def get_students():

    # Read all records from students table
    response = (
        supabase
        .table("Students")
        .select("*")
        .execute()
    )

    # Send database records as API response
    return {
        "message": "Students fetched successfully",
        "data": response.data
    }
# UPDATE
@app.put("/students/{student_id}")
def update_student(student_id: int, marks: int):

    # Data to be updated
    updated_data = {
        "marks": marks
    }

    # Update student in Supabase
    response = (
        supabase
        .table("Students")
        .update(updated_data)
        .eq("id", student_id)
        .execute()
    )

    return {
        "message": "Student updated successfully",
        "data": response.data
    }


# DELETE
@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    # Delete student from Supabase
    response = (
        supabase
        .table("Students")
        .delete()
        .eq("id", student_id)
        .execute()
    )

    return {
        "message": "Student deleted successfully",
        "data": response.data
    }