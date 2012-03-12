from google.appengine.ext import db

class NoteIndex(db.Model):
    title = db.StringProperty()