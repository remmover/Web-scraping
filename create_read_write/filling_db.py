import json
import random

from faker import Faker
from mongoengine import connect, MultipleObjectsReturned

from create_read_write.models import Author, Quote, Contact

connect(
    db="mein",
    host="mongodb+srv://remmover:789456@cluster0.uhuxtdj.mongodb.net/?retryWrites=true&w=majority"
)

fake = Faker()


def load_data_from_json(json_file):
    with open(json_file, "r", encoding='utf-8') as fh:
        data = json.load(fh)
    return data


def save_authors_to_database(authors):
    Author.objects().delete()
    try:
        for author in authors:
            Author(
                fullname=author["fullname"],
                born_date=author["born_date"],
                born_location=author["born_location"],
                description=author["description"],
            ).save()
        print("Authors data loaded successfully.")
    except Exception as e:
        print(f"Error loading quotes data: {str(e)}")


def save_quotes_to_database(quotes):
    Quote.objects().delete()
    try:
        for quote in quotes:
            try:
                author = Author.objects.get(fullname=quote["author"])
            except MultipleObjectsReturned:
                continue

            Quote(tags=quote["tags"], author=author, text=quote["text"]).save()

        print("Quotes data loaded successfully.")
    except Exception as e:
        print(f"Error loading quotes data: {str(e)}")


def save_contacts_to_database():
    Contact.objects().delete()
    try:
        for _ in range(30):
            Contact(
                fullname=fake.name(),
                email=fake.email(),
                phone=fake.phone_number(),
                preferred_contact_method=random.choice(["email", "sms"]),
                logic_=False,
            ).save()
        print("Contacts data loaded successfully.")
    except Exception as e:
        print(f"Error loading quotes data: {str(e)}")


def main():
    authors_json_file = "C:/Mein/Projects/Web-scraping/data/author.json"
    quotes_json_file = "C:/Mein/Projects/Web-scraping/data/quotes.json"

    authors_data = load_data_from_json(authors_json_file)
    quotes_data = load_data_from_json(quotes_json_file)

    save_authors_to_database(authors_data)
    save_quotes_to_database(quotes_data)
    save_contacts_to_database()


if __name__ == "__main__":
    main()

