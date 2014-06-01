from bottle import jinja2_template as template, request, redirect
import os
import admin.session as withsession
from datetime import datetime
from models.cmsmodels import Themes
import math


@withsession.app.app.get('/themes/<page:int>')
@withsession.app.app.get('/themes')
@withsession.issessionactive()
def themes(page=1):
    try:
        returned_themes = Themes.objects.order_by('-date').skip((int(page) - 1) * 10).limit(10)
        themecount = Themes.objects().count()
        data = {
            "themes": returned_themes,
            "count": themecount,
            "ceil": math.ceil(themecount / 10),
            "currentPage": page
        }
    except:
        return template('admin/views/login.jinja2', {'errorMessage': 'DB error'})
    return template('admin/views/themes.jinja2', data)


@withsession.app.app.post('/themes/uploadtheme')
@withsession.issessionactive()
def uploadtheme():
    file = request.files.get('newtheme')
    if file:
        name, ext = os.path.splitext(file.filename)
        if ext == '.css':
            try:
                save_path = os.path.join(os.getcwd(),'static','css', file.filename)
                print(save_path)
                save_path = os.path.abspath(save_path)
                if os.path.exists(save_path):
                    os.remove(save_path)
                file.save(save_path)
                theme = None
                try:
                    theme = Themes.objects.get(title=name)
                except:
                    pass

                if not theme:
                    for t in Themes.objects():
                        t.isactive = False
                        t.save()
                    theme = Themes()
                    theme.title = name
                    theme.date = datetime.now()
                    theme.isactive = True
                    theme.save()

                themecount = Themes.objects().count()
                returned_themes = Themes.objects.order_by('-date').skip((int(1) - 1) * 10).limit(10)
                data = {
                    "themes": returned_themes,
                    "count": themecount,
                    "ceil": math.ceil(themecount / 10),
                    "currentPage": 1
                }
                return template('admin/views/themes.jinja2', data)
            except Exception as e:
                return template('admin/views/themes.jinja2', {'errorMessage': str(e)})
        else:
            return template('admin/views/themes.jinja2', {'errorMessage': 'file extension not allowed!'})
    else:
        return template('admin/views/themes.jinja2', {'errorMessage': "couldn't save file"})
    return template('admin/views/themes.jinja2')


@withsession.app.app.route('/themes/delete', method=['POST'])
@withsession.issessionactive()
def deletetheme():
    try:
        Themes.objects(id=request.forms.get('id')).delete()
        save_path = os.path.join(os.getcwd(),'static','css', request.forms.get('name') + '.css')
        save_path = os.path.abspath(save_path)
        if os.path.exists(save_path):
            os.remove(save_path)
        return 'ok'
    except:
        return 'failed'


@withsession.app.app.route('/themes/activate', method=['POST'])
@withsession.issessionactive()
def activatetheme():
    try:
        theme = Themes.objects.get(id=request.forms.get('id'))
        if theme and not theme.isactive:
            for t in Themes.objects():
                t.isactive = False
                t.save()
            theme.isactive = True
            theme.save()
        return 'ok'
    except Exception as e:
        print(str(e))
        return 'failed'


def initialize():
    print('theme controller initialized')
