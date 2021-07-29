from project import db
from datetime import datetime


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
    department = db.relationship('Departments', backref=db.backref('department', lazy='dynamic'))

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
    employee = db.relationship('Employees', backref=db.backref('employee', lazy='dynamic'))

    def __repr__(self):
        return '<Orders %r>' % self.order_id


class NotificationTasks(db.Model):
    n_task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_dt = db.Column(db.DateTime, default=datetime.now())
    message = db.Column(db.String(100))
    name = db.Column(db.Integer)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    # order = db.relationship('Orders', backref=db.backref('order', lazy='dynamic'))

    def __repr__(self):
        return '<NotificationTasks %r>' % self.n_task_id


class Customers(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_dt = db.Column(db.DateTime)
    c_name = db.Column(db.String(50))
    password = db.Column(db.Integer)
    phone = db.Column(db.Integer)
    email = db.Column(db.String(20))
    chat_id = db.Column(db.Integer)
    is_subscribed = db.Column(db.Boolean, default=False)
    # task = db.relationship('NotificationTasks', backref=db.backref('task', lazy='dynamic'))

    def __repr__(self):
        return '<Customers %r>' % self.customer_id
