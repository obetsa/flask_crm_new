from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Departments(db.Model):
    department_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    department_name = db.Column(db.String(75), unique=True)

    def __repr__(self):
        return '<Departments %r>' % self.department_id


class Employees(db.Model):
    employee_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fio = db.Column(db.String(50), nullable=False, unique=True)
    position = db.Column(db.String(75))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.department_id'), nullable=False)


class Orders(db.Model):
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_dt = db.Column(db.DateTime, default=datetime.now())
    update_dt = db.Column(db.DateTime, nullable=True)
    order_type = db.Column(db.String(25), nullable=False)
    descriptions = db.Column(db.String(200))
    status = db.Column(db.String(10), nullable=False)
    serial_no = db.Column(db.Integer, nullable=False, unique=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'), nullable=False)


@app.route('/')
@app.route('/crm')
def index():
    return render_template("index.html")

@app.route('/all_departments')
def all_departments():
    departments = Departments.query.order_by(Departments.department_name).all()
    return render_template('departments.html', departments=departments)


@app.route("/create_department", methods=["POST", "GET"])
def create_department():
    if request.method == 'POST':
        department_name = request.form['department_name']
        department_profile = Departments(department_name=department_name)
        try:
            db.session.add(department_profile)
            db.session.commit()
            return redirect('/departments')
        except:
            return "Some Trouble"
    else:
        return render_template("create_department.html")


@app.route('/department/<string:name>/<int:id>')
def departments(name, id):
    return "department: " + name + " - " + str(id)


# @app.route('/employees/<string:name>/<int:id>')
# def employees():
#     return render_template("index.html")
#
#
# @app.route('/orders/<string:name>/<int:id>')
# def orders():
#     return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
