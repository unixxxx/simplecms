import math
from datetime import datetime

from bottle import jinja2_template as template, request, redirect

from models.cmsmodels import Posts
import admin.session as withsession


app = withsession.app


@withsession.app.app.get('/posts/<page:int>')
@withsession.app.app.get('/posts')
@withsession.issessionactive()
def posts(page=1):
    try:
        returned_posts = Posts.objects.order_by('-date').skip((int(page) - 1) * 10).limit(10)
        postcount = Posts.objects().count()
        data = {
            "posts": returned_posts,
            "count": postcount,
            "ceil": math.ceil(postcount / 10),
            "currentPage": page
        }
    except:
        return template('admin/views/login.jinja2', {'errorMessage': 'DB error'})
    return template('admin/views/posts.jinja2', data)


@withsession.app.app.route('/posts/addpost', method=['GET', 'POST'])
@withsession.issessionactive()
def savepost():
    if request.method == 'GET':
        return template('admin/views/addoreditpost.jinja2')
    else:
        try:
            title = request.forms.getunicode('title')
            content = request.forms.getunicode('content')
            p_id = request.forms.get('isediting')
            if p_id:
                post = Posts.objects.get(id=p_id)
            else:
                post = Posts()
            post.title = title
            post.content = content
            post.date = datetime.now()
            post.save()
        except:
            return template('admin/views/login.jinja2', {'errorMessage': 'DB error'})
        redirect('/admin/posts')


@withsession.app.app.get('/posts/editpost')
@withsession.issessionactive()
def editpost():
    post_id = request.params.get('id')
    try:
        post = Posts.objects.get(id=post_id)
        if post:
            return template('admin/views/addoreditpost.jinja2', {'post': post})
        else:
            raise Exception()
    except:
        redirect('/admin/posts')


@withsession.app.app.route('/posts/delete', method=['POST'])
def deletepost():
    try:
        Posts.objects(id=request.forms.get('id')).delete()
        return 'ok'
    except:
        return 'failed'


def initialize():
    print('post controller initialized')
