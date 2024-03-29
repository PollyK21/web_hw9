from mongoengine import Document
from mongoengine.fields import DateTimeField, ReferenceField, ListField, StringField


class Authors(Document):
    fullname = StringField()
    born_date = DateTimeField()
    born_location = StringField()
    description = StringField()


class Quotes(Document):
    tags = ListField()
    author = ReferenceField(Authors, reverse_delete_rule=2)
    quote = StringField(required=True)

