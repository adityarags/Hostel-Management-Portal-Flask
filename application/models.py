from .database import db
from flask_security import UserMixin, RoleMixin


roles_users = db.Table('roles_users', 
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    email = db.Column(db.String(225), unique = True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary = roles_users, backref = db.backref('users', lazy = 'dynamic'))

class Role(db.Model, RoleMixin):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key = True)
    name =  db.Column(db.String(40))
    description = db.Column(db.String(255))


class Complaint(db.Model):
    __tablename__ = "complaint"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    userid = db.Column(db.Integer)
    hostelName = db.Column(db.String(255))
    category = db.Column(db.String(255))
    name = db.Column(db.String(255))
    availability = db.Column(db.String(255))
    room_no = db.Column(db.Integer)
    phone_no = db.Column(db.Integer)
    description = db.Column(db.String(255))
    status = db.Column(db.String(255))
    extra = db.Column(db.String(255))

    def __init__(self, userid, hostelName, category, name, avail, rno, pno, desc):
        self.userid = userid
        self.hostelName = hostelName
        self.category = category
        self.name = name
        self.availability = avail
        self.room_no = rno
        self.phone_no = pno
        self.description = desc
        self.status = "Pending"
        self.extra = "-"

