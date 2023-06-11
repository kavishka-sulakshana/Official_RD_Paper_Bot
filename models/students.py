from models.connection import db as database

students_ref = database.collection('students')


def get_all_students():
    return students_ref.get()


def add_student(student):
    students_ref.document(student['barcode']).set(student)


def get_student_by_barcode(barcode):
    return students_ref.document(barcode).get()
