import hashlib
import json
import os.path
from datetime import date
from sqlalchemy import update, asc, text, desc

from flask_admin.model import typefmt

from sqlalchemy import and_
from manageapp import app, db
from manageapp.models import *
from manageapp.models import Semester, Student, Mark, User, Class, UserRole, Subject, Requirement


def get_last_word(string):
    if string:
        my_str = string
        word_list = my_str.split()
        return word_list[-1]


def get_newest_requirement():
    requirement = Requirement.query.order_by(Requirement.id.desc()).first()
    if requirement:
        return requirement


def valid_dob(dob):
    try:
        date_time_dob_obj = datetime.strptime(dob, '%Y-%m-%d')
    except ValueError:
        return False

    date_time_now_dob_obj = datetime.now()

    duration = (date_time_now_dob_obj - date_time_dob_obj).days
    age = duration / 365

    requirement = get_newest_requirement()
    max_age_student = requirement.max_age_student
    min_age_student = requirement.min_age_student

    if min_age_student <= int(age) <= max_age_student:
        return True
    else:
        return False


def exist_email_student(email):
    student = Student.query.filter(Student.email.__eq__(email)).count()
    if student == 0:
        return True
    else:
        return False


def get_user_by_id(user_id):
    user = User.query.filter(User.id.__eq__(user_id)).first()
    if user:
        return user


def get_password_user_by_id(user_id):
    user = User.query.filter(User.id.__eq__(user_id)).first()
    if user:
        return user.password


def check_login(username, password):
    if username and password:
        password = hash_password(password)

    return User.query.filter(and_(User.username.__eq__(username.strip())),
                             User.password.__eq__(password.strip())).first()


def add_student(fullname, gender, email, phone, address, dob):
    try:
        student = Student(fullname=fullname,
                          gender=gender,
                          email=email,
                          phone=phone,
                          address=address,
                          dob=dob)
        db.session.add(student)
        db.session.commit()
    except:
        db.session.rollback()
        raise


def date_format(view, value):
    return value.strftime('%d/%m/%Y')


def remove_all_character(school_year_name):
    if school_year_name:
        new_string = school_year_name
        new_string = new_string.translate({ord(i): None for i in 'abcdefghijklmnopqrstuvwxyz'})
        new_string = new_string.translate({ord(i): None for i in '!@#$%^&*()_=+{}|><.,?/'})
        return new_string


MY_DEFAULT_FORMATTERS = dict(typefmt.BASE_FORMATTERS)
MY_DEFAULT_FORMATTERS.update({
    type(None): typefmt.null_formatter,
    date: date_format
})


def hash_password(password):
    return hashlib.md5(password.strip().encode('utf-8')).hexdigest()


def update_user_info(user_id, fullname, email, phone, address, dob, **kwargs):
    user = User.query.filter(User.id.__eq__(user_id)).first()
    user.fullname = fullname
    user.email = email
    user.phone = phone
    user.address = address
    user.dob = dob
    if kwargs.get('avatar'):
        user.avatar = kwargs.get('avatar')
    db.session.commit()


def update_password(user_id, new_password):
    user = User.query.filter(User.id.__eq__(user_id)).first()
    password = hash_password(new_password)
    user.password = password
    db.session.commit()


def get_all_student():
    students = Student.query.filter().all()
    if students:
        students.sort(key=lambda x: get_last_word(x.fullname.lower()))
        return students


def read_student_by_page(page):
    student_size = app.config['STUDENT_SIZE']
    start = (page - 1) * student_size
    end = start + student_size

    if page:
        students = get_all_student()
        return students[start:end]


def count_student():
    return Student.query.filter().count()


def count_subject():
    return Subject.query.filter().count()


def count_staff():
    return User.query.filter(User.user_role == UserRole.STAFF).count()


def count_teacher():
    return User.query.filter(User.user_role == UserRole.TEACHER).count()


def get_class_id_by_name(class_name):
    result = Class.query.filter(Class.name == class_name).first()
    if result:
        return result.id


def get_class_by_id(class_id):
    result = Class.query.filter(Class.id == class_id).first()
    if result:
        return result


def get_class_by_name(class_name):
    result = Class.query.filter(Class.name.__eq__(class_name)).first()
    if result:
        return result


def update_class_for_student(student_id, class_id):
    student = Student.query.filter(Student.id.__eq__(student_id)).first()
    old_class_id = student.class_id

    if old_class_id != class_id:
        old_class = Class.query.filter(Class.id.__eq__(old_class_id)).first()
        if old_class:
            old_class.class_size = int(count_student_in_class(class_id=old_class_id)) - 1

        new_class = Class.query.filter(Class.id.__eq__(class_id)).first()
        new_class.class_size = int(count_student_in_class(class_id=class_id)) + 1

        student.class_id = class_id

        db.session.commit()


def get_student_by_id(student_id):
    student_id = str(student_id).lower().strip()
    student = Student.query.filter(Student.id.__eq__(student_id)).first()
    if student:
        return student


def get_subject_by_id(subject_id):
    subject_id = str(subject_id).lower().strip()
    subject = Subject.query.filter(Subject.subject_id.__eq__(subject_id)).first()
    if subject:
        return subject


def get_semester_by_id(semester_id):
    semester_id = str(semester_id).lower().strip()
    semester = Semester.query.filter(Semester.id.__eq__(semester_id)).first()
    if semester:
        return semester


def get_all_school_year_name():
    label = []
    semesters = Semester.query.order_by(desc(Semester.school_year_name)).all()
    for s in semesters:
        label.append(s.school_year_name)

    label = set(label)
    if label:
        return label


def get_subject_by_name(subject_name):
    subject_name = str(subject_name).lower().strip()
    subject = Subject.query.filter(Subject.name.__eq__(subject_name)).first()
    if subject:
        return subject


def get_subject_id_by_name(subject_name):
    subject_name = str(subject_name).lower().strip()
    subject = Subject.query.get(Subject.name.__eq__(subject_name)).first()
    if subject:
        return subject.subject_id


def get_mark_by_id(student_id, subject_id, semester_id):
    return Mark.query.filter(Mark.student_id.__eq__(student_id),
                             Mark.subject_id.__eq__(subject_id),
                             Mark.semester_id.__eq__(semester_id)).first()


def normalize_float(float_number):
    return float(float_number) if float_number else -1


def calcAVG(hs1, hs2, final):
    sum_hs1 = 0
    count_hs1 = 0
    sum_hs2 = 0
    count_hs2 = 0
    count_hs3 = 3

    for mark1 in hs1:
        if mark1 >= 0:
            sum_hs1 = sum_hs1 + float(mark1)
            count_hs1 = count_hs1 + 1

    for mark2 in hs2:
        if mark2 >= 0:
            sum_hs2 = sum_hs2 + float(mark2) * 2
            count_hs2 = count_hs2 + 2

    if count_hs1 == 0:
        count_hs1 = 1

    if count_hs2 == 0:
        count_hs2 = 2

    return float(sum_hs1 + sum_hs2 + float(final) * count_hs3) / (count_hs1 + count_hs2 + count_hs3)


def update_mark(mark15_1, mark15_2, mark15_3, mark15_4, mark15_5,
                mark45_1, mark45_2, mark45_3, final,
                student_id, student, subject_id, subject, semester_id):
    mark = get_mark_by_id(student_id=student_id, subject_id=subject_id, semester_id=semester_id)
    hs1 = ([mark15_1, mark15_2, mark15_3, mark15_4, mark15_5])
    hs2 = ([mark45_1, mark45_2, mark45_3])

    if mark:
        mark.mark15_1 = mark15_1 if mark15_1 >= 0 else -1
        mark.mark15_2 = mark15_2 if mark15_2 >= 0 else -1
        mark.mark15_3 = mark15_3 if mark15_3 >= 0 else -1
        mark.mark15_4 = mark15_4 if mark15_4 >= 0 else -1
        mark.mark15_5 = mark15_5 if mark15_5 >= 0 else -1
        mark.mark45_1 = mark45_1 if mark45_1 >= 0 else -1
        mark.mark45_2 = mark45_2 if mark45_2 >= 0 else -1
        mark.mark45_3 = mark45_3 if mark45_3 >= 0 else -1
        mark.final = final if final >= 0 else -1

        mark.avg = calcAVG(hs1=hs1, hs2=hs2, final=final)

        db.session.commit()
    else:
        mark = Mark(student_id=student_id, student=student,
                    subject_id=subject_id, subject=subject,
                    semester_id=semester_id)
        mark.mark15_1 = mark15_1 if mark15_1 >= 0 else -1
        mark.mark15_2 = mark15_2 if mark15_2 >= 0 else -1
        mark.mark15_3 = mark15_3 if mark15_3 >= 0 else -1
        mark.mark15_4 = mark15_4 if mark15_4 >= 0 else -1
        mark.mark15_5 = mark15_5 if mark15_5 >= 0 else -1
        mark.mark45_1 = mark45_1 if mark45_1 >= 0 else -1
        mark.mark45_2 = mark45_2 if mark45_2 >= 0 else -1
        mark.mark45_3 = mark45_3 if mark45_3 >= 0 else -1
        mark.final = final if final >= 0 else -1

        mark.avg = calcAVG(hs1=hs1, hs2=hs2, final=final)

        db.session.add(mark)
        db.session.commit()


def create_mark(mark15_1, mark15_2, mark15_3, mark15_4, mark15_5,
                mark45_1, mark45_2, mark45_3, final,
                student_id, subject_id, semester_id):
    hs1 = ([mark15_1, mark15_2, mark15_3, mark15_4, mark15_5])
    hs2 = ([mark45_1, mark45_2, mark45_3])

    mark15_1 = mark15_1 if mark15_1 >= 0 else -1
    mark15_2 = mark15_2 if mark15_2 >= 0 else -1
    mark15_3 = mark15_3 if mark15_3 >= 0 else -1
    mark15_4 = mark15_4 if mark15_4 >= 0 else -1
    mark15_5 = mark15_5 if mark15_5 >= 0 else -1
    mark45_1 = mark45_1 if mark45_1 >= 0 else -1
    mark45_2 = mark45_2 if mark45_2 >= 0 else -1
    mark45_3 = mark45_3 if mark45_3 >= 0 else -1
    final = final if final >= 0 else -1

    avg = calcAVG(hs1=hs1, hs2=hs2, final=final)

    mark = Mark(subject_id=subject_id, student_id=student_id, semester_id=semester_id,
                mark15_1=mark15_1, mark15_2=mark15_2, mark15_3=mark15_3, mark15_4=mark15_4,
                mark15_5=mark15_5, mark45_1=mark45_1, mark45_2=mark45_2, mark45_3=mark45_3,
                final=final, avg=avg)

    db.session.add(mark)
    db.session.commit()


def get_all_class():
    class_all = Class.query.order_by(asc(Class.name)).all()
    if class_all:
        return class_all


def get_all_subject():
    subjects = Subject.query.order_by(asc(Subject.subject_id)).all()
    if subjects:
        return subjects


def get_school_year_by_semester_id(semester_id):
    semester = Semester.query.filter(Semester.id.__eq__(semester_id)).first()
    if semester:
        return semester.school_year_name


def get_school_year_by_name(school_year_name):
    school_year_name = str(school_year_name).strip().lower()
    semester = Semester.query.filter(Semester.school_year_name.__eq__(school_year_name)).first()
    if semester:
        return semester


def get_label_class_name(mark_sem):
    labels = []
    for m in mark_sem:
        class_obj = get_class_by_id(m.student.class_id)
        labels.append(class_obj.name)

    if labels:
        return labels


def get_mark_avg_all_subject_by_all_student(school_year_name, class_id, semester_no):
    students = get_all_student_in_class(class_id=class_id)
    semester = Semester.query.filter(and_(Semester.school_year_name.__eq__(school_year_name),
                                          Semester.semester_name.__eq__(semester_no))).first()
    mark_all = []
    if students:
        for student in students:
            mark_all.append(get_mark_avg_all_subject(student_id=student.id,
                                                     semester_id=semester.id
                                                     ))

    if mark_all:
        return mark_all


def get_mark_avg_all_subject(student_id, semester_id):
    mark = []
    counter = 0
    marks = Mark.query.filter(and_(Mark.student_id.__eq__(student_id),
                                   Mark.semester_id.__eq__(semester_id))).all()
    for m in marks:
        counter = counter + 1
        if m.avg >= 0:
            mark.append(m.avg)
        else:
            mark.append(0)

    if len(mark) != 0:
        return sum(mark) / count_subject()
    else:
        return 0


def get_class_id_by_student_id(student_id):
    student = Student.query.filter(Student.id == student_id).first()
    if student:
        return student.class_id


def get_mark_by_subject_and_class(semester_id, subject_id, class_id):
    mark_list = []
    students = get_all_student_in_class(class_id=class_id)
    if students:
        for s in students:
            mark_result = Mark.query.filter(and_(Mark.semester_id.__eq__(semester_id),
                                                 Mark.student_id == s.id,
                                                 Mark.subject_id.__eq__(subject_id))).first()
            if mark_result:
                mark_list.append(mark_result)
            else:
                mark_list.append(None)

    return mark_list


def avg_mark(mark_list, hs):
    sum_list = 0
    count = 0

    for mark in mark_list:
        if mark >= 0:
            sum_list = sum_list + float(mark) * hs
            count = count + hs

    if count == 0:
        return 0
    else:
        return sum_list / count


def get_all_student_in_class(class_id):
    students = Student.query.filter(Student.class_id.__eq__(class_id)).all()
    if students:
        students.sort(key=lambda x: get_last_word(x.fullname.lower()))
        return students


def count_student_in_class(class_id):
    students = Student.query.filter(Student.class_id.__eq__(class_id)).count()
    if students:
        return students
    else:
        return 0


def valid_add_student_to_class(class_id):
    requirement = get_newest_requirement()
    class_obj = Class.query.filter(Class.id.__eq__(class_id)).first()
    if class_obj.class_size < requirement.max_class_size:
        return True
    else:
        return False


# ========================== STATS ========================== #
def stats(subject_id, semester_id):
    classes = Class.query.order_by(asc(Class.name)).all()
    array_count = []

    if classes:
        for cl in classes:
            mark = get_mark_by_subject_and_class(class_id=cl.id,
                                                 subject_id=subject_id,
                                                 semester_id=semester_id)
            count = 0
            if mark:
                for m in mark:
                    if m:
                        if m.avg >= 5.0:
                            count = count + 1
                array_count.append(count)

    return array_count
