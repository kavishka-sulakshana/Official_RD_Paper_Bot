import models.classes as classes
import models.students
import pprint

# res2 = classes.get_marks('2023 Theory', '33', '89287283')
# data = res2.to_dict()
# pprint.pprint(data['student_id'].get().to_dict()['name'])
# pprint.pprint(data['marks'])
# pprint.pprint(data['rank'])
# res3 = res2.to_dict()['student_id']
# for doc in res3:
#     pprint.pprint(doc.to_dict())
# abc = doc.to_dict()
res2 = classes.get_student_marks('2023 Theory', "55519610")
res2 = classes.get_average(res2)
pprint.pprint(res2)
