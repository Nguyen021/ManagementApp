from sqlalchemy import Column, Integer, String, Boolean, \
    DateTime, ForeignKey, Date, Float, Enum, func
from sqlalchemy.orm import relationship, backref
from manageapp import db
from datetime import datetime
from flask_login import UserMixin
from enum import Enum as UserEnum
from utils import *


class UserRole(UserEnum):
    NONE = 0
    ADMIN = 1
    STAFF = 2
    TEACHER = 3

    def __str__(self):
        if str(self.name).__eq__('STAFF'):
            return 'NHÂN VIÊN'
        elif str(self.name).__eq__('TEACHER'):
            return 'GIÁO VIÊN'

        return self.name


class People(db.Model):
    __abstract__ = True

    fullname = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    phone = Column(String(15), nullable=False, unique=True)
    address = Column(String(50), nullable=False)
    dob = Column(Date)
    gender = Column(Boolean, nullable=False)


class User(People, UserMixin):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(150),
                    default='https://res.cloudinary.com/dxorabap0/image/upload/v1642074622/tb-avatar-none_r1c2ye.jpg')
    joined_date = Column(DateTime, default=datetime.now())
    status = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.NONE)

    def __str__(self):
        return self.username


class Student(People):
    __tablename__ = 'student'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)

    class_id = Column(Integer, ForeignKey('class.id'))

    def __str__(self):
        return "[{id}]. {name}".format(id=self.id, name=self.fullname)

    def __repr__(self):
        return self.fullname


class Grade(db.Model):
    __tablename__ = 'grade'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(Integer)

    classes = relationship('Class', backref='grade', lazy=True)

    def __str__(self):
        return str(self.number)


class Class(db.Model):
    __tablename__ = 'class'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10), nullable=False, unique=True)
    class_size = Column(Integer, nullable=False, default=0)

    students = relationship('Student', backref='class', lazy=True)
    grade_id = Column(Integer, ForeignKey('grade.id'), nullable=False)

    def __str__(self):
        return self.name


class Subject(db.Model):
    __tablename__ = 'subject'
    __table_args__ = {'extend_existing': True}

    subject_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

    def __str__(self):
        return self.name


class Mark(db.Model):
    __tablename__ = 'mark'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    mark15_1 = Column(Float)
    mark15_2 = Column(Float)
    mark15_3 = Column(Float)
    mark15_4 = Column(Float)
    mark15_5 = Column(Float)
    mark45_1 = Column(Float)
    mark45_2 = Column(Float)
    mark45_3 = Column(Float)
    final = Column(Float)
    avg = Column(Float)

    subject_id = Column(Integer, ForeignKey('subject.subject_id'), nullable=False)
    subject = relationship('Subject', foreign_keys=[subject_id])
    student_id = Column(Integer, ForeignKey('student.id'), nullable=False)
    student = relationship('Student', foreign_keys=[student_id])

    semester_id = Column(Integer, ForeignKey('semester.id'), nullable=False)

    def __str__(self):
        return "{student} - {subject} - {semester}".format(student=self.student.fullname,
                                                           subject=self.subject.name,
                                                           semester=self.semester_id)


class Semester(db.Model):
    __tablename__ = 'semester'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    semester_name = Column(String(15), nullable=False)
    school_year_name = Column(String(15), nullable=False)

    marks = relationship('Mark', backref='semester', lazy=True)

    def __str__(self):
        return "HK{semester} - {school_year_name}".format(semester=self.semester_name,
                                                          school_year_name=self.school_year_name)


class Requirement(db.Model):
    __tablename__ = 'requirement'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    min_age_student = Column(Integer)
    max_age_student = Column(Integer)
    max_class_size = Column(Integer)


if __name__ == '__main__':
    db.create_all()
