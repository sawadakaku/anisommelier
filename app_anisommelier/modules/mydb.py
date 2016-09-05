from google.appengine.ext import ndb

class Personalanswer(ndb.Model):
    question = ndb.StringProperty(indexed=False)
    answer = ndb.StringProperty(indexed=False)
