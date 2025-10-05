from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.orm import deferred
import json

# Association table for favorites (many-to-many relationship)
favorites = db.Table('favorites',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('car_id', db.Integer, db.ForeignKey('car.id'), primary_key=True),
    db.Column('created_at', db.DateTime, default=db.func.current_timestamp())
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    cars = db.relationship('Car', backref='owner', lazy='dynamic')
    
    # Favorites relationship
    favorite_cars = db.relationship('Car', secondary=favorites, 
                                   lazy='dynamic',
                                   backref=db.backref('favorited_by', lazy='dynamic'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def add_favorite(self, car):
        if not self.has_favorited(car):
            self.favorite_cars.append(car)
    
    def remove_favorite(self, car):
        if self.has_favorited(car):
            self.favorite_cars.remove(car)
    
    def has_favorited(self, car):
        return self.favorite_cars.filter(favorites.c.car_id == car.id).count() > 0

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(64))
    model = db.Column(db.String(64))
    year = db.Column(db.Integer)
    price = db.Column(db.Float)
    engine = db.Column(db.String(64))  # e.g., '2.0L'
    mileage = db.Column(db.Integer)
    category = db.Column(db.String(64))  # e.g., 'Sedan'
    gearbox = db.Column(db.String(32))  # 'Automatic', 'Manual'
    steering = db.Column(db.String(32))  # 'Left', 'Right'
    drive = db.Column(db.String(32))  # 'Front', 'Rear', '4x4'
    doors = db.Column(db.String(32))  # '2/3', '4/5', '>5'
    tech_inspection = db.Column(db.Boolean)
    catalyst = db.Column(db.Boolean)
    features = db.Column(db.Text)  # JSON list of features
    color = db.Column(db.String(64))
    interior_material = db.Column(db.String(64))
    interior_color = db.Column(db.String(64))
    description = db.Column(db.Text)
    images = db.Column(db.Text)  # JSON list of image paths
    # videos = db.Column(db.Text, nullable=True, default=None)  # JSON list of video paths (optional) - Commented out until database migrated
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def get_features(self):
        return json.loads(self.features) if self.features else []

    def set_features(self, features_list):
        self.features = json.dumps(features_list)

    def get_images(self):
        return json.loads(self.images) if self.images else []

    def set_images(self, images_list):
        self.images = json.dumps(images_list)
    
    def get_videos(self):
        try:
            return json.loads(self.videos) if self.videos else []
        except (AttributeError, TypeError):
            # Handle case where videos column doesn't exist yet
            return []
    
    def set_videos(self, videos_list):
        try:
            self.videos = json.dumps(videos_list)
        except AttributeError:
            # Silently skip if videos column doesn't exist
            pass