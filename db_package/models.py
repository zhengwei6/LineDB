from .app import *
from .parameter import *

user_class      = db.Table(
                   'user_class',
                   db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                   db.Column('class_id', db.Integer, db.ForeignKey('class.id'))
                  )
                  
student_parent  = db.Table(
                   'student_parent',
                   db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
                   db.Column('parent_id', db.Integer, db.ForeignKey('parent.id'))
                  )
                  
class User(db.Model):
  __table__name = 'user'
  id           = db.Column(db.Integer, primary_key=True)
  account      = db.Column(db.String(80), nullable=False, unique=True)
  password     = db.Column(db.String(191), nullable=False)
  email        = db.Column(db.String(80))
  phone        = db.Column(db.String(80))
  create_at    = db.Column(db.String(80))
  
  # relationship one to one mapping https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/#simple-example
  student = db.relationship(
              'Student',
              backref = 'user',
              cascade = "all,delete",
              lazy    = 'dynamic'
            )
  
  parent  = db.relationship(
              'Parent',
              backref = 'user',
              cascade = "all,delete",
              lazy    = 'dynamic'
            )
  
  teacher = db.relationship(
              'Teacher',
              backref = 'user',
              cascade = "all,delete",
              lazy    = 'dynamic'
            )
            
  classes = db.relationship(
              '_Class', 
              secondary=user_class, 
              lazy='subquery',
              backref=db.backref('user', lazy=True)
            )
            
  def create_user(**options):
    user_parm = dict(const_user_parameter)
    for arg in options.items():
      if arg[0] in const_user_parameter:
        user_parm[arg[0]] = arg[1]
    user = User.read_user_by_account(user_parm['account'])
    if user != None:
      return None
    user = User(user_parameter=user_parm)
    db.session.add(user)
    db.session.commit()
    return user
    
  def read_user_by_account(account):
    user    = User.query.filter_by(account=account)
    return user.first()  
    
  
  def __init__(self, user_parameter):
    self.account   = user_parameter['account']
    self.password  = user_parameter['password']
    self.email     = user_parameter['email']
    self.phone     = user_parameter['phone']
    self.create_at = user_parameter['create_at']
    
  def __repr__(self):
    return 'id:%s, account:%s' % \
            (self.id, self.account)
  
class Student(db.Model):
  __table__name = 'student'
  id            = db.Column(db.Integer, primary_key=True)
  student_name  = db.Column(db.String(80), nullable=False)
  user_id       = db.Column(db.Integer, db.ForeignKey('user.id')) 
  class_id      = db.Column(db.Integer, db.ForeignKey('class.id'))
  
  grade         = db.relationship(
                    'Grade',
                    backref = 'student',
                    cascade = "all,delete",
                    lazy    = 'dynamic'
                  )
                  
  parents       = db.relationship(
                    'Parent', 
                    secondary=student_parent, 
                    lazy='subquery',
                    backref=db.backref('student', lazy=True)
                  )
                  
  def create_student(**options):
    student_parm = dict(const_student_parameter)
    for arg in options.items():
      if arg[0] in const_student_parameter:
        student_parm[arg[0]] = arg[1]
    student = Student(student_parm)
    db.session.add(student)
    db.session.commit()
    return student

  def read_student_by_id(student_id):
    student = Student.query.filter_by(id=student_id)
    return student.first()

  def read_students_by_name(student_name):
    student = Student.query.filter_by(student_name=student_name)
    return student.all()
    
  def read_student_by_name(student_name):
    student = Student.query.filter_by(student_name=student_name)
    return student.first()

  def assign_to_user(self, user_object):
    self.user_id = user_object.id
    db.session.commit()
    return 1
  
  def assign_to_class(self, class_object):
    self.class_id = class_object.id
    db.session.commit()
    return 1
  
  def assign_to_parent(self, parent_object):
    self.parents.append(parent_object)
    db.session.commit()
    return 1
  
  def __init__(self, student_parameter):
    self.student_name = student_parameter['student_name']
  
  def __repr__(self):
    return 'id:%s student_name:%s, user_id:%s' % \
            (self.id, self.student_name, self.user_id)
            
class Parent(db.Model):
  __table__name = 'parent'
  id            = db.Column(db.Integer, primary_key=True)
  parent_name   = db.Column(db.String(80))
  user_id       = db.Column(db.Integer, db.ForeignKey('user.id'))
  class_id      = db.Column(db.Integer, db.ForeignKey('class.id'))
  
  def create_parent(**options):
    parent_parm = dict(const_parent_parameter)
    for arg in options.items():
      if arg[0] in const_parent_parameter:
        parent_parm[arg[0]] = arg[1]
    parent = Parent(parent_parm)
    db.session.add(parent)
    db.session.commit()
    return parent
    
  def read_parent_by_name(parent_name):
    parent  = Parent.query.filter_by(parent_name=parent_name)
    return parent.first()

  def read_parents_by_name(parent_name):
    parent  = Parent.query.filter_by(parent_name=parent_name)
    return parent.all()

  def assign_to_user(self, user_object):
    self.user_id = user_object.id
    db.session.commit()
    return 1
  
  def assign_to_class(self, class_object):
    self.class_id = class_object.id
    db.session.commit()
    return 1

  def __init__(self, parent_parameter):
    self.parent_name = parent_parameter['parent_name']
  
  def __repr__(self):
    return 'id:%s parent_name:%s, user_id:%s' % \
            (self.id, self.parent_name, self.user_id)
    
class Teacher(db.Model):
  __table__name = 'teacher'
  id            = db.Column(db.Integer, primary_key=True)
  teacher_name  = db.Column(db.String(80))
  user_id       = db.Column(db.Integer, db.ForeignKey('user.id'))
  class_id      = db.Column(db.Integer, db.ForeignKey('class.id'))
  
  def create_teacher(**options):
    teacher_parm = dict(const_teacher_parameter)
    for arg in options.items():
      if arg[0] in const_teacher_parameter:
        teacher_parm[arg[0]] = arg[1]
    teacher = Teacher(teacher_parm)
    db.session.add(teacher)
    db.session.commit()
    return teacher
  
  def read_teacher_by_name(teacher_name):
    teacher  = Teacher.query.filter_by(teacher_name=teacher_name)
    return teacher.first()
    
  def read_teachers_by_name(teacher_name):
    teacher  = Teacher.query.filter_by(teacher_name=teacher_name)
  
  def assign_to_user(self, user_object):
    self.user_id = user_object.id
    db.session.commit()
    return 1
  
  def assign_to_class(self, class_object):
    self.class_id = class_object.id
    db.session.commit()
    return 1
    
  def __init__(self, teacher_parameter):
    self.teacher_name = teacher_parameter['teacher_name']
  
  def __repr__(self):
    return 'id:%s teacher_name:%s, user_id:%s' % \
            (self.id, self.teacher_name, self.user_id)
            
class Grade(db.Model):
  __table__name = 'grade'
  id            = db.Column(db.Integer, primary_key=True)
  grade_name    = db.Column(db.String(80))
  grade_value   = db.Column(db.String(80))
  student_id    = db.Column(db.Integer, db.ForeignKey('student.id'))
  
  def create_grade(**options):
    grade_parm = dict(const_grade_parameter)
    for arg in options.items():
      if arg[0] in const_grade_parameter:
        grade_parm[arg[0]] = arg[1]
    grade   = Grade(grade_parm)
    db.session.add(grade)
    db.session.commit()
    return grade
  
  def assign_to_student(self, student_object):
    self.student_id = student_object.id
    db.session.commit()
    return 1
  
  def __init__(self, grade_parameter):
    self.grade_name  = grade_parameter['grade_name']
    self.grade_value = grade_parameter['grade_value']
  
  def __repr__(self):
    return 'id:%s grade_name:%s, student_id:%s' % \
            (self.id, self.grade_name, self.student_id)
  
class _Class(db.Model):
  __table__name = 'class'
  id            = db.Column(db.Integer, primary_key=True)
  
  class_name    = db.Column(db.String(80))
  
  student       = db.relationship(
                    'Student',
                    backref = 'class',
                    cascade = "all,delete",
                    lazy    = 'dynamic'
                  )
                  
  parent        = db.relationship(
                    'Parent',
                    backref = 'class',
                    cascade = "all,delete",
                    lazy    = 'dynamic'
                  )
                  
  teacher       = db.relationship(
                    'Teacher',
                    backref = 'class',
                    cascade = "all,delete",
                    lazy    = 'dynamic'
                  )
                  
  board         = db.relationship(
                    'Board',
                    backref = 'class',
                    cascade = "all,delete",
                    lazy    = 'dynamic'
                  )                 
                  
  def create_class(**options):
    class_parm = dict(const_class_parameter)
    for arg in options.items():
      if arg[0] in const_class_parameter:
        class_parm[arg[0]] = arg[1]
    _class = _Class(class_parameter=class_parm)
    db.session.add(_class)
    db.session.commit()
    return _class

  def read_class_by_id(class_id):
    _class = _Class.query.filter_by(id=class_id)
    return _class.first()

  def read_class_by_name(class_name):
    _class = _Class.query.filter_by(class_name=class_name)
    return _class.first()

  def read_classes_by_name(class_name):
    _class = _Class.query.filter_by(class_name=class_name)
    return _class.all()
    
  def __init__(self, class_parameter):
    self.class_name = class_parameter['class_name']
  
  def __repr__(self):
    return 'id:%s class_name:%s' % \
           (self.id, self.class_name)
    
class Board(db.Model):
  __table__name = 'board'
  id            = db.Column(db.Integer, primary_key=True)
  board_str     = db.Column(db.String(80))
  class_id      = db.Column(db.Integer, db.ForeignKey('class.id'))
  
  def create_board(**options):
    board_parm = dict(const_board_parameter)
    for arg in options.items():
      if arg[0] in const_board_parameter:
        board_parm[arg[0]] = arg[1]
    board  = Board(board_parameter=board_parm)
    db.session.add(board)
    db.session.commit()
    return board
  
  def assign_to_class(self, class_object):
    self.class_id = class_object.id
    db.session.commit()
    return 1
    
  def __init__(self, board_parameter):
    self.board_str = board_parameter['board_str']
  
  def __repr__(self):
    return 'id:%s class_id:%s' %\
           (self.id, self.class_id)
# db.create_all()
# db.session.commit()

'''
create_student_by_user
create_teacher_by_user
create_parent_by_user
'''
def create_student_by_user(user_parameter, student_parameter):
  # create user
  user = create_user(user_parameter)
  if user == None:
    return None
  student = Student(student_parameter)
  user.student = student
  user.role    = 'Student'
  db.session.add(student)
  db.session.commit()
  return student

def create_teacher_by_user(user_parameter, teacher_parameter):
  # create user
  user = create_user(user_parameter)
  if user == None:
    return None
  teacher = Teacher(teacher_parameter)
  user.teacher = teacher
  user.role    = 'Teacher'
  db.session.add(teacher)
  db.session.commit()
  return teacher

def create_parent_by_user(user_parameter, parent_parameter):
  # create user
  user = create_user(user_parameter)
  if user == None:
    return None
  parent = Parent(parent_parameter)
  user.parent = parent
  user.role   = 'Parent'
  db.session.add(parent)
  db.session.commit()
  return parent

'''
update_user_to_class
'''
def update_class_to_user(user_object, class_object):
  if user_object == None:
    return None
  user_object.classes.append(class_object)
  db.session.commit()
  return user_object

def update_student_to_user(user_object, student_object):
  if student_object == None:
    return None
  student_object.user_id = user_object.id
  db.session.commit()
  return user_object

  
# class_id = CreateClass("501")
# print(class_id)
#CreateStudent("willy", 7, "Willy")
# print(ReadClass("501"))
# CreateParentFromName("willy")
# CreateUserFromAccount("ji32k7au4a83")
# user   = ReadUserFromAccount("ji32k7au4a83")
# parent = ReadParentFromName("willy")

# user.parent = parent
# db.session.commit()
# user1_parm = dict(user_parameter)
# user1_parm['account'] = 'willyy'
# user1_parm['password'] = 'ji32k7au4a3'
# CreateUser(user1_parm)
# print(ReadUserFromAccount("willy"))
# user1_parm = dict(user_parameter)
# user1_parm['account'] = 'leo'
# user1_parm['password'] = 'ji32k7au4a83'
# student1_parm = dict(student_parameter)
# student1_parm['student_name'] = 'zzz'
# CreateStudentWithUser(user1_parm, student1_parm)

