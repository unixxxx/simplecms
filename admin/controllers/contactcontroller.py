from bottle import jinja2_template as template, request

from models.cmsmodels import Email
import admin.session as withsession


@withsession.app.app.route('/contact', method=['GET', 'POST'])
@withsession.issessionactive()
def contact():
    try:
        if request.method == 'GET':
            email = Email.objects.get()
            return template('admin/views/contact.jinja2', {"email": email.email, "saved": False})
        else:
            email = Email.objects.get()
            email.email = request.forms.get('email')
            email.save()
            return template('admin/views/contact.jinja2', {"email": email.email, "saved": True})
    except:
        return template('admin/views/contact.jinja2',
                        {"saved": False, "errorMessage": "DB error"})


def initialize():
    print('contact controller initialized')
