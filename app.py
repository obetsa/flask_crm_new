from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Models


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

    def __repr__(self):
        return '<Employees %r>' % self.employee_id


class Orders(db.Model):
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_dt = db.Column(db.DateTime, default=datetime.now())
    update_dt = db.Column(db.DateTime, nullable=True)
    order_type = db.Column(db.String(25), nullable=False)
    descriptions = db.Column(db.String(200))
    status = db.Column(db.String(10), nullable=False)
    serial_no = db.Column(db.Integer, nullable=False, unique=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'), nullable=False)

    def __repr__(self):
        return '<Orders %r>' % self.order_id


# Routes

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
            return redirect('/all_departments')
        except:
            return "Some Trouble"
    else:
        return render_template("create_department.html")


@app.route('/department/<int:department_id>')
def department_detail(department_id):
    department = Departments.query.get(department_id)
    return render_template('department_detail.html', department=department)


@app.route('/department/<int:department_id>/update', methods=["POST", "GET"])
def update_department(department_id):
    department = Departments.query.get(department_id)
    if request.method == 'POST':
        department.department_name = request.form['department_name']
        try:
            db.session.commit()
            return redirect('/all_departments')
        except:
            return "Some Trouble"
    else:
        return render_template("update_department.html", department=department)


@app.route('/department/<int:department_id>/delete')
def department_delete(department_id):
    department = Departments.query.get_or_404(department_id)

    try:
        db.session.delete(department)
        db.session.commit()
        return redirect('/all_departments')
    except:
        return "Some Trouble"


@app.route('/all_employees')
def all_employees():
    employees = Employees.query.order_by(Employees.fio).all()
    return render_template('employees.html', employees=employees)


@app.route("/create_employee", methods=["POST", "GET"])
def create_employee():
    if request.method == 'POST':
        fio = request.form['fio']
        position = request.form['position']
        department_id = request.form['department_id']
        employee_profile = Employees(fio=fio, position=position, department_id=department_id)
        try:
            db.session.add(employee_profile)
            db.session.commit()
            return redirect('/all_employees')
        except:
            return "Some Trouble"
    else:
        return render_template("create_employee.html")


@app.route('/employee/<int:employee_id>')
def employee_detail(employee_id):
    employee = Employees.query.get(employee_id)
    return render_template('employee_detail.html', employee=employee)


@app.route('/employee/<int:employee_id>/update', methods=["POST", "GET"])
def update_employee(employee_id):
    employee = Employees.query.get(employee_id)
    if request.method == 'POST':
        employee.fio = request.form['fio']
        employee.position = request.form['position']
        employee.department_id = request.form['department_id']
        try:
            db.session.commit()
            return redirect('/all_employees')
        except:
            return "Some Trouble"
    else:
        return render_template("update_employee.html", employee=employee)


@app.route('/employee/<int:employee_id>/delete')
def employee_delete(employee_id):
    employee = Employees.query.get_or_404(employee_id)

    try:
        db.session.delete(employee)
        db.session.commit()
        return redirect('/all_employees')
    except:
        return "Some Trouble"


@app.route('/all_orders')
def all_orders():
    orders = Orders.query.order_by(Orders.create_dt.desc()).all()
    return render_template('orders.html', orders=orders)


@app.route("/create_order", methods=["POST", "GET"])
def create_order():
    if request.method == 'POST':
        order_type = request.form['order_type']
        status = request.form['status']
        serial_no = request.form['serial_no']
        descriptions = request.form['descriptions']
        creator_id = request.form['creator_id']
        order_profile = Orders(order_type=order_type, status=status, serial_no=serial_no,
                               descriptions=descriptions, creator_id=creator_id)
        try:
            db.session.add(order_profile)
            db.session.commit()
            return redirect('/all_orders')
        except:
            return "Some Trouble"

    return render_template("create_order.html")


@app.route('/order/<int:order_id>')
def order_detail(order_id):
    order = Orders.query.get(order_id)
    return render_template('order_detail.html', order=order)


@app.route('/order/<int:order_id>/update', methods=["POST", "GET"])
def update_order(order_id):
    order = Orders.query.get(order_id)
    if request.method == 'POST':
        order.order_type = request.form['order_type']
        order.status = request.form['status']
        order.serial_no = request.form['serial_no']
        order.descriptions = request.form['descriptions']
        order.creator_id = request.form['creator_id']

        try:
            db.session.commit()
            return redirect('/all_orders')
        except:
            return "Some Trouble"
    else:
        return render_template("update_order.html", order=order)


@app.route('/order/<int:order_id>/delete')
def order_delete(order_id):
    order = Orders.query.get_or_404(order_id)

    try:
        db.session.delete(order)
        db.session.commit()
        return redirect('/all_orders')
    except:
        return "Some Trouble"


@app.route('/about')
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
