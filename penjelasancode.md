
### Fungsi `get_students()`

- **Tujuan**: Menampilkan semua siswa yang ada dalam database.
- **Proses**:
  - Mengambil semua data siswa dari tabel `students` menggunakan `Student.query.all()`.
  - Mengembalikan tampilan HTML `students.html` dengan data siswa yang telah diambil.

```python
@app.route('/students')
def get_students():
    students = Student.query.all()
    return render_template('students.html', students=students)
```

### Fungsi `add_student()`

- **Tujuan**: Menambahkan siswa baru ke dalam database.
- **Proses**:
  - Mengambil semua data kelas dari tabel `classes` untuk ditampilkan dalam form.
  - Jika metode permintaan adalah `POST`, mengambil data dari form (nama, nomor siswa, dan ID kelas).
  - Membuat objek `Student` baru dengan data yang diambil dan menambahkannya ke sesi database.
  - Melakukan commit pada sesi database untuk menyimpan perubahan.
  - Mengarahkan ulang ke halaman daftar siswa setelah siswa baru ditambahkan.
  - Jika metode permintaan adalah `GET`, menampilkan form `add_student.html` untuk menambah siswa baru.

```python
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
```

### Fungsi `delete_student(id)`

- **Tujuan**: Menghapus siswa dari database berdasarkan ID.
- **Proses**:
  - Mengambil data siswa berdasarkan ID yang diberikan.
  - Mencoba menghapus siswa dari sesi database.
  - Jika berhasil, melakukan commit dan menampilkan pesan sukses.
  - Jika gagal karena adanya nilai yang terkait, melakukan rollback dan menampilkan pesan error.
  - Mengarahkan ulang ke halaman daftar siswa setelah operasi selesai.

```python
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
```

### Fungsi `update_student(id)`

- **Tujuan**: Memperbarui informasi siswa yang ada dalam database.
- **Proses**:
  - Mengambil data siswa dan semua kelas dari database.
  - Jika metode permintaan adalah `POST`, mencoba memperbarui data siswa dengan data baru dari form.
  - Jika berhasil, melakukan commit dan menampilkan pesan sukses.
  - Jika gagal karena konflik data (misalnya, nomor siswa sudah digunakan), melakukan rollback dan menampilkan pesan error.
  - Menampilkan form `update_student.html` dengan data siswa saat ini untuk diedit.

```python
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
```

Setiap fungsi di atas menggunakan Flask untuk menangani permintaan HTTP dan SQLAlchemy untuk berinteraksi dengan database. Mereka juga menggunakan mekanisme `flash` untuk menampilkan pesan kepada pengguna setelah operasi database dilakukan.
Berikut adalah penjelasan mendetail dari setiap fungsi dalam kode yang Anda berikan:

## **Rute Mahasiswa**

### **1. `get_students`**

```python
@app.route('/students')
def get_students():
    students = Student.query.all()
    return render_template('students.html', students=students)
```

- **Fungsi**: Mengambil semua data mahasiswa dari database dan menampilkannya pada halaman `students.html`.
- **Proses**:
  - Menggunakan `Student.query.all()` untuk mengambil semua entri mahasiswa dari tabel `students`.
  - Menggunakan `render_template` untuk merender template HTML `students.html` dengan data mahasiswa yang diambil.

### **2. `add_student`**

```python
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
```

- **Fungsi**: Menambahkan mahasiswa baru ke database.
- **Proses**:
  - Mengambil semua data kelas untuk ditampilkan dalam form penambahan mahasiswa.
  - Jika metode permintaan adalah `POST`, data mahasiswa baru diambil dari form.
  - Membuat objek `Student` baru dan menambahkannya ke sesi database.
  - Melakukan `commit` untuk menyimpan perubahan ke database.
  - Mengarahkan ulang ke halaman daftar mahasiswa setelah penambahan berhasil.
  - Jika metode permintaan adalah `GET`, merender template `add_student.html` dengan data kelas untuk pilihan.

### **3. `delete_student`**

```python
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
```

- **Fungsi**: Menghapus mahasiswa dari database berdasarkan ID.
- **Proses**:
  - Mengambil mahasiswa berdasarkan ID yang diberikan. Jika tidak ditemukan, mengembalikan halaman 404.
  - Mencoba menghapus mahasiswa dari sesi database dan melakukan `commit`.
  - Jika berhasil, menampilkan pesan sukses.
  - Jika gagal karena adanya nilai terkait, melakukan `rollback` dan menampilkan pesan kesalahan.
  - Mengarahkan ulang ke halaman daftar mahasiswa.

### **4. `update_student`**

```python
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
```

- **Fungsi**: Memperbarui informasi mahasiswa yang ada di database.
- **Proses**:
  - Mengambil mahasiswa berdasarkan ID yang diberikan. Jika tidak ditemukan, mengembalikan halaman 404.
  - Mengambil semua data kelas untuk ditampilkan dalam form pembaruan mahasiswa.
  - Jika metode permintaan adalah `POST`, memperbarui informasi mahasiswa dengan data dari form.
  - Mencoba melakukan `commit` untuk menyimpan perubahan.
  - Jika berhasil, menampilkan pesan sukses dan mengarahkan ulang ke halaman daftar mahasiswa.
  - Jika terjadi kesalahan, seperti `student_number` yang sudah digunakan, melakukan `rollback` dan menampilkan pesan kesalahan.
  - Jika metode permintaan adalah `GET`, merender template `update_student.html` dengan data mahasiswa dan kelas.

## **Rute Tugas**

### **1. `get_assignments`**

```python
@app.route('/assignments')
def get_assignments():
    assignments = Assignment.query.all()
    return render_template('assignments.html', assignments=assignments)
```

- **Fungsi**: Mengambil semua data tugas dari database dan menampilkannya pada halaman `assignments.html`.
- **Proses**:
  - Menggunakan `Assignment.query.all()` untuk mengambil semua entri tugas dari tabel `assignments`.
  - Menggunakan `render_template` untuk merender template HTML `assignments.html` dengan data tugas yang diambil.

### **2. `add_assignment`**

```python
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
```

- **Fungsi**: Menambahkan tugas baru ke database.
- **Proses**:
  - Mengambil semua data kelas dan mata pelajaran untuk ditampilkan dalam form penambahan tugas.
  - Jika metode permintaan adalah `POST`, data tugas baru diambil dari form.
  - Membuat objek `Assignment` baru dan menambahkannya ke sesi database.
  - Melakukan `commit` untuk menyimpan perubahan ke database.
  - Mengarahkan ulang ke halaman daftar tugas setelah penambahan berhasil.
  - Jika metode permintaan adalah `GET`, merender template `add_assignment.html` dengan data kelas dan mata pelajaran untuk pilihan.

### **3. `delete_assignment`**

```python
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
```

- **Fungsi**: Menghapus tugas dari database berdasarkan ID.
- **Proses**:
  - Mengambil tugas berdasarkan ID yang diberikan. Jika tidak ditemukan, mengembalikan halaman 404.
  - Mencoba menghapus tugas dari sesi database dan melakukan `commit`.
  - Jika berhasil, menampilkan pesan sukses.
  - Jika gagal karena adanya nilai terkait, melakukan `rollback` dan menampilkan pesan kesalahan.
  - Mengarahkan ulang ke halaman daftar tugas.

### **4. `update_assignment`**

```python
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
```

- **Fungsi**: Memperbarui informasi tugas yang ada di database.
- **Proses**:
  - Mengambil tugas berdasarkan ID yang diberikan. Jika tidak ditemukan, mengembalikan halaman 404.
  - Mengambil semua data kelas dan mata pelajaran untuk ditampilkan dalam form pembaruan tugas.
  - Jika metode permintaan adalah `POST`, memperbarui informasi tugas dengan data dari form.
  - Mencoba melakukan `commit` untuk menyimpan perubahan.
  - Jika berhasil, menampilkan pesan sukses dan mengarahkan ulang ke halaman daftar tugas.
  - Jika terjadi kesalahan, melakukan `rollback` dan menampilkan pesan kesalahan.
  - Jika metode permintaan adalah `GET`, merender template `update_assignment.html` dengan data tugas, kelas, dan mata pelajaran.

  Berikut adalah penjelasan mendetail dari setiap fungsi dalam rute untuk **Kelas**, **Mata Pelajaran**, dan **Nilai** dalam kode yang Anda berikan:

## **Rute Kelas**

### **1. `get_classes`**

```python
@app.route('/classes')
def get_classes():
    classes = Class.query.all()
    return render_template('classes.html', classes=classes)
```

- **Fungsi**: Mengambil semua data kelas dari database dan menampilkannya pada halaman `classes.html`.
- **Proses**:
  - Menggunakan `Class.query.all()` untuk mengambil semua entri kelas dari tabel `classes`.
  - Menggunakan `render_template` untuk merender template HTML `classes.html` dengan data kelas yang diambil.

### **2. `add_class`**

```python
@app.route('/class/add', methods=['GET', 'POST'])
def add_class():
    if request.method == 'POST':
        class_name = request.form['class_name']
        new_class = Class(class_name=class_name)
        db.session.add(new_class)
        db.session.commit()
        return redirect(url_for('get_classes'))
    return render_template('add_class.html')
```

- **Fungsi**: Menambahkan kelas baru ke database.
- **Proses**:
  - Jika metode permintaan adalah `POST`, data nama kelas baru diambil dari form.
  - Membuat objek `Class` baru dan menambahkannya ke sesi database.
  - Melakukan `commit` untuk menyimpan perubahan ke database.
  - Mengarahkan ulang ke halaman daftar kelas setelah penambahan berhasil.
  - Jika metode permintaan adalah `GET`, merender template `add_class.html`.

### **3. `delete_class`**

```python
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
```

- **Fungsi**: Menghapus kelas dari database berdasarkan ID.
- **Proses**:
  - Mengambil kelas berdasarkan ID yang diberikan. Jika tidak ditemukan, mengembalikan halaman 404.
  - Mencoba menghapus kelas dari sesi database dan melakukan `commit`.
  - Jika berhasil, menampilkan pesan sukses.
  - Jika gagal karena adanya mahasiswa atau tugas terkait, melakukan `rollback` dan menampilkan pesan kesalahan.
  - Mengarahkan ulang ke halaman daftar kelas.

### **4. `update_class`**

```python
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
```

- **Fungsi**: Memperbarui informasi kelas yang ada di database.
- **Proses**:
  - Mengambil kelas berdasarkan ID yang diberikan. Jika tidak ditemukan, mengembalikan halaman 404.
  - Jika metode permintaan adalah `POST`, memperbarui informasi kelas dengan data dari form.
  - Mencoba melakukan `commit` untuk menyimpan perubahan.
  - Jika berhasil, menampilkan pesan sukses dan mengarahkan ulang ke halaman daftar kelas.
  - Jika terjadi kesalahan, melakukan `rollback` dan menampilkan pesan kesalahan.
  - Jika metode permintaan adalah `GET`, merender template `update_class.html` dengan data kelas.

## **Rute Mata Pelajaran**

### **1. `get_subjects`**

```python
@app.route('/subjects')
def get_subjects():
    subjects = Subject.query.all()
    return render_template('subjects.html', subjects=subjects)
```

- **Fungsi**: Mengambil semua data mata pelajaran dari database dan menampilkannya pada halaman `subjects.html`.
- **Proses**:
  - Menggunakan `Subject.query.all()` untuk mengambil semua entri mata pelajaran dari tabel `subjects`.
  - Menggunakan `render_template` untuk merender template HTML `subjects.html` dengan data mata pelajaran yang diambil.

### **2. `add_subject`**

```python
@app.route('/subject/add', methods=['GET', 'POST'])
def add_subject():
    if request.method == 'POST':
        subject_name = request.form['subject_name']
        new_subject = Subject(subject_name=subject_name)
        db.session.add(new_subject)
        db.session.commit()
        return redirect(url_for('get_subjects'))
    return render_template('add_subject.html')
```

- **Fungsi**: Menambahkan mata pelajaran baru ke database.
- **Proses**:
  - Jika metode permintaan adalah `POST`, data nama mata pelajaran baru diambil dari form.
  - Membuat objek `Subject` baru dan menambahkannya ke sesi database.
  - Melakukan `commit` untuk menyimpan perubahan ke database.
  - Mengarahkan ulang ke halaman daftar mata pelajaran setelah penambahan berhasil.
  - Jika metode permintaan adalah `GET`, merender template `add_subject.html`.

### **3. `delete_subject`**

```python
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
```

- **Fungsi**: Menghapus mata pelajaran dari database berdasarkan ID.
- **Proses**:
  - Mengambil mata pelajaran berdasarkan ID yang diberikan. Jika tidak ditemukan, mengembalikan halaman 404.
  - Mencoba menghapus mata pelajaran dari sesi database dan melakukan `commit`.
  - Jika berhasil, menampilkan pesan sukses.
  - Jika gagal karena adanya tugas terkait, melakukan `rollback` dan menampilkan pesan kesalahan.
  - Mengarahkan ulang ke halaman daftar mata pelajaran.

### **4. `update_subject`**

```python
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
```

- **Fungsi**: Memperbarui informasi mata pelajaran yang ada di database.
- **Proses**:
  - Mengambil mata pelajaran berdasarkan ID yang diberikan. Jika tidak ditemukan, mengembalikan halaman 404.
  - Jika metode permintaan adalah `POST`, memperbarui informasi mata pelajaran dengan data dari form.
  - Mencoba melakukan `commit` untuk menyimpan perubahan.
  - Jika berhasil, menampilkan pesan sukses dan mengarahkan ulang ke halaman daftar mata pelajaran.
  - Jika terjadi kesalahan, melakukan `rollback` dan menampilkan pesan kesalahan.
  - Jika metode permintaan adalah `GET`, merender template `update_subject.html` dengan data mata pelajaran.

## **Rute Nilai**

### **1. `get_grades`**

```python
@app.route('/grades')
def get_grades():
    grades = Grade.query.all()
    return render_template('grades.html', grades=grades)
```

- **Fungsi**: Mengambil semua data nilai dari database dan menampilkannya pada halaman `grades.html`.
- **Proses**:
  - Menggunakan `Grade.query.all()` untuk mengambil semua entri nilai dari tabel `grades`.
  - Menggunakan `render_template` untuk merender template HTML `grades.html` dengan data nilai yang diambil.

### **2. `add_grade`**

```python
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
```

- **Fungsi**: Menambahkan nilai baru ke database.
- **Proses**:
  - Mengambil semua data mahasiswa dan tugas untuk ditampilkan dalam form penambahan nilai.
  - Jika metode permintaan adalah `POST`, data nilai baru diambil dari form.
  - Membuat objek `Grade` baru dan menambahkannya ke sesi database.
  - Melakukan `commit` untuk menyimpan perubahan ke database.
  - Mengarahkan ulang ke halaman daftar nilai setelah penambahan berhasil.
  - Jika metode permintaan adalah `GET`, merender template `add_grade.html` dengan data mahasiswa dan tugas untuk pilihan.

### **3. `delete_grade`**

```python
@app.route('/grade/delete/<int:id>')
def delete_grade(id):
    grade_to_delete = Grade.query.get_or_404(id)
    db.session.delete(grade_to_delete)
    db.session.commit()
    flash('Grade deleted successfully', 'success')
    return redirect(url_for('get_grades'))
```

- **Fungsi**: Menghapus nilai dari database berdasarkan ID.
- **Proses**:
  - Mengambil nilai berdasarkan ID yang diberikan. Jika tidak ditemukan, mengembalikan halaman 404.
  - Menghapus nilai dari sesi database dan melakukan `commit`.
  - Menampilkan pesan sukses.
  - Mengarahkan ulang ke halaman daftar nilai.

### **4. `update_grade`**

```python
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
```

- **Fungsi**: Memperbarui informasi nilai yang ada di database.
- **Proses**:
  - Mengambil nilai berdasarkan ID yang diberikan. Jika tidak ditemukan, mengembalikan halaman 404.
  - Mengambil semua data mahasiswa dan tugas untuk ditampilkan dalam form pembaruan nilai.
  - Jika metode permintaan adalah `POST`, memperbarui informasi nilai dengan data dari form.
  - Mencoba melakukan `commit` untuk menyimpan perubahan.
  - Jika berhasil, menampilkan pesan sukses dan mengarahkan ulang ke halaman daftar nilai.
  - Jika terjadi kesalahan, melakukan `rollback` dan menampilkan pesan kesalahan.
  - Jika metode permintaan adalah `GET`, merender template `update_grade.html` dengan data nilai, mahasiswa, dan tugas.

  
  
Citations:
[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/18441442/3736316d-c3b0-4d35-980f-098c18be55bd/app.py
Citations:
[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/18441442/3736316d-c3b0-4d35-980f-098c18be55bd/app.py
Citations:
[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/18441442/3736316d-c3b0-4d35-980f-098c18be55bd/app.py
  
  
app.py
Berikut adalah penjelasan mendetail dari setiap fungsi dalam kode `app.py` yang diberikan:

### Setup dan Konfigurasi Aplikasi
- **Import Libraries**: Kode ini mengimpor beberapa modul penting seperti `Flask`, `SQLAlchemy`, dan `logging` untuk membangun aplikasi web, mengelola database, dan mencatat log.
- **Konfigurasi Aplikasi**: Aplikasi Flask dikonfigurasi untuk menggunakan database SQLite dan mengatur kunci rahasia untuk sesi.
- **Error Handlers**: Fungsi `page_not_found` dan `internal_server_error` menangani kesalahan HTTP 404 dan 500 dengan menampilkan halaman HTML yang sesuai.

### Model Database
- **Student Model**: Mewakili tabel `students` dengan kolom `id`, `name`, `student_number`, dan `class_id`. Relasi `grades` menghubungkan ke model `Grade`.
- **Class Model**: Mewakili tabel `classes` dengan kolom `id` dan `class_name`. Relasi `students` dan `assignments` menghubungkan ke model `Student` dan `Assignment`.
- **Subject Model**: Mewakili tabel `subjects` dengan kolom `id` dan `subject_name`. Relasi `assignments` menghubungkan ke model `Assignment`.
- **Assignment Model**: Mewakili tabel `assignments` dengan kolom `id`, `assignment_name`, `date_assigned`, `class_id`, dan `subject_id`. Relasi `grades` menghubungkan ke model `Grade`.
- **Grade Model**: Mewakili tabel `grades` dengan kolom `id`, `student_id`, `assignment_id`, dan `score`.

### Inisialisasi Database
- Database diinisialisasi menggunakan konteks aplikasi Flask dengan `db.create_all()` untuk membuat tabel berdasarkan model yang didefinisikan.

### Rute Aplikasi
#### Rute Mahasiswa
- **`/students`**: Menampilkan semua mahasiswa.
- **`/students/add`**: Menambahkan mahasiswa baru menggunakan data dari formulir.
- **`/students/delete/<id>`**: Menghapus mahasiswa berdasarkan `id`.
- **`/students/update/<id>`**: Memperbarui data mahasiswa berdasarkan `id`.

#### Rute Tugas
- **`/assignments`**: Menampilkan semua tugas.
- **`/assignments/add`**: Menambahkan tugas baru.
- **`/assignments/delete/<id>`**: Menghapus tugas berdasarkan `id`.
- **`/assignments/update/<id>`**: Memperbarui data tugas berdasarkan `id`.

#### Rute Kelas
- **`/classes`**: Menampilkan semua kelas.
- **`/class/add`**: Menambahkan kelas baru.
- **`/class/delete/<id>`**: Menghapus kelas berdasarkan `id`.
- **`/class/update/<id>`**: Memperbarui data kelas berdasarkan `id`.

#### Rute Mata Pelajaran
- **`/subjects`**: Menampilkan semua mata pelajaran.
- **`/subject/add`**: Menambahkan mata pelajaran baru.
- **`/subject/delete/<id>`**: Menghapus mata pelajaran berdasarkan `id`.
- **`/subject/update/<id>`**: Memperbarui data mata pelajaran berdasarkan `id`.

#### Rute Nilai
- **`/grades`**: Menampilkan semua nilai.
- **`/grade/add`**: Menambahkan nilai baru.
- **`/grade/delete/<id>`**: Menghapus nilai berdasarkan `id`.
- **`/grade/update/<id>`**: Memperbarui data nilai berdasarkan `id`.

### Menjalankan Aplikasi
- Aplikasi dijalankan dalam mode debug dengan `app.run(debug=True)`.

Fungsi-fungsi ini memungkinkan pengelolaan data mahasiswa, kelas, mata pelajaran, tugas, dan nilai dalam aplikasi berbasis web menggunakan Flask dan SQLAlchemy.

Citations:
[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/18441442/3736316d-c3b0-4d35-980f-098c18be55bd/app.py
studenterss.html
Template yang Anda berikan adalah bagian dari aplikasi web yang menggunakan Flask dan Jinja2 untuk merender halaman HTML. Berikut adalah penjelasan mendetail tentang template tersebut:

## **Struktur Template**

### **1. Penggunaan Template Dasar**

```html
{% extends 'base.html' %}
```

- **Fungsi**: Menggunakan template dasar `base.html` sebagai kerangka utama halaman ini. Template ini mungkin berisi elemen-elemen seperti header, footer, dan navigasi yang konsisten di seluruh halaman aplikasi.

### **2. Blok Konten**

```html
{% block content %}
...
{% endblock content %}
```

- **Fungsi**: Menandai bagian dari template yang akan diisi dengan konten spesifik halaman ini. Semua yang ada di antara `{% block content %}` dan `{% endblock content %}` akan dimasukkan ke dalam blok `content` dari `base.html`.

### **3. Judul Halaman**

```html
<h2 class="mt-4 mb-4">Daftar Siswa</h2>
```

- **Fungsi**: Menampilkan judul halaman "Daftar Siswa" dengan margin atas (`mt-4`) dan margin bawah (`mb-4`) untuk memberikan spasi.

### **4. Tabel Data Siswa**

```html
<table class="table table-striped table-hover">
    <thead class="thead-dark">
        <tr>
            <th>Nama</th>
            <th>Nomor Siswa</th>
            <th>Kelas</th>
            <th>Aksi</th>
        </tr>
    </thead>
    <tbody>
        {% for student in students %}
        <tr>
            <td>{{ student.name }}</td>
            <td>{{ student.student_number }}</td>
            <td>{{ student.class.class_name }}</td>
            <td>
                <a href="{{ url_for('update_student', id=student.id) }}" class="btn btn-sm btn-primary">Edit</a>
                <a href="{{ url_for('delete_student', id=student.id) }}" class="btn btn-sm btn-danger" onclick="return confirm('Apakah Anda yakin ingin menghapus siswa ini?');">Hapus</a>
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
```

- **Fungsi**: Menampilkan data siswa dalam bentuk tabel dengan kolom untuk Nama, Nomor Siswa, Kelas, dan Aksi.
- **Proses**:
  - **Header Tabel**: Menggunakan `thead-dark` untuk memberikan latar belakang gelap pada header tabel.
  - **Looping Data Siswa**: Menggunakan `{% for student in students %}` untuk mengiterasi setiap objek `student` dalam daftar `students` yang diteruskan dari rute Flask.
  - **Kolom Aksi**: Menyediakan tombol untuk mengedit (`Edit`) dan menghapus (`Hapus`) siswa. Tombol hapus memiliki konfirmasi JavaScript untuk memastikan tindakan penghapusan.

### **5. Tombol Tambah Siswa Baru**

```html
<a href="{{ url_for('add_student') }}" class="btn btn-success">Tambah Siswa Baru</a>
```

- **Fungsi**: Menyediakan tautan ke halaman penambahan siswa baru dengan menggunakan `url_for('add_student')` untuk mendapatkan URL rute `add_student`.
- **Tampilan**: Menggunakan kelas `btn btn-success` untuk menampilkan tombol hijau.

## **Kesimpulan**

Template ini dirancang untuk menampilkan daftar siswa dalam bentuk tabel yang rapi dan interaktif. Penggunaan Jinja2 memungkinkan integrasi data dinamis dari backend Flask ke dalam HTML. Tombol aksi memberikan kemampuan untuk mengelola data siswa dengan mudah, termasuk menambah, mengedit, dan menghapus entri.
