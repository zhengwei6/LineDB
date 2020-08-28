from app  import app
from models import *

if __name__ == '__main__':
  user1_parm = dict(user_parameter)
  user1_parm['account'] = 'leo'
  user1_parm['password'] = 'ji32k7au4a83'
  student1_parm = dict(student_parameter)
  student1_parm['student_name'] = 'zzz'
  CreateStudentWithUser(user1_parm, student1_parm)