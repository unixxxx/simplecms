__author__ = 'ShJashiashvili'
import mongoengine as mongo


class Users(mongo.Document):
    username = mongo.fields.StringField(max_length=10, required=True)
    password = mongo.fields.BaseField(required=True)


class Email(mongo.Document):
    email = mongo.fields.EmailField()


class Posts(mongo.Document):
    title = mongo.StringField(required=True)
    content = mongo.StringField(required=True)
    date = mongo.DateTimeField(required=True)


class Themes(mongo.Document):
    title = mongo.StringField(required=True, unique=True)
    date = mongo.DateTimeField(required=True)
    isactive = mongo.BooleanField(required=True, default=False)