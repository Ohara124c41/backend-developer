from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)), nullable=False)
    website_link = db.Column(db.String(500))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    shows = db.relationship(
        'Show',
        backref='venue',
        cascade='all, delete-orphan',
        lazy=True,
    )

    __table_args__ = (
        db.UniqueConstraint('name', 'city', 'state', name='uq_venue_name_city_state'),
    )


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)), nullable=False)
    website_link = db.Column(db.String(500))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    shows = db.relationship(
        'Show',
        backref='artist',
        cascade='all, delete-orphan',
        lazy=True,
    )

    __table_args__ = (
        db.UniqueConstraint('name', 'city', 'state', name='uq_artist_name_city_state'),
    )


class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
