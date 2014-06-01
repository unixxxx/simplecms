import base64

from bottle import jinja2_template as template, request, response, redirect

from models.cmsmodels import Users
import admin.session as withsession
import uuid

app = withsession.app


@withsession.app.app.get('/')
@withsession.app.app.get('/index')
@withsession.issessionactive()
def index():
    return template('admin/views/index.jinja2')


@withsession.app.app.route('/login', method=['GET', 'POST'])
def login():
    withsession.session = request.environ.get('beaker.session')
    loggedin = request.cookies.get('loggedin')
    if request.method == 'GET' and not loggedin and loggedin not in withsession.session:
        return template('admin/views/login.jinja2')
    elif request.method == 'GET' and loggedin and loggedin in withsession.session:
        redirect('index')
    else:
        try:
            postedname=request.forms.get('username')
            postedpassword=request.forms.get('password')
            if postedname and postedpassword:
                user = Users.objects.get(username=postedname,password=base64.b64encode(bytes(postedpassword, 'UTF8')))
                if user:
                    global username
                    guid=uuid.uuid1()
                    username=user.username
                    withsession.session['loggedin'] = str(guid)
                    response.set_cookie('loggedin', str(guid), max_age=600)
                    return template('admin/views/index.jinja2')
                else:
                    return template('admin/views/login.jinja2', {'errorMessage': 'Invalid Username or Password'})
            else:
                return template('admin/views/login.jinja2')
        except Exception as e:
            return template('admin/views/login.jinja2', {'errorMessage': str(e)})


@withsession.app.app.route('/logout', method=['GET', 'POST'])
@withsession.issessionactive()
def logout():
    del (withsession.session['loggedin'])
    redirect('login')



