import base64

from bottle import jinja2_template as template, request

from models.cmsmodels import Users
import admin.session as withsession


@withsession.app.app.route('/password', method=['GET', 'POST'])
@withsession.issessionactive()
def password():
    try:
        if request.method == 'GET':
            return template('admin/views/password.jinja2')
        else:
            user = Users.objects.get()
            if user and user.password == base64.b64encode(bytes(request.forms.get('oldPassword'), 'UTF8')):
                user.password = base64.b64encode(bytes(request.forms.get('newPassword'), 'UTF8'))
                user.save()
                return template('admin/views/password.jinja2', {"saved": True})
            else:
                return template('admin/views/password.jinja2',
                                {"saved": False, "errorMessage": "incorrect password"})
    except:
        return template('admin/views/password.jinja2',
                        {"saved": False, "errorMessage": "DB error"})


def initialize():
    print('password controller initialized')