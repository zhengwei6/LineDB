from .app import *
from .parameter import *
import hashlib
from sqlalchemy.dialects.mysql import BIGINT
import random

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
  hash_account = db.Column(BIGINT(unsigned=True), nullable=False, unique=True)
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
              lazy='dynamic',
              backref=db.backref('user', lazy='dynamic')
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
  
  def add_to_class(self, class_object):
    if class_object == None:
      return None
    self.classes.append(class_object)
    db.session.commit()
    return 1
    
  def read_user_by_account(account):
    hash_account = int(hashlib.md5(account.encode('utf-8')).hexdigest(), 16) % 18446744073709551615
    user    = User.query.filter_by(hash_account=hash_account)
    return user.first()  
  
  def read_user_by_id(user_id):
    user    = User.query.filter_by(id=user_id)
    return user.first()
  
  def __init__(self, user_parameter):
    self.account   = user_parameter['account']
    self.password  = user_parameter['password']
    self.email     = user_parameter['email']
    self.phone     = user_parameter['phone']
    self.create_at = user_parameter['create_at']
    self.hash_account = int(hashlib.md5(self.account.encode('utf-8')).hexdigest(), 16) % 18446744073709551615
    
  def __repr__(self):
    return 'id:%s, account:%s' % \
            (self.id, self.account)
  
class Student(db.Model):
  __table__name = 'student'
  id            = db.Column(db.Integer, primary_key=True)
  student_name  = db.Column(db.String(80), nullable=False)
  user_id       = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
  class_id      = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
  
  grade         = db.relationship(
                    'Grade',
                    backref = 'student',
                    cascade = "all,delete",
                    lazy    = 'dynamic'
                  )
  
  status        = db.relationship(
                    'Status',
                    backref = 'student',
                    cascade = "all,delete",
                    lazy    = 'dynamic'
                  )
                  
  parents       = db.relationship(
                    'Parent', 
                    secondary=student_parent, 
                    lazy='subquery',
                    backref=db.backref('student', lazy='dynamic')
                  )
                  
  def create_student(user_object, class_object, **options):
    if user_object == None or class_object == None:
      return None
    student_parm = dict(const_student_parameter)
    for arg in options.items():
      if arg[0] in const_student_parameter:
        student_parm[arg[0]] = arg[1]
    student = Student(student_parm)
    student.user_id  = user_object.id
    student.class_id = class_object.id 
    db.session.add(student)
    db.session.commit()
    return student

  def read_student_by_id(student_id):
    student = Student.query.filter_by(id=student_id)
    return student.first()
  
  def assign_to_user(self, user_object):
    if user_object == None:
      return None
    self.user_id = user_object.id
    return 1
  
  def assign_to_class(self, class_object):
    if class_object == None:
      return None
    self.class_id = class_object.id
    db.session.commit()
    return 1
  
  def add_to_parent(self, parent_object):
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
  user_id       = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  class_id      = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
  
  def create_parent(user_object, class_object, **options):
    if user_object == None or class_object == None:
      return None
    parent_parm = dict(const_parent_parameter)
    for arg in options.items():
      if arg[0] in const_parent_parameter:
        parent_parm[arg[0]] = arg[1]
    parent = Parent(parent_parm)
    parent.user_id  = user_object.id
    parent.class_id = class_object.id 
    db.session.add(parent)
    db.session.commit()
    return parent
  
  def read_parent_by_id(parent_id):
    parent  = Parent.query.filter_by(id=parent_id)
    return parent.first()

  def read_parents_by_name(parent_name):
    parent  = Parent.query.filter_by(parent_name=parent_name)
    return parent.all()
  
  def assign_to_user(self, user_object):
    if user_object == None:
      return None
    self.user_id = user_object.id
    db.session.commit()
    return 1
    
  def assign_to_class(self, class_object):
    if class_object == None:
      return None
    self.class_id = class_object.id
    db.session.commit()
    return 1
  
  def add_to_student(self, student_object):
    if student_object == None:
      return None
    self.student.append(student_object)
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
  user_id       = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  class_id      = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
  
  def create_teacher(user_object, class_object, **options):
    if user_object == None or class_object == None:
      return None
    teacher_parm = dict(const_teacher_parameter)
    for arg in options.items():
      if arg[0] in const_teacher_parameter:
        teacher_parm[arg[0]] = arg[1]
    teacher = Teacher(teacher_parm)
    teacher.user_id  = user_object.id
    teacher.class_id = class_object.id 
    db.session.add(teacher)
    db.session.commit()
    return teacher
  
  def assign_to_user(self, user_object):
    if user_object == None:
      return None
    self.user_id = user_object.id
    db.session.commit()
    return 1

  def assign_to_class(self, class_object):
    if class_object == None:
      return None
    self.class_id = class_object.id
    db.session.commit()
    return 1
    
  def read_teacher_by_id(teacher_id):
    teacher  = Teacher.query.filter_by(id=teacher_id)
    return teacher.first()
  
  def __init__(self, teacher_parameter):
    self.teacher_name = teacher_parameter['teacher_name']
  
  def __repr__(self):
    return 'teacher_id:%s teacher_name:%s, user_id:%s' % \
            (self.id, self.teacher_name, self.user_id)
            
class Grade(db.Model):
  __table__name = 'grade'
  id            = db.Column(db.Integer, primary_key=True)
  date          = db.Column(db.String(80))
  subject       = db.Column(db.String(80))
  grade_name    = db.Column(db.String(80))
  grade_value   = db.Column(db.String(80))
  student_id    = db.Column(db.Integer, db.ForeignKey('student.id'))
  
  def create_grade(student_object, **options):
    if student_object == None:
      return None
    grade_parm = dict(const_grade_parameter)
    for arg in options.items():
      if arg[0] in const_grade_parameter:
        grade_parm[arg[0]] = arg[1]
    grade = Grade(grade_parm)
    grade.student_id = student_object.id
    db.session.add(grade)
    db.session.commit()
    return grade
  
  def read_grade_by_id(grade_id):
    grade  = Grade.query.filter_by(id=grade_id)
    return grade.first()
    
  def assign_to_student(self, student_object):
    self.student_id = student_object.id
    db.session.commit()
    return 1
  
  def __init__(self, grade_parameter):
    self.date        = grade_parameter['date']
    self.subject     = grade_parameter['subject']
    self.grade_name  = grade_parameter['grade_name']
    self.grade_value = grade_parameter['grade_value']
  
  def __repr__(self):
    return 'id:%s grade_name:%s, student_id:%s' % \
            (self.id, self.grade_name, self.student_id)
  
class _Class(db.Model):
  __table__name = 'class'
  id            = db.Column(db.Integer, primary_key=True)
  class_name    = db.Column(db.String(80))
  class_auth    = db.Column(db.Integer, unique=True, nullable=False)
  student       = db.relationship(
                    'Student',
                    backref = 'classes',
                    cascade = "all,delete",
                    lazy    = 'dynamic'
                  )
                  
  parent        = db.relationship(
                    'Parent',
                    backref = 'classes',
                    cascade = "all,delete",
                    lazy    = 'dynamic'
                  )
                  
  teacher       = db.relationship(
                    'Teacher',
                    backref = 'classes',
                    cascade = "all,delete",
                    lazy    = 'dynamic'
                  )
                  
  board         = db.relationship(
                    'Board',
                    backref = 'classes',
                    cascade = "all,delete",
                    lazy    = 'dynamic'
                  )                 
  learn         = db.relationship(
                    'Learn',
                    backref = 'classes',
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
  
  def read_class_by_auth(class_auth):
    _class = _Class.query.filter_by(class_auth=class_auth)
    return _class.first()
    
  def add_to_user(self, user_object):
    if user_object == None:
      return None
    self.user.append(user_object)
    db.session.commit()
    return 1
  
  def __init__(self, class_parameter):
    self.class_name = class_parameter['class_name']
    # auth
    auth_num = random.randint(10000000, 2147483647)
    _class = _Class.query.filter_by(class_auth= auth_num).first()
    while _class != None:
      auth_num = random.randint(10000000, 2147483647)
      _class = _Class.query.filter_by(class_auth=auth_num).first()
    self.class_auth = auth_num
    
  def __repr__(self):
    return 'id:%s class_name:%s' % \
           (self.id, self.class_name)
    
class Board(db.Model):
  __table__name = 'board'
  id            = db.Column(db.Integer, primary_key=True)
  author        = db.Column(db.String(80))
  date          = db.Column(db.String(80))
  board_str     = db.Column(db.String(500))
  class_id      = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
  
  def create_board(class_object, **options):
    if class_object == None:
      return None
    board_parm = dict(const_board_parameter)
    for arg in options.items():
      if arg[0] in const_board_parameter:
        board_parm[arg[0]] = arg[1]
    board  = Board(board_parameter=board_parm)
    board.class_id = class_object.id
    db.session.add(board)
    db.session.commit()
    return board
  
  def read_board_by_id(board_id):
    board    = Board.query.filter_by(id=board_id)
    return board.first()
  
  def assign_to_class(self, class_object):
    if class_object == None:
      return None
    self.class_id = class_object.id
    db.session.commit()
    return 1
  
  def __init__(self, board_parameter):
    self.author    = board_parameter['author']
    self.date      = board_parameter['date']
    self.board_str = board_parameter['board_str']
  
  def __repr__(self):
    return 'id:%s class_id:%s' %\
           (self.id, self.class_id)

class Status(db.Model):
  __table__name = 'status'
  id            = db.Column(db.Integer, primary_key=True)
  status        = db.Column(db.String(80))
  reason        = db.Column(db.String(80))
  student_id    = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
  
  def create_status(student_object, **options):
    if student_object == None:
      return None
    status_parm = dict(const_status_parameter)
    for arg in options.items():
      if arg[0] in const_status_parameter:
        status_parm[arg[0]] = arg[1]
    status = Status(student_object, status_parameter=status_parm)
    db.session.add(status)
    db.session.commit()
    return status
  
  def read_status_by_id(status_id):
    status = Status.query.filter_by(id=status_id)
    return status.first()
  
  def assign_to_student(self, student_object):
    if student_object == None:
      return None
    self.student_id = student_object.id
    return 1
  
  def __init__(self, student_object, status_parameter):
    self.date   = status_parameter['date']
    self.status = status_parameter['status']
    self.reason = status_parameter['reason']
    self.student_id = student_object.id
  
  def __repr__(self):
    return 'id:%s student_id:%s' %\
           (self.id, self.student_id)

class Learn(db.Model):
  __table__name = 'learn'
  id            = db.Column(db.Integer, primary_key=True)
  author        = db.Column(db.String(80))
  date          = db.Column(db.String(80))
  content       = db.Column(db.String(500))
  class_id      = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
  
  def create_learn(class_object, **options):
    if class_object == None:
      return None
    learn_parm = dict(const_learn_parameter)
    for arg in options.items():
      if arg[0] in const_learn_parameter:
        learn_parm[arg[0]] = arg[1]
    learn  = Learn(class_object, learn_parameter=learn_parm)
    learn.class_id = class_object.id
    db.session.add(learn)
    db.session.commit()
    return learn
  
  def read_learn_by_id(learn_id):
    learn = Learn.query.filter_by(id=learn_id)
    return learn.first()
  
  def __init__(self, class_object, learn_parameter):
    self.author    = learn_parameter['author']
    self.date      = learn_parameter['date']
    self.content   = learn_parameter['content']
    self.class_id  = class_object.id
  
  def __repr__(self):
    return 'id:%s class_id:%s' %\
           (self.id, self.class_id)

