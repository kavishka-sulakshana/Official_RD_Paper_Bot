from models.connection import db as database

classes_ref = database.collection('classes')


def get_all_classes():
    return classes_ref.stream()


def get_class_by_name(name):
    return classes_ref.document(name).get()


def get_id_paper_by_name(clzID, paperName):
    res = classes_ref.document(clzID).collection(
        'papers').where('name', '==', paperName)
    return res.get()[0].id


def get_marks(clzID, paperName, barcode):
    return classes_ref.document(clzID).collection('papers').document(paperName).collection('students').document(
        barcode).get()


def add_class(clz):
    classes_ref.document(clz['name']).set(clz)
