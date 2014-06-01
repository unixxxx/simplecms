from bottle import jinja2_template as template, Bottle, request
from models.cmsmodels import Email, Themes
import smtplib
from email.mime.text import MIMEText
import os

app = Bottle()


@app.get('/')
def contactus():
    try:
        theme = Themes.objects.get(isactive=True)
    except Exception as e:
        return template('views/contact.jinja2', {'errorMessage': str(e)})
    return template('views/contact.jinja2', {'theme': theme.title + '.css'})


@app.post('/sendmail')
def sendmail():
    try:
        toaddress = Email.objects.get().email
        theme = Themes.objects.get(isactive=True)
    except Exception as e:
        return template('views/contact.jinja2', {'errorMessage': str(e)})
    name = request.forms.getunicode('inputName')
    email = request.forms.get('inputEmail')
    subject = request.forms.getunicode('inputSubject')
    msg = email + os.linesep + request.forms.getunicode('inputMessage')
    mesg = MIMEText(msg)
    mesg['Subject'] = subject
    mesg['From'] = email
    mesg['To'] = toaddress
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com')
        server.login('tsucms@gmail.com', 'tsucmsadmin')
        server.sendmail(email, toaddress, mesg.as_string())
        server.close()
    except Exception as e:
        return template('views/contact.jinja2', {'errorMessage': str(e)})
    return template('views/contact.jinja2', {'success': 'email sent successfully', 'theme': theme.title + '.css'})


@app.error(404)
def error404(error):
    return template('views/index.jinja2', {'errorMessage': 'page not found'})
