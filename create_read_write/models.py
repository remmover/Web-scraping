from mongoengine import Document, ReferenceField, StringField, connect, ListField, BooleanField

connect(db="mein", host="mongodb+srv://remmover:789456@cluster0.uhuxtdj.mongodb.net/?retryWrites=true&w=majority")


class Author(Document):
    fullname = StringField(max_length=100, required=True)
    born_date = StringField(max_length=30, required=True)
    born_location = StringField(required=True)
    description = StringField(required=True)
    meta = {
        "collection": "authors",
        "indexes": [("fullname", "born_date")],
    }


class Quote(Document):
    tags = ListField(StringField(required=True))
    author = ReferenceField(Author, required=True)
    text = StringField(required=True)
    meta = {'collection': 'quotes'}


class Contact(Document):
    fullname = StringField(max_length=100, required=True)
    email = StringField(max_length=40, required=True)
    phone = StringField(max_length=30, required=True)
    preferred_contact_method = StringField(max_length=10)
    logic_ = BooleanField(required=True)
    meta = {'collection': 'contacts'}
