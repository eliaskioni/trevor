from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class PlaneModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model_number = db.Column(db.Integer, unique=True)
    capacity = db.Column(db.String(128))
    weight = db.Column(db.Integer)
    planes = db.relationship('Plane', backref='plane', lazy=False)


class Plane(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    registration_number = db.Column(db.String(128), unique=True)
    model_number = db.Column(db.Integer, db.ForeignKey('plane_model.model_number'),
                         nullable=False)


relationship_table = db.Table('expertise_technician_table',
                              db.Column('expertise_id', db.Integer, db.ForeignKey('expertise.id'), nullable=False),
                              db.Column('technician_id', db.Integer, db.ForeignKey('technician.id'), nullable=False),
                              db.PrimaryKeyConstraint('expertise_id', 'technician_id'))


class Expertise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plane_model = db.Column(db.String(128))
    technicians = db.relationship('Technician', secondary=relationship_table, backref='technicians')


class Technician(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    technician_number = db.Column(db.String(128), unique=True)
    address = db.Column(db.String(128))
    phone_number = db.Column(db.String(128))
    salary = db.Column(db.Integer)
    kaa_tests = db.relationship('KenyaPortAuthorityTest', backref='kenya_port_authority_test', lazy=False)


class EmployeeUnion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)


class Employees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employees_number = db.Column(db.String(128), unique=True)
    date_of_medical_check = db.Column(db.DATE)
    is_technician = db.Column(db.Boolean)
    union_id = db.Column(db.Integer, db.ForeignKey('employee_union.id'),
                         nullable=False)


class KenyaPortAuthorityTest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(128), unique=True)
    name = db.Column(db.String(128))
    score = db.Column(db.Integer)
    technician_id = db.Column(db.Integer, db.ForeignKey('technician.id'),
                              nullable=False)
    hours = db.Column(db.Integer)


@app.route('/')
def home():
    # users = [{'name': user.name, 'id': user.id} for user in  User.query.all()]
    plane_models = [{'model_number': plane_model.model_number, 'capacity': plane_model.capacity,
                     'weight': plane_model.weight, 'id': plane_model.id}
                    for plane_model in PlaneModel.query.all()]

    planes = [{'registration_number': plane.registration_number, 'model_number': plane.model_number}
              for plane in Plane.query.all()]

    technicians = [{'name': technician.name, 'technician_number': technician.technician_number,
                    'address': technician.address, 'phone_number': technician.phone_number,
                    'salary': technician.salary, 'id': technician.id}
                   for technician in Technician.query.all()]
    return render_template('hello.html',
                           name='Elias',
                           plane_models=plane_models,
                           planes=planes,
                           technicians=technicians)


@app.route('/create-plane-model', methods=['POST'])
def create_plane_model():
    model_number = request.form.get('model_number')
    capacity = request.form.get('capacity')
    weight = request.form.get('weight')
    plane_model = PlaneModel(model_number=model_number,
                             capacity=capacity,
                             weight=weight)
    db.session.add(plane_model)
    db.session.commit()
    return redirect('/')


@app.route('/create-plane', methods=['POST'])
def create_plane():
    plane_model = PlaneModel.query.get(request.form.get('plane_model'))
    registration_number = request.form.get('reg_number')
    plane = Plane(model_number=plane_model.model_number, registration_number=registration_number)
    db.session.add(plane)
    db.session.commit()
    return redirect('/')


@app.route('/create-expertise', methods=['POST'])
def create_expert():
    plane_model = request.form.get('plane_model')
    expertise = Expertise(plane_model=plane_model)
    technicians = Technician.query.all()
    expertise.technicians.append(technicians)
    db.session.add(expertise)
    db.session.commit()
    return redirect('/')


@app.route('/create-technician', methods=['POST'])
def create_technician():
    name = request.form.get('name')
    technician_number = request.form.get('t_number')
    address = request.form.get('address')
    phone_number = request.form.get('phone_number')
    salary = request.form.get('salary')

    technician = Technician(
        name=name,
        technician_number=technician_number,
        address=address,
        phone_number=phone_number,
        salary=salary
    )

    db.session.add(technician)
    db.session.commit()
    return redirect('/')


@app.route('/create-union', methods=['POST'])
def create_union():
    name = request.form.get('name')
    union = EmployeeUnion(
        name=name
    )
    db.session.add(union)
    db.session.commit()
    return redirect('/')


@app.route('/create-employee', methods=['POST'])
def create_employee():
    employees_number = request.form.get('e_number')
    date_of_medical_check = request.form.get('date_of_medical_check')
    is_technician = False
    union_id = request.form.get('union_id')

    employee = Employees(
        employees_number=employees_number,
        date_of_medical_check=date_of_medical_check,
        is_technician=is_technician,
        union_id=union_id
    )

    db.session.add(employee)
    db.session.commit()
    return redirect('/')


@app.route('/create-kaa-test', methods=['POST'])
def create_kaa_test():
    number = request.form.get('kaa_test_number')
    name = request.form.get('name')
    score = request.form.get('score')
    hours = request.form.get('hours')
    technician_id = request.form.get('technician_id')

    test = KenyaPortAuthorityTest(
        number=number,
        name=name,
        score=score,
        hours=hours,
        technician_id=technician_id
    )

    db.session.add(test)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run()
