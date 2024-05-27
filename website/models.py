from . import db
from flask_login import UserMixin
from datetime import datetime

# many-to-many relationship amongst user and product database models
user_product_association = db.Table('user_product_association',
    db.Column('user_id', db.Integer, db.ForeignKey('user_database.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('product_database.id')),
    db.Column('quantity', db.Integer),
    db.Column('date_added', db.DateTime, default=datetime.utcnow),
    db.UniqueConstraint('user_id', 'product_id', name='unique_user_product')
)


# database model to store user info
class UserDatabase(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))

    # relationship with product database model
    products = db.relationship('ProductDatabase', secondary=user_product_association, backref='users_rls')


# database model to store product info
class ProductDatabase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(150))
    description = db.Column(db.String(500))
    price = db.Column(db.Integer)
    stock = db.Column(db.Integer)

    # relationship with user database model
    users = db.relationship('UserDatabase', secondary=user_product_association, backref='products_rls')


class UserBasket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_database.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product_database.id'))
    quantity = db.Column(db.Integer)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # defining relationship between user and product database
    user = db.relationship('UserDatabase', backref='baskets')
    product = db.relationship('ProductDatabase', backref='baskets')


class Likes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_database.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product_database.id'))

    # defining relationship between user and product database
    user = db.relationship('UserDatabase', backref='likes')
    product = db.relationship('ProductDatabase', backref='likes')
