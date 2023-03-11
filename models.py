from mongoengine import Document
from mongoengine.fields import StringField, DateField, ListField, ReferenceField, DateTimeField


class Author(Document):
    fullname = StringField(max_length=50, unique=True)
    born_date = DateTimeField()
    born_location = StringField()
    description = StringField(min_length=10)


class Quote(Document):
    tags = ListField()
    author = ReferenceField(Author)
    quote = StringField()
