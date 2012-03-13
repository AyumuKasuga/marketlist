from google.appengine.ext import db

class NoteIndex(db.Model):
    user = db.UserProperty(required=True)
    date = db.DateTimeProperty(auto_now_add=True, required=True)
    title = db.StringProperty(required=True)
    
class NoteList(db.Model):
    noteindex = db.ReferenceProperty(NoteIndex)
    name = db.StringProperty(required=True)
    price = db.IntegerProperty()
    