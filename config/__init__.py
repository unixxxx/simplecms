import base64
import os
import mongoengine


__author__ = 'ShJashiashvili'
import bottle
import os
from models.cmsmodels import Users, Email, Posts
from datetime import datetime


DB_CREDENTIALS = {
    'creds': {
        'username': os.environ['OPENSHIFT_MONGODB_DB_USERNAME'],
        'password': os.environ['OPENSHIFT_MONGODB_DB_PASSWORD'],
        'host': os.environ['OPENSHIFT_MONGODB_DB_HOST'],
        'port': int(os.environ['OPENSHIFT_MONGODB_DB_PORT'])
    },
    'db': os.environ['OPENSHIFT_APP_NAME']
}


def configure():
    # connect to mongodb instance
    try:
        mongoengine.connect(db=DB_CREDENTIALS['db'], **DB_CREDENTIALS['creds'])
    except:
        print('error while connecting to db')

    # override template path
    separator = os.sep
    bottle.TEMPLATE_PATH.insert(0, separator.join(str(os.getcwd()).split(separator)))

def registermainuser():
    try:
        if Users.objects().count() == 0:
            user = Users()
            user.username = 'admin'
            user.password = base64.b64encode(bytes('admin', 'UTF8'))
            user.save()
        if Email.objects().count() == 0:
            email = Email()
            email.email = 'admin@tsu.ge'
            email.save()
        if Posts.objects.count() == 0:
            post = Posts()
            post.title = 'სატესტო'
            post.content = "სატესტო პოსტი"
            post.date = datetime.now()
            post.save()
    except:
        print('error while connecting to db')



