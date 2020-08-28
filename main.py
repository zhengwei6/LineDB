from db_package.models import *
from db_package.models import _Class

if __name__ == '__main__':
  # step 1 : create_table()
  
  # step 2 : create user, student, class object
  
  # new_user    = User.create_user(account="myaccount", password="ji32k7au4a83")
  # new_student = Student.create_student(student_name="zhengwei")
  # new_class   = _Class.create_class(class_name="105")
  # new_student.assign_to_user(new_user)
  
  # find_student  = Student.read_student_by_name("zhengwei")
  # find_class    = _Class.read_class_by_name("105")
  # find_student.assign_to_class(find_class)
  # print(find_student)
  
  # new_user    = User.create_user(account="myaccountttt", password="ji32k7au4a83")
  # find_teacher  = Teacher.read_teacher_by_name("www")
  # find_class    = _Class.read_class_by_name("105")
  # find_teacher.assign_to_user(new_user)
  # find_teacher.assign_to_class(find_class)
  # print(find_teacher)
  
  
  # new_grade     = Grade.create_grade(grade_name="math", grade_value="98")
  # find_student  = Student.read_student_by_name(student_name="zhengwei")
  # new_grade.assign_to_student(find_student)
  
  # new_board       = Board.create_board(board_str="87878")
  # find_class      = _Class.read_class_by_name("105")
  # new_board.assign_to_class(find_class)
  
  # read_student = Student.read_student_by_name(student_name="zhengwei")
  # read_parent  = Parent.read_parent_by_name(parent_name="pppp")
  # read_student.assign_to_parent(read_parent)
  
  # find_user     = User.read_user_by_account("myaccount")
  # new_parent    = Parent.create_parent(parent_name="pppp")
  # find_class    = _Class.read_class_by_name("105")
  # new_parent.assign_to_user(find_user)
  # new_parent.assign_to_class(find_class)
  
  # new_student = create_student(student_name="willy")
  # new_class   = create_class(class_name="105")
  
  # update_student_to_user(new_user, new_student)
  
  
  # student_parm = dict(student_parameter)
  # student_parm['student_name'] = "willy"
  # new_student = create_student(student_parm)
  
  # step 3 : update student to user
  # first read the user and student
  # user_object    = read_user_by_account("willyyy")
  # student_object = read_student_by_name("willy")
  # update_student_to_user(user_object, student_object)
  
  # step 4 : create new class
  
  
  
  # class_parm = dict(class_parameter)
  # class_parm['class_name'] = "104"
  # new_class = create_class(class_parm)
  
  # new_class  = read_class_by_name("104")
  # user_parm  = dict(user_parameter)
  # user_parm['account'] = "my"
  # user_parm['password'] = "ji32k7au4a83"
  # new_user  = create_user(user_parm)
  # update_class_to_user(new_user, new_class)
  
  # new_user = read_user_by_account("myaccountyy")
  # student_parm = dict(student_parameter)
  # student_parm['student_name'] = "willy"
  # new_student = create_student(student_parm)
  # new_student = update_student_to_user(new_user, new_student)
  # print(new_student)
  
  # old_user = read_user_by_account("myaccountyy")
  # delete_object(old_user)
  
  class_object = _Class.read_class_by_name("105")
  delete_object(class_object)