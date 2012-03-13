# coding: utf-8
import re

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import db

from model import NoteIndex, NoteList

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
    def items_to_insert(self, x):
        if re.match("item-(\d+)", x):
            value = self.request.get(x)
            if value is not u'':
                r = re.match("(.*)\[(\d+)\]", value)
                if r is not None:
                    price = r.groups()[1]
                    value = r.groups()[0]
                else:
                    price = 0
                self.items.append({'name':value, 'price':price})

    def get(self):
        self.response.out.write(template.render('templates/addform.html', {'userbar':user_bar(page = self.request.uri)}))
    def post(self):
        arguments = self.request.arguments()
        title = self.request.get('title')
        self.items = []
        print 1
        map(self.items_to_insert, arguments)
        n = NoteIndex(user=users.get_current_user(), title=title)
        n.put()
        inserts = []
        map(lambda x: inserts.append(NoteList(noteindex = n, name = x['name'], price = int(x['price']))), self.items)
        db.put(inserts)
    
urls = [
    ('/', MainPage),
    ('/add', AddPage),
]
application = webapp.WSGIApplication(urls,debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
