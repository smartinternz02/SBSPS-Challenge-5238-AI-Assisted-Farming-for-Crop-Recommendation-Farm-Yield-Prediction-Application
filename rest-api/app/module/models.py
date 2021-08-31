from app import db

class crop_details(db.Model):
    crop = db.Column(db.String(200),primary_key=True)
    n = db.Column(db.Float,nullable=False)
    p = db.Column(db.Float, nullable=False)
    k =db.Column(db.Float,nullable=False)
    temperature = db.Column(db.Float,nullable=False)
    humidity = db.Column(db.Float,nullable=False)
    ph = db.Column(db.Float,nullable=False)
    rainfall = db.Column(db.Float,nullable=False)

class rain_info(db.Model):
    state = db.Column(db.String(200),primary_key=True)
    january = db.Column(db.Float,nullable=False)
    february = db.Column(db.Float,nullable=False)
    march = db.Column(db.Float,nullable=False)
    april = db.Column(db.Float,nullable=False)
    may = db.Column(db.Float,nullable=False)
    june = db.Column(db.Float,nullable=False)
    july = db.Column(db.Float,nullable=False)
    august = db.Column(db.Float,nullable=False)
    september = db.Column(db.Float,nullable=False)
    october = db.Column(db.Float,nullable=False)
    november = db.Column(db.Float,nullable=False)
    december = db.Column(db.Float,nullable=False)

class msp_details(db.Model):
    crop = db.Column(db.String(200),primary_key=True)
    year2010 = db.Column(db.Integer,nullable=False)
    year2011 = db.Column(db.Integer, nullable=False)
    year2012 = db.Column(db.Integer, nullable=False)
    year2013 = db.Column(db.Integer, nullable=False)
    year2014 = db.Column(db.Integer, nullable=False)
    year2015 = db.Column(db.Integer, nullable=False)
    year2016 = db.Column(db.Integer, nullable=False)
    year2017 = db.Column(db.Integer, nullable=False)
    year2018 = db.Column(db.Integer, nullable=False)
    year2019 = db.Column(db.Integer, nullable=False)
    year2020 = db.Column(db.Integer, nullable=False)
    year2021 = db.Column(db.Integer, nullable=False)

class user(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(200),nullable=False)
    hashed_password = db.Column(db.String(200),nullable=False)
    api_token = db.Column(db.String(200),nullable=False)
    auth_key = db.Column(db.String(200),nullable=False)