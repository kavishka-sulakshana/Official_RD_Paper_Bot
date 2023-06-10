from connection import db as database

classes_ref = database.collection('classes')

def get_all_classes():
    return classes_ref.stream()

def add_class(clz):
    classes_ref.document(clz['name']).set(clz)