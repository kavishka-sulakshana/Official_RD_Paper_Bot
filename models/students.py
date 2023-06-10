from connection import db as database

students_ref = database.collection('students')

def get_all_students():
    return students_ref.stream()

def add_student(student):
    students_ref.document(student['barcode']).set(student)