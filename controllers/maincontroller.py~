from bottle import Bottle, static_file, jinja2_template as template, request, run
from config import configure, registermainuser
from admin.controllers import admincontroller
from controllers import contactcontroller
from models.cmsmodels import Posts, Themes
import math


configure()
registermainuser()
application = Bottle()
app = application
app.mount('/admin', admincontroller.app)
app.mount('/contact', contactcontroller.app)


@app.get('/<page:int>')
@app.get('/')
def index(page=1):
    searchcriteria = request.query.getunicode('search')
    try:
        returned_posts = Posts.objects.order_by('-date').skip((int(page) - 1) * 10).limit(
            10) if not searchcriteria else Posts.objects(title__icontains=searchcriteria).order_by('-date').skip(
            (int(page) - 1) * 10).limit(10)
        postcount = Posts.objects().count() if not searchcriteria else Posts.objects(title__icontains=searchcriteria).count()
        theme = Themes.objects.get(isactive=True)
        if theme:
            data = {
                "posts": returned_posts,
                "count": postcount,
                "ceil": math.ceil(postcount / 10),
                "currentPage": page,
                "theme": theme.title + '.css'
            }
        else:
            return template('views/index.jinja2', {'errorMessage': 'incorrect theme'})
    except Exception as e:
        return template('views/index.jinja2', {'errorMessage': str(e)})
    return template('views/index.jinja2', data)


@app.get('/static/<path:path>')
def static(path):
    return static_file(path, root='static')


@app.error(404)
def error404(error):
    return template('views/index.jinja2', {'errorMessage': 'page not found'})


if __name__ == '__main__':
    run(app, host='localhost', port=8081, debug=True)


