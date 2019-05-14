from app import db


class PlaneModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model_number = db.Column(db.Integer)
    capacity = db.Column(db.String(128))
    weight = db.Column(db.Integer)
    planes = db.relationship('AirPlane', backref='plane', lazy=False)


class Plane(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    registration_number = db.Column(db.String(128))
    model_id = db.Column(db.Integer, db.ForeignKey('plane_model.id'),
                         nullable=False)


relationship_table = db.Table('expertise_technician_table',
                              db.Column('expertise_id', db.Integer, db.ForeignKey('expertise.id'), nullable=False),
                              db.Column('technician_id', db.Integer, db.ForeignKey('technician.id'), nullable=False),
                              db.PrimaryKeyConstraint('expertise_id', 'technician_id'))


class Expertise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plane_model = db.Column(db.Integer, db.ForeignKey('plane_model.id'),
                            nullable=False)
    technicians = db.relationship('Technician', secondary=relationship_table, backref='technicians' )


class Technician(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    technician_number = db.Column(db.String(128))
    address = db.Column(db.String(128))
    phone_number = db.Column(db.String(128))
    salary = db.Column(db.Integer)
    kaa_tests = db.relationship('KenyaPortAuthorityTest', backref='kenya_port_authority_test', lazy=False)
    expertise_s = db.relationship('Expertise', backref='expertise_s', lazy=False)


class Employees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employees_number = db.Column(db.String(128))
    union = db.Column()
    date_of_medical_check = db.Column(db.DATE)
    is_technician = db.Column(db.Boolean)


class KenyaPortAuthorityTest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(128))
    name = db.Column(db.String(128))
    score = db.Column(db.Integer)
    technician_id = db.Column(db.Integer, db.ForeignKey('technician.id'),
                              nullable=False)
    hours = db.Column(db.Interval)
