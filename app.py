from flask import Flask, render_template, request, redirect
from models import db, StudentModel

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f"An error occurred during database initialization: {str(e)}")

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')

    if request.method == 'POST':
        hobbies = ",".join(map(str, request.form.getlist('hobbies')))
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']
        country = request.form['country']

        student = StudentModel(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            gender=gender,
            hobbies=hobbies,
            country=country
        )

        try:
            db.session.add(student)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"An error occurred: {str(e)}"

@app.route('/')
def retrieve_list():
    students = StudentModel.query.all()
    return render_template('datalist.html', students=students)

@app.route('/<int:id>')
def retrieve_student(id):
    student = StudentModel.query.get(id)
    if student:
        return render_template('data.html', student=student)
    return f"Student with id = {id} does not exist"

@app.route('/<int:id>/edit', methods=['GET', 'POST'])
def update(id):
    student = StudentModel.query.get(id)

    if request.method == 'POST':
        if student:
            try:
                db.session.delete(student)
                db.session.commit()
            except Exception as e:
                return f"An error occurred: {str(e)}"

        hobbies = ",".join(map(str, request.form.getlist('hobbies')))
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']
        country = request.form['country']

        student = StudentModel(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            gender=gender,
            hobbies=hobbies,
            country=country
        )

        try:
            db.session.add(student)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"An error occurred: {str(e)}"

    return render_template('update.html', student=student)

@app.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete(id):
    student = StudentModel.query.get(id)
    if request.method == 'POST':
        if student:
            try:
                db.session.delete(student)
                db.session.commit()
                return redirect('/')
            except Exception as e:
                return f"An error occurred: {str(e)}"

    return render_template('delete.html')

if __name__ == '__main__':
    app.run(debug=True)
