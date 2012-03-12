# coding: utf-8

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import users

from model import NoteIndex

def user_bar(page):
    user = users.get_current_user()
    if user:
        return user.nickname()+'<a href='+users.create_logout_url(page)+'> Logout</a>'
    else:
        return 'Guest'+'<a href='+users.create_login_url(page)+'> Login</a>'

class MainPage(webapp.RequestHandler):
    def get(self):
        query = NoteIndex.all()
        content = '<a href="/add">Добавить</a>'
        self.response.out.write(template.render('templates/index.html', {'content':content, 'indexes':query,
                                                                         'userbar':user_bar(page = self.request.uri)}))
    
    def post(self):
        newindex = NoteIndex()
        newindex.title = self.request.get('title')
        newindex.put()
        self.redirect('/')

class AddPage(webapp.RequestHandler):
    def get(self):
        self.response.out.write(template.render('templates/addform.html', {'userbar':user_bar(page = self.request.uri)}))
    def post(self):
        print self.request.arguments()
    
urls = [
    ('/', MainPage),
    ('/add', AddPage),
]
application = webapp.WSGIApplication(urls,debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
