import hashlib
from datetime import date
from manageapp import admin, db
from flask_admin.contrib.sqla import ModelView
from manageapp.models import User, Student, \
    Grade, Class, Subject, UserRole, Semester, Mark, Requirement
from flask_admin import BaseView, expose
from flask_login import logout_user, current_user
from flask import redirect, request, url_for
from wtforms import validators
from manageapp import utils
from utils import *


class AuthenticatedModelView(ModelView):
    column_display_pk = True
    can_view_details = True
    edit_modal = True
    details_modal = True
    can_export = True
    column_type_formatters = MY_DEFAULT_FORMATTERS

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()

        return redirect('/login')

    def is_accessible(self):
        return current_user.is_authenticated


class HomeView(BaseView):
    @expose('/')
    def __index__(self):
        return redirect(url_for('index'))


class StatsView(BaseView):
    @expose('/')
    def __index__(self):
        classes = Class.query.order_by(asc(Class.name)).all()
        subjects = Subject.query.order_by(asc(Subject.subject_id)).all()
        semesters = Semester.query.order_by(asc(Semester.id)).all()

        subject_id = request.args.get('subject_id')
        subject = utils.get_subject_by_id(subject_id=subject_id)

        semester_id = request.args.get('semester_id')
        semester = utils.get_semester_by_id(semester_id=semester_id)

        stats_table = utils.stats(subject_id=subject_id, semester_id=semester_id)

        return self.render('admin/stats.html',
                           sub_id=subject_id,
                           subject=subject,
                           semester_id=semester_id,
                           semester=semester,
                           stats_table=stats_table,
                           classes=classes,
                           subjects=subjects,
                           semesters=semesters
                           )

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class UserView(AuthenticatedModelView):
    column_filters = ['username', 'status', 'joined_date']
    column_list = ['username', 'fullname', 'gender', 'email', 'phone',  'dob', 'user_role']
    column_labels = {
        'fullname': 'H??? v?? t??n',
        'gender': 'Gi???i t??nh',
        'phone': 'S??? ??i???n tho???i',
        'address': '?????a ch???',
        'dob': 'Ng??y sinh',
        'id': 'M?? t??i kho???n',
        'username': 'T??n ????ng nh???p',
        'password': 'M???t kh???u',
        'avatar': '???????ng d???n ???nh ?????i di???n',
        'status': 'Tr???ng th??i',
        'user_role': 'Quy???n'
    }
    form_excluded_columns = ['status', 'joined_date', 'avatar']
    column_default_sort = 'fullname'

    def on_model_change(self, form, model, is_created):
        account = User.query.filter(User.username.__eq__(form.username.data)).first()
        account.password = utils.hash_password(form.password.data)
        db.session.commit()

        if date.today().__le__(form.dob.data):
            raise validators.ValidationError('Ng??y sinh kh??ng h???p l???!')


class StudentView(AuthenticatedModelView):
    column_filters = ['fullname', 'email', 'dob']
    column_editable_list = ['fullname']
    column_export_list = ['students']
    column_labels = {
        'id': 'M?? s???',
        'fullname': 'H??? v?? t??n',
        'gender': 'Gi???i t??nh',
        'phone': 'S??? ??i???n tho???i',
        'address': '?????a ch???',
        'dob': 'Ng??y sinh',
        'class': 'H???c l???p'
    }
    column_list = ['id', 'fullname', 'gender', 'email', 'phone',
                   'address', 'dob', 'class']
    column_display_all_relations = True


class GradeView(AuthenticatedModelView):
    column_filters = ['number']
    column_labels = {
        'id': 'M?? kh???i',
        'number': 'Kh???i',
        'classes': 'L???p thu???c kh???i'
    }
    column_list = ['id', 'number', 'classes']
    column_display_all_relations = True
    column_default_sort = 'number'
    form_columns = ['number', 'classes']


class ClassView(AuthenticatedModelView):
    edit_modal = False
    column_filters = ['name', 'class_size', 'grade']
    column_default_sort = 'name'
    column_labels = {
        'id': 'M?? L???p',
        'name': 'T??n L???p',
        'class_size': 'S?? s???',
        'grade': 'Kh???i L???p',
        'students': 'H???c sinh thu???c l???p'
    }
    column_list = ['name', 'class_size', 'grade',
                   'students']
    column_display_all_relations = True
    form_columns = ['name', 'grade', 'students']


class SubjectsView(AuthenticatedModelView):
    column_display_pk = False
    column_filters = ['name', 'subject_id']
    column_exclude_list = ['mark']
    column_default_sort = 'name'
    column_labels = {
        'subject_id': 'M?? m??n',
        'name': 'T??n m??n h???c'
    }
    column_display_all_relations = True
    form_columns = ['name']


class SchoolYearView(AuthenticatedModelView):
    column_filters = ['id', 'name']
    column_labels = {
        'id': 'ID',
        'name': 'Ni??n kho??',
        'semesters': 'H???c k??'
    }
    form_columns = ['name', 'semesters']


class SemesterView(AuthenticatedModelView):
    column_filters = ['id', 'semester_name']
    column_labels = {
        'id': 'ID',
        'semester_name': 'H???c k??',
        'school_year_name': 'N??m h???c'
    }
    form_excluded_columns = ['marks']


class MarkView(AuthenticatedModelView):
    column_display_all_relations = True
    column_display_pk = False
    column_default_sort = 'semester_id'
    column_filters = ['avg', 'semester', 'subject']
    column_list = ['id', 'semester', 'subject', 'student', 'mark15_1', 'mark15_2', 'mark15_3',
                   'mark15_4', 'mark15_5', 'mark45_1', 'mark45_2', 'mark45_3', 'final', 'avg']
    column_labels = {
        'semester': 'H???c k??',
        'subject': 'M??n',
        'student': 'H???c sinh',
        'mark15_1': '15p l???n 1',
        'mark15_2': '15p l???n 2',
        'mark15_3': '15p l???n 3',
        'mark15_4': '15p l???n 4',
        'mark15_5': '15p l???n 5',
        'mark45_1': '1 ti???t l???n 1',
        'mark45_2': '1 ti???t l???n 2',
        'mark45_3': '1 ti???t l???n 3',
        'final': 'Cu???i k??',
        'avg': '??TB'
    }
    form_excluded_columns = ['avg']
    form_columns = ['semester', 'subject', 'student', 'mark15_1', 'mark15_2',
                    'mark15_3', 'mark15_4', 'mark15_5', 'mark45_1', 'mark45_2', 'mark45_3', 'final']


class RequirementView(AuthenticatedModelView):
    column_display_all_relations = True
    column_display_pk = True
    column_default_sort = 'id'
    column_filters = ['min_age_student', 'max_age_student', 'max_class_size']
    column_labels = {
        'min_age_student': 'Tu???i t???i thi???u c???a h???c sinh',
        'max_age_student': 'Tu???i t???i ??a c???a h???c sinh',
        'max_class_size': 'S?? s??? t???i ??a',
    }
    form_excluded_columns = []
    form_columns = []


admin.add_view(UserView(User, db.session, name='T??i kho???n'))
admin.add_view(StudentView(Student, db.session, name='H???c sinh'))
admin.add_view(GradeView(Grade, db.session, name='Kh???i'))
admin.add_view(ClassView(Class, db.session, name='L???p'))
admin.add_view(SubjectsView(Subject, db.session, name='M??n h???c'))
admin.add_view(MarkView(Mark, db.session, name='??i???m thi'))
admin.add_view(SemesterView(Semester, db.session, name='H???c k??'))
admin.add_view(RequirementView(Requirement, db.session, name='Quy ?????nh'))
admin.add_view(StatsView(name='Th???ng k??'))
admin.add_view(HomeView(name='Trang ch??nh'))
admin.add_view(LogoutView(name='????ng xu???t'))
