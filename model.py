from google.appengine.ext import db


class NoteIndex(db.Model):
    user = db.UserProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    title = db.StringProperty()


class NoteList(db.Model):
    noteindex = db.ReferenceProperty(NoteIndex)
    name = db.StringProperty()
    prefix = db.StringProperty()
    price = db.IntegerProperty()
