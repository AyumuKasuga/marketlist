# coding: utf-8
import re
from functools import partial

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.api import memcache

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
        if(self.request.get('action') == 'remove'):
            id = self.request.get('id')
            qr = NoteIndex.get_by_id(int(id))
            if (qr.user == users.get_current_user()):
                nl = qr.notelist_set.fetch(1000)
                for i in nl:
                    i.delete()
                qr.delete()
        elif (self.request.get('action') == 'clone'):
            id = self.request.get('id')
            newname = self.request.get('newname')
            if newname is u'':
                return self.error(500)
            n = NoteIndex(user=users.get_current_user(), title=newname)
            n.put()
            ni = NoteIndex.get_by_id(int(id))
            nl = ni.notelist_set.fetch(1000)
            inserts = []
            map(lambda x: inserts.append(NoteList(noteindex=n, name = x.name, price=int(x.price), prefix=x.name[0:2].lower())), nl)
            db.put(inserts)
        elif (self.request.get('action') == 'rename'):
            id = self.request.get('id')
            newname = self.request.get('newname')
            if newname is u'':
                return self.error(500)
            ni = NoteIndex.get_by_id(int(id))
            ni.title = newname
            ni.put()

class GetMyLists(webapp.RequestHandler):
    def get(self):
        query = NoteIndex.all()
        self.response.out.write(template.render('templates/noteslist.html', {'indexes':query}))


class PrepareToInsert():
    def __init__(self, request):
        self.items = []
        self.request = request
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


class AddPage(webapp.RequestHandler):

    def get(self):
        self.response.out.write(template.render('templates/addform.html', {'userbar':user_bar(page = self.request.uri)}))

    def post(self):
        arguments = self.request.arguments()
        title = self.request.get('title')
        self.items = []
        pre = PrepareToInsert(self.request)
        map(pre.items_to_insert, arguments)
        n = NoteIndex(user=users.get_current_user(), title=title)
        n.put()
        inserts = []
        map(lambda x: inserts.append(NoteList(noteindex=n, name = x['name'], price=int(x['price']), prefix=x['name'][0:2].lower())), pre.items)
        db.put(inserts)
        self.redirect('/')


class EditPage(webapp.RequestHandler):
    def get(self, id):
        ni = NoteIndex.get_by_id(int(id))
        nl = ni.notelist_set.fetch(1000)
        editfields = {'title': ni.title, 'id': int(id), 'items':nl}
        self.response.out.write(template.render('templates/addform.html', {'userbar':user_bar(page = self.request.uri), 'edit':True, 'editfields': editfields}))
    
    def post(self, id):
        id = self.request.get('id')
        title = self.request.get('title')
        ni = NoteIndex.get_by_id(int(id))
        ni.title = title
        ni.put()
        db.delete(ni.notelist_set.fetch(1000))
        arguments = self.request.arguments()
        self.items = []
        pre = PrepareToInsert(self.request)
        map(pre.items_to_insert, arguments)
        inserts = []
        map(lambda x: inserts.append(NoteList(noteindex=ni, name = x['name'], price=int(x['price']), prefix=x['name'][0:2].lower())), pre.items)
        db.put(inserts)
        self.redirect('/')

class ViewPage(webapp.RequestHandler):
    def get(self, id):
        ni = NoteIndex.get_by_id(int(id))
        if (ni.user == users.get_current_user()):
            nl = ni.notelist_set.fetch(1000)
            self.response.out.write(template.render('templates/view.html', {'userbar':user_bar(page = self.request.uri), 'items': nl}))


class AcPage(webapp.RequestHandler):
    def get(self):
        ac = self.request.get('term')
        prefix_ac = unicode(ac[0:2].lower())
        ac_items = memcache.get(key=u'ac_' + prefix_ac)
        if ac_items is None:
            ac_items = []
            acquery = NoteList.gql('WHERE prefix = :1', prefix_ac)
            for q in acquery.fetch(1000):
                ac_items.append((q.name, q.price))
            if len(ac_items) > 0:
                ac_items = list(set(ac_items))
                memcache.set(key=u'ac_' + prefix_ac, value=ac_items, time=1800)
        func_search = partial(self.search_filter, ac)
        final_ac_items = filter(func_search, ac_items)
        self.response.out.write(template.render('templates/ac.html', {'items': final_ac_items}))
    
    def search_filter(self, strfind, string):
        if string[0].find(strfind) is not -1:
            return True
        else:
            return False

        

urls = [
    ('/', MainPage),
    ('/add', AddPage),
    ('/view/(\d*)', ViewPage),
    ('/ac', AcPage),
    ('/getmylists', GetMyLists),
    ('/edit/(\d*)', EditPage),
]
application = webapp.WSGIApplication(urls,debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
