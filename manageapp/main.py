from datetime import datetime
import math
import re
from functools import wraps

import cloudinary
import cloudinary.uploader

from flask import render_template, request, url_for
from flask_login import login_user, login_required
from jinja2 import TemplateNotFound
from werkzeug.utils import secure_filename

import utils
from manageapp import login
from manageapp.admin import *
from manageapp.forms import LoginForm, MarkCheck


def teacher_requirement(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        try:
            if current_user.user_role == UserRole.TEACHER or current_user.user_role == UserRole.ADMIN:
                return f(*args, **kwargs)
            else:
                return redirect(url_for('access_denied'))
        except:
            return redirect(url_for('access_denied'))

    return wrap


def staff_requirement(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        try:
            if current_user.user_role == UserRole.STAFF or current_user.user_role == UserRole.ADMIN:
                return f(*args, **kwargs)
            else:
                return redirect(url_for('access_denied'))
        except:
            return redirect(url_for('access_denied'))

    return wrap


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@login.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def user_login():
    if not current_user.is_authenticated:
        form = LoginForm(request.form)
        msg = None
        user = None
        password = None

        if form.validate_on_submit():
            username = request.form['username']
            password = request.form['password']

            password = utils.hash_password(password)
            user = User.query.filter(User.username.__eq__(username.strip())).first()

            if user:
                if password.__eq__(user.password):
                    login_user(user=user)
                    return redirect(url_for('index'))
                else:
                    msg = "Sai mật khẩu!!!"
            else:
                msg = "Không tồn tại username trong hệ thống!!!"
    else:
        return redirect('/')

    return render_template('accounts/login.html', form=form, msg=msg, user=user, password=password,
                           UserRole=UserRole)


@login.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id=user_id)


@app.route('/admin-login', methods=['post'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = utils.check_login(username=username, password=password)

    if user:
        login_user(user=user)

    return redirect('/admin')


# App main route + generic routing
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path>')
def index(path):
    staff_counter = utils.count_staff()
    teacher_counter = utils.count_teacher()
    student_counter = utils.count_student()

    if not current_user.is_authenticated:
        return redirect(url_for('user_login'))

    try:
        if not path.endswith('.html'):
            path += '.html'

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template('home/' + path, UserRole=UserRole,
                               staff_counter=staff_counter,
                               teacher_counter=teacher_counter,
                               student_counter=student_counter)

    except TemplateNotFound:
        return render_template('home/page-404.html', UserRole=UserRole), 404
    except:
        return render_template('home/page-500.html', UserRole=UserRole), 500


@app.route('/access-denied')
def access_denied():
    return render_template('home/page-403.html', UserRole=UserRole)


@app.route('/about-us')
@login_required
def about_us():
    return render_template('home/about-us.html', UserRole=UserRole)


@app.route('/tra-cuu-nhap-diem', methods=['GET', 'POST'])
@login_required
@teacher_requirement
def tra_cuu_nhap_diem():
    msg = None
    page = request.args.get('page', 1)
    counter = utils.count_student()
    students = utils.read_student_by_page(page=int(page))
    subjects = utils.get_all_subject()
    semesters = Semester.query.order_by(asc(Semester.id)).all()

    return render_template('home/tra-cuu-nhap-diem.html', UserRole=UserRole,
                           students=students,
                           subjects=subjects,
                           semesters=semesters,
                           page=math.ceil(counter / app.config['STUDENT_SIZE']),
                           current_page=int(page),
                           msg=msg
                           )


# CHUC NANG CUA GIAO VIEN
@app.route('/nhap-diem', methods=['GET', 'POST'])
@login_required
@teacher_requirement
def nhap_diem():
    msg = None
    page = request.args.get('page', 1)
    counter = utils.count_student()
    students = utils.read_student_by_page(page=int(page))
    subjects = utils.get_all_subject()
    semesters = Semester.query.order_by(asc(Semester.id)).all()

    student_id = request.args.get('student_id', 0)
    subject_id = request.args.get('subject_id', 0)
    semester_id = request.args.get('semester_id', 0)
    student = utils.get_student_by_id(student_id=student_id)
    subject = utils.get_subject_by_id(subject_id=subject_id)
    semester = utils.get_semester_by_id(semester_id=semester_id)
    mark = utils.get_mark_by_id(student_id=student_id, subject_id=subject_id, semester_id=semester_id)

    if request.method.__eq__('POST'):
        student_id = request.form.get('student_id', -1.0)
        subject_id = request.form.get('subject_id', -1.0)
        semester_id = request.form.get('semester_id', -1.0)

        student = utils.get_student_by_id(student_id=student_id)
        subject = utils.get_subject_by_id(subject_id=subject_id)
        semester = utils.get_semester_by_id(semester_id=semester_id)

        mark15_1 = request.form.get('mark15_1', -1)
        mark15_2 = request.form.get('mark15_2', -1)
        mark15_3 = request.form.get('mark15_3', -1)
        mark15_4 = request.form.get('mark15_4', -1)
        mark15_5 = request.form.get('mark15_5', -1)
        mark45_1 = request.form.get('mark45_1', -1)
        mark45_2 = request.form.get('mark45_2', -1)
        mark45_3 = request.form.get('mark45_3', -1)
        final = request.form.get('final', -1)

        mark15_1 = utils.normalize_float(mark15_1)
        mark15_2 = utils.normalize_float(mark15_2)
        mark15_3 = utils.normalize_float(mark15_3)
        mark15_4 = utils.normalize_float(mark15_4)
        mark15_5 = utils.normalize_float(mark15_5)
        mark45_1 = utils.normalize_float(mark45_1)
        mark45_2 = utils.normalize_float(mark45_2)
        mark45_3 = utils.normalize_float(mark45_3)
        final = utils.normalize_float(final)

        utils.update_mark(mark15_1=mark15_1,
                          mark15_2=mark15_2,
                          mark15_3=mark15_3,
                          mark15_4=mark15_4,
                          mark15_5=mark15_5,
                          mark45_1=mark45_1,
                          mark45_2=mark45_2,
                          mark45_3=mark45_3,
                          final=final,
                          student_id=student_id,
                          student=student,
                          subject_id=subject_id,
                          subject=subject,
                          semester_id=semester_id)

        return redirect(url_for('nhap_diem', student_id=student_id, subject_id=subject_id,
                                semester_id=semester_id))

    return render_template('home/nhap-diem.html', UserRole=UserRole,
                           students=students,
                           subjects=subjects,
                           semesters=semesters,
                           student=student,
                           subject=subject,
                           semester=semester,
                           page=math.ceil(counter / app.config['STUDENT_SIZE']),
                           current_page=int(page),
                           mark=mark,
                           msg=msg,
                           student_id=student_id,
                           subject_id=subject_id,
                           semester_id=semester_id
                           )


@app.route('/bang-diem-theo-lop', methods=['GET', 'POST'])
@login_required
@teacher_requirement
def xuat_diem_theo_lop():
    students = None
    classes = utils.get_all_class()
    semesters = Semester.query.order_by(asc(Semester.id)).all()
    subjects = utils.get_all_subject()
    mark = None
    msg = None
    class_id = None
    class_name = None
    semester_id = None
    subject_id = None
    school_year_name = None

    class_obj = None
    semester = None
    subject = None

    hs1 = None
    hs2 = None

    if request.method.__eq__('POST'):
        class_name = request.form.get('class_name')
        semester_id = request.form.get('semester_id', 0)
        subject_id = request.form.get('subject_id', 0)

        class_id = utils.get_class_id_by_name(class_name=class_name)
        if class_id:
            class_obj = utils.get_class_by_id(class_id=class_id)

            semester = utils.get_semester_by_id(semester_id)
            if semester:
                subject = utils.get_subject_by_id(subject_id)
                if subject:
                    school_year_name = utils.get_school_year_by_semester_id(semester_id=semester_id)
                    students = utils.get_all_student_in_class(class_id=class_obj.id)
                    mark = utils.get_mark_by_subject_and_class(semester_id=semester_id,
                                                               subject_id=subject_id,
                                                               class_id=class_id)
                else:
                    msg = 'Mã môn không tồn tại'
            else:
                msg = 'Mã kì học không tồn tại'
        else:
            msg = 'Lớp không tồn tại'

    return render_template('home/xuat-diem-mon-theo-lop.html', UserRole=UserRole,
                           class_name=class_name,
                           semester_id=semester_id,
                           subject_id=subject_id,
                           classes=classes,
                           class_id=class_id,
                           class_obj=class_obj,
                           semesters=semesters,
                           subjects=subjects,
                           students=students,
                           subject=subject,
                           mark=mark,
                           hs1=hs1,
                           hs2=hs2,
                           semester=semester,
                           school_year_name=school_year_name,
                           msg=msg
                           )


@app.route('/bang-diem-trung-binh-lop', methods=['GET', 'POST'])
@login_required
@teacher_requirement
def bang_diem_trung_binh_lop():
    students = None
    classes = utils.get_all_class()
    subjects = utils.get_all_subject()
    label_school_year_name = utils.get_all_school_year_name()
    class_name = None
    msg = None
    mark_sem1 = None
    mark_sem2 = None
    school_year_name = None
    subject_id = None
    subject_name = None

    if request.method.__eq__('POST'):
        school_year_name = request.form.get('school_year_name')
        class_name = request.form.get('class_name')

        school_year_name = utils.remove_all_character(school_year_name=school_year_name)

        exist_school_year = utils.get_school_year_by_name(school_year_name=school_year_name)
        if exist_school_year:
            class_obj = utils.get_class_by_name(class_name=class_name)
            if class_obj:
                students = utils.get_all_student_in_class(class_id=class_obj.id)

                mark_sem1 = utils.get_mark_avg_all_subject_by_all_student(school_year_name=school_year_name,
                                                                          class_id=class_obj.id,
                                                                          semester_no=1)

                mark_sem2 = utils.get_mark_avg_all_subject_by_all_student(school_year_name=school_year_name,
                                                                          class_id=class_obj.id,
                                                                          semester_no=2)
            else:
                msg = 'ID môn học không tồn tại'
        else:
            msg = 'Không tồn tại năm học'

    return render_template('home/bang-diem-trung-binh-lop.html', UserRole=UserRole,
                           msg=msg,
                           classes=classes,
                           students=students,
                           subjects=subjects,
                           label_school_year_name=label_school_year_name,
                           school_year_name=school_year_name,
                           class_name=class_name,
                           mark_sem1=mark_sem1,
                           mark_sem2=mark_sem2,
                           subject_id=subject_id,
                           subject_name=subject_name,
                           start_count=1
                           )


# CHUC NANG DANH CHO NHAN VIEN
@app.route('/dieu-chinh-lop', methods=['GET', 'POST'])
@login_required
@staff_requirement
def dieu_chinh_lop():
    success_msg = None
    warning_msg = None

    page = request.args.get('page', 1)
    counter = utils.count_student()
    students = utils.read_student_by_page(page=int(page))
    classes = utils.get_all_class()
    student_id = None
    student_name = None
    class_name = None

    if request.method.__eq__('POST'):
        student_id = request.form.get('student_id')
        class_name = request.form.get('class_name')

        class_obj = utils.get_class_by_name(class_name)
        student = utils.get_student_by_id(student_id)

        if student:
            student_name = student.fullname
            if class_obj:
                valid = utils.valid_add_student_to_class(class_obj.id)
                if valid:
                    utils.update_class_for_student(student_id=student_id,
                                                   class_id=class_obj.id)
                    success_msg = "Cập nhật thành công lớp mới cho học sinh: {student_name}".format(
                        student_name=student_name)
                else:
                    warning_msg = "Lớp {class_name} đã đạt sĩ số tối đa".format(class_name=class_name)

            else:
                warning_msg = "Không tồn tại lớp có tên: {class_name}".format(class_name=class_name)
        else:
            warning_msg = "Không tồn tại học sinh có id = {student_id}".format(student_id=student_id)

    return render_template('home/dieu-chinh-lop.html', UserRole=UserRole, students=students,
                           classes=classes,
                           current_page=int(page),
                           page=math.ceil(counter / app.config['STUDENT_SIZE']),
                           warning_msg=warning_msg,
                           success_msg=success_msg,
                           student_id=student_id,
                           student_name=student_name,
                           class_name=class_name
                           )


@app.route('/tiep-nhan', methods=['GET', 'POST'])
@login_required
@staff_requirement
def tiep_nhan():
    page = request.args.get('page', 1)
    counter = utils.count_student()
    students = utils.read_student_by_page(page=int(page))

    success_msg = None
    warning_msg = None
    fullname = None
    email = None
    phone = None
    address = None
    dob_day = None
    dob_month = None
    dob_year = None
    requirement_obj = utils.get_newest_requirement()
    max_age_student = requirement_obj.max_age_student
    min_age_student = requirement_obj.min_age_student

    if request.method.__eq__('POST'):
        fullname = request.form.get('fullname')
        gender = request.form.get('gender')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        dob_day = request.form.get('dob_day')
        dob_month = request.form.get('dob_month')
        dob_year = request.form.get('dob_year')
        dob = "{year}-{month}-{day}".format(year=dob_year,
                                            month=dob_month,
                                            day=dob_day)

        check_email = utils.exist_email_student(email=email)
        if check_email:
            check_dob = utils.valid_dob(dob=dob)
            if check_dob:
                utils.add_student(fullname=fullname, email=email, gender=bool(int(gender)),
                                  phone=phone, address=address, dob=dob)
                counter = utils.count_student()
                students = utils.read_student_by_page(page=int(page))
                success_msg = 'Tiếp nhận thành công học sinh'
                fullname = None
                email = None
                phone = None
                address = None
                dob_day = None
                dob_month = None
                dob_year = None
            else:
                warning_msg = "Độ tuổi của học sinh nằm trong khoảng từ {min} đến {max}. " \
                              "Hoặc ngày nhập vào không hợp lệ!!!" \
                              " Vui lòng kiểm tra lại ngày sinh" \
                    .format(min=min_age_student, max=max_age_student)
        else:
            warning_msg = 'Email đã tồn tại'

    return render_template('home/tiep-nhan.html', UserRole=UserRole,
                           current_page=int(page),
                           page=math.ceil(counter / app.config['STUDENT_SIZE']),
                           students=students,
                           success_msg=success_msg,
                           warning_msg=warning_msg,
                           fullname=fullname,
                           email=email,
                           phone=phone,
                           address=address,
                           dob_day=dob_day,
                           dob_month=dob_month,
                           dob_year=dob_year
                           )


@app.route('/xuat-danh-sach-lop', methods=['GET', 'POST'])
@login_required
@staff_requirement
def xuat_danh_sach_lop():
    msg = None
    students = None
    class_confirm = None
    class_id = None
    class_name = None
    classes = utils.get_all_class()
    student_counter = 0

    if request.method.__eq__('POST'):
        class_name = request.form.get('class_name')

        class_id = utils.get_class_id_by_name(class_name=class_name)

        if class_id:
            student_counter = utils.count_student_in_class(class_id=class_id)
            class_confirm = utils.get_class_by_id(class_id=class_id)
            if class_confirm:
                students = utils.get_all_student_in_class(class_id)
                if not students:
                    msg = 'Lớp này hiện chưa có học sinh'
            else:
                msg = 'Tên lớp học không tồn tại'
        else:
            msg = 'Không tồn tại lớp này'

    return render_template('home/xuat-danh-sach-lop.html', UserRole=UserRole, msg=msg,
                           classes=classes,
                           class_id=class_id,
                           class_name=class_name,
                           class_confirm=class_confirm,
                           students=students,
                           student_counter=student_counter
                           )


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    msg = None
    avatar = None
    current_dob = datetime.strptime(str(current_user.dob), '%Y-%m-%d')
    dob_day = current_dob.day
    dob_month = current_dob.month
    dob_year = current_dob.year

    if request.method.__eq__('POST'):
        user_id = request.form.get('id')
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        pwd = request.form.get('password')
        dob_day = request.form.get('dob_day')
        dob_month = request.form.get('dob_month')
        dob_year = request.form.get('dob_year')
        dob = "{year}-{month}-{day}".format(year=dob_year,
                                            month=dob_month,
                                            day=dob_day)

        password_new_user = utils.get_password_user_by_id(user_id=user_id)
        if str(password_new_user).__eq__(utils.hash_password(pwd)):
            avatar = request.files.get('avatar')
            if avatar:
                res = cloudinary.uploader.upload(avatar)
                avatar_path = res['secure_url']

                utils.update_user_info(user_id=user_id,
                                       fullname=fullname,
                                       email=email,
                                       phone=phone,
                                       address=address,
                                       dob=dob,
                                       avatar=avatar_path
                                       )
            else:
                utils.update_user_info(user_id=user_id,
                                       fullname=fullname,
                                       email=email,
                                       phone=phone,
                                       address=address,
                                       dob=dob
                                       )
        else:
            msg = 'Mật khẩu không chính xác'

    return render_template('home/profile.html', UserRole=UserRole,
                           msg=msg,
                           avatar=avatar,
                           dob_day=dob_day,
                           dob_month=dob_month,
                           dob_year=dob_year
                           )


@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    warning_msg = None
    success_msg = None

    if request.method.__eq__('POST'):
        user_id = request.form.get('id')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        check_current_password = utils.get_password_user_by_id(user_id=user_id)
        if str(check_current_password).__eq__(utils.hash_password(current_password)):
            if new_password.__eq__(confirm_password):
                utils.update_password(user_id=user_id, new_password=new_password)
                success_msg = 'Thay đổi mật khẩu thành công'
            else:
                warning_msg = "Mật khẩu mới không khớp"
        else:
            warning_msg = 'Mật khẩu hiện tại không chính xác'

    return render_template('home/change-password.html', UserRole=UserRole,
                           warning_msg=warning_msg,
                           success_msg=success_msg
                           )


if __name__ == '__main__':
    app.run(debug=True)
