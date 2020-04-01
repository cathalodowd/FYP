from finalyearproject import db


class Course(db.Model):
    modCode = db.Column(db.String(20), primary_key=True)
    modName = db.Column(db.String(80), unique=False)
    modLect = db.Column(db.String(30), unique=False)
    modYear = db.Column(db.Integer, unique=False)

    venues = db.relationship('Venue', backref='course', lazy='dynamic')

    def __repr__(self):
        return f"Course('{self.modCode}', {self.modName}', '{self.modLect}', '{self.modYear}'"


class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    venue = db.Column(db.String(30), unique=False)
    longitude = db.Column(db.String(80), unique=False)
    latitude = db.Column(db.String(80), unique=False)
    capacity = db.Column(db.Integer, unique=False)
    floorNo = db.Column(db.Integer, unique=False)
    day = db.Column(db.String(20), unique=False)
    time = db.Column(db.String(20), unique=False)
    course_modCode = db.Column(db.String(20), db.ForeignKey('course.modCode'))

    def __repr__(self):
        return f"Venue('{self.venue}', {self.longitude}', '{self.latitude}', '{self.course_modCode}'"
