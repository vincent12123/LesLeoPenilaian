from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import logging
from sqlalchemy.exc import IntegrityError
import os

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student_grades.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = os.environ.get('SECRET_KEY', 'your_fallback_secret_key_here')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
db = SQLAlchemy(app)

# Student Model
class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    student_number = db.Column(db.Integer, unique=True, nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    grades = db.relationship('Grade', backref='student', lazy=True)

class Class(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(50), nullable=False, unique=True)
    students = db.relationship('Student', backref='class', lazy=True)
    assignments = db.relationship('Assignment', backref='class_', lazy=True)  # Use 'class_' to avoid conflict with reserved keyword

class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(100), nullable=False, unique=True)
    assignments = db.relationship('Assignment', backref='subject', lazy=True)

class Assignment(db.Model):
    __tablename__ = 'assignments'
    id = db.Column(db.Integer, primary_key=True)
    assignment_name = db.Column(db.String(100), nullable=False)
    date_assigned = db.Column(db.Date, nullable=False, default=date.today)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    grades = db.relationship('Grade', backref='assignment', lazy=True)
    
class Grade(db.Model):
    __tablename__ = 'grades'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)

# Initialize the database
with app.app_context():
    db.create_all()

# Initialize the database
with app.app_context():
    db.create_all()

# Routes for CRUD operations
@app.route('/')
def index():
    return render_template('index.html')
# --- Student Routes ---
@app.route('/students')
def get_students():
    students = Student.query.all()
    return render_template('students.html', students=students)

@app.route('/students/add', methods=['GET', 'POST'])
def add_student():
    classes = Class.query.all()  # Mengambil semua data kelas
    if request.method == 'POST':
        name = request.form['name']
        class_id = request.form['class_id']  # Menggunakan class_id dari form
        student_number = request.form['student_number']
        
        new_student = Student(name=name, class_id=class_id, student_number=student_number)
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('get_students'))
    
    return render_template('add_student.html', classes=classes)

# Student routes
@app.route('/students/delete/<int:id>')
def delete_student(id):
    student = Student.query.get_or_404(id)
    try:
        db.session.delete(student)
        db.session.commit()
        flash('Student deleted successfully', 'success')
    except IntegrityError:
        db.session.rollback()
        flash('Cannot delete this student because they have associated grades. Please delete the grades first.', 'danger')
    return redirect(url_for('get_students'))

@app.route('/students/update/<int:id>', methods=['GET', 'POST'])
def update_student(id):
    student = Student.query.get_or_404(id)
    classes = Class.query.all()
    if request.method == 'POST':
        try:
            student.name = request.form['name']
            student.class_id = request.form['class_id']
            student.student_number = request.form['student_number']
            db.session.commit()
            flash('Student updated successfully', 'success')
            return redirect(url_for('get_students'))
        except IntegrityError:
            db.session.rollback()
            flash('Update failed. This student number may already be in use.', 'danger')
    return render_template('update_student.html', student=student, classes=classes)

# --- Assignment Routes ---
@app.route('/assignments')
def get_assignments():
    assignments = Assignment.query.all()
    return render_template('assignments.html', assignments=assignments)

@app.route('/assignments/add', methods=['GET', 'POST'])
def add_assignment():
    classes = Class.query.all()  # Fetch all classes
    subjects = Subject.query.all()  # Fetch all subjects
    if request.method == 'POST':
        assignment_name = request.form['assignment_name']
        class_id = request.form['class_id']
        subject_id = request.form['subject_id']
        new_assignment = Assignment(
            assignment_name=assignment_name,
            date_assigned=date.today(),
            class_id=class_id,
            subject_id=subject_id
        )
        db.session.add(new_assignment)
        db.session.commit()
        return redirect(url_for('get_assignments'))
    return render_template('add_assignment.html', classes=classes, subjects=subjects)

@app.route('/assignments/delete/<int:id>')
def delete_assignment(id):
    assignment = Assignment.query.get_or_404(id)
    try:
        db.session.delete(assignment)
        db.session.commit()
        flash('Assignment deleted successfully', 'success')
    except IntegrityError:
        db.session.rollback()
        flash('Cannot delete this assignment because it has associated grades. Please delete the grades first.', 'danger')
    return redirect(url_for('get_assignments'))

@app.route('/assignments/update/<int:id>', methods=['GET', 'POST'])
def update_assignment(id):
    assignment = Assignment.query.get_or_404(id)
    classes = Class.query.all()
    subjects = Subject.query.all()
    if request.method == 'POST':
        try:
            assignment.assignment_name = request.form['assignment_name']
            assignment.class_id = request.form['class_id']
            assignment.subject_id = request.form['subject_id']
            db.session.commit()
            flash('Assignment updated successfully', 'success')
            return redirect(url_for('get_assignments'))
        except IntegrityError:
            db.session.rollback()
            flash('Update failed. Please ensure all fields are filled correctly.', 'danger')
    return render_template('update_assignment.html', assignment=assignment, classes=classes, subjects=subjects)


# Routes for Class
@app.route('/classes')
def get_classes():
    classes = Class.query.all()
    return render_template('classes.html', classes=classes)

@app.route('/class/add', methods=['GET', 'POST'])
def add_class():
    if request.method == 'POST':
        class_name = request.form['class_name']
        new_class = Class(class_name=class_name)
        db.session.add(new_class)
        db.session.commit()
        return redirect(url_for('get_classes'))
    return render_template('add_class.html')

@app.route('/class/delete/<int:id>')
def delete_class(id):
    class_to_delete = Class.query.get_or_404(id)
    try:
        db.session.delete(class_to_delete)
        db.session.commit()
        flash('Class deleted successfully', 'success')
    except IntegrityError:
        db.session.rollback()
        flash('Cannot delete this class because it has associated students or assignments. Please reassign or delete them first.', 'danger')
    return redirect(url_for('get_classes'))

@app.route('/class/update/<int:id>', methods=['GET', 'POST'])
def update_class(id):
    class_to_update = Class.query.get_or_404(id)
    if request.method == 'POST':
        try:
            class_to_update.class_name = request.form['class_name']
            db.session.commit()
            flash('Class updated successfully', 'success')
            return redirect(url_for('get_classes'))
        except IntegrityError:
            db.session.rollback()
            flash('Update failed. This class name may already be in use.', 'danger')
    return render_template('update_class.html', class_item=class_to_update)


# Routes for Subject
@app.route('/subjects')
def get_subjects():
    subjects = Subject.query.all()
    return render_template('subjects.html', subjects=subjects)

@app.route('/subject/add', methods=['GET', 'POST'])
def add_subject():
    if request.method == 'POST':
        subject_name = request.form['subject_name']
        new_subject = Subject(subject_name=subject_name)
        db.session.add(new_subject)
        db.session.commit()
        return redirect(url_for('get_subjects'))
    return render_template('add_subject.html')

@app.route('/subject/delete/<int:id>')
def delete_subject(id):
    subject_to_delete = Subject.query.get_or_404(id)
    try:
        db.session.delete(subject_to_delete)
        db.session.commit()
        flash('Subject deleted successfully', 'success')
    except IntegrityError:
        db.session.rollback()
        flash('Cannot delete this subject because it has associated assignments. Please delete the assignments first.', 'danger')
    return redirect(url_for('get_subjects'))

@app.route('/subject/update/<int:id>', methods=['GET', 'POST'])
def update_subject(id):
    subject_to_update = Subject.query.get_or_404(id)
    if request.method == 'POST':
        try:
            subject_to_update.subject_name = request.form['subject_name']
            db.session.commit()
            flash('Subject updated successfully', 'success')
            return redirect(url_for('get_subjects'))
        except IntegrityError:
            db.session.rollback()
            flash('Update failed. This subject name may already be in use.', 'danger')
    return render_template('update_subject.html', subject=subject_to_update)
# Routes for Grade
@app.route('/grades')
def get_grades():
    grades = Grade.query.all()
    return render_template('grades.html', grades=grades)

@app.route('/grade/add', methods=['GET', 'POST'])
def add_grade():
    students = Student.query.all()
    assignments = Assignment.query.all()
    if request.method == 'POST':
        student_id = request.form['student_id']
        assignment_id = request.form['assignment_id']
        score = request.form['score']
        new_grade = Grade(student_id=student_id, assignment_id=assignment_id, score=score)
        db.session.add(new_grade)
        db.session.commit()
        return redirect(url_for('get_grades'))
    return render_template('add_grade.html', students=students, assignments=assignments)

@app.route('/grade/delete/<int:id>')
def delete_grade(id):
    grade_to_delete = Grade.query.get_or_404(id)
    db.session.delete(grade_to_delete)
    db.session.commit()
    flash('Grade deleted successfully', 'success')
    return redirect(url_for('get_grades'))

@app.route('/grade/update/<int:id>', methods=['GET', 'POST'])
def update_grade(id):
    grade_to_update = Grade.query.get_or_404(id)
    students = Student.query.all()
    assignments = Assignment.query.all()
    if request.method == 'POST':
        try:
            grade_to_update.student_id = request.form['student_id']
            grade_to_update.assignment_id = request.form['assignment_id']
            grade_to_update.score = request.form['score']
            db.session.commit()
            flash('Grade updated successfully', 'success')
            return redirect(url_for('get_grades'))
        except IntegrityError:
            db.session.rollback()
            flash('Update failed. Please ensure all fields are filled correctly.', 'danger')
    return render_template('update_grade.html', grade=grade_to_update, students=students, assignments=assignments)

if __name__ == '__main__':
    app.run(debug=True)
