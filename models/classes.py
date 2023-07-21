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


def get_all_papers(clzID):
    return classes_ref.document(clzID).collection('papers').stream()

# Analitical Functions


def get_student_marks(clzID,  barcode) -> dict:
    class_dict = {}
    for doc in get_all_papers(clzID):
        paper_id = doc.id
        res = get_marks(clzID, paper_id, barcode)
        if res.exists:
            class_dict[paper_id] = res.to_dict()['marks']
        else:
            class_dict[paper_id] = None
    return class_dict


def get_average(marks: dict) -> tuple:
    total = 0
    count = 0
    for key in marks:
        if marks[key] is not None:
            total += float(marks[key])
            count += 1
    if count == 0:
        return (0, 0)
    return (total/count, count)
