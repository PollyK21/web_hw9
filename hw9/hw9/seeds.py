import json
from models import Authors, Quotes
import connect
import os


def load_authors(json_file):
    json_file_path = os.path.join(os.path.dirname(__file__), json_file)
    with open(json_file_path, 'r') as file:
        data = json.load(file)
        for item in data:
            author = Authors(fullname=item['fullname'], born_date=item.get('born_date', ''), 
                            born_location=item.get('born_location', ''), description=item.get('description', ''))
            author.save()


def load_quotes(json_file):
    json_file_path = os.path.join(os.path.dirname(__file__), json_file)
    with open(json_file_path, 'r') as file:
        data = json.load(file)
        for quote_data in data:
            author_fullname = quote_data.get('author', '')
            author = Authors.objects(fullname=author_fullname).first()
            if author:
                quote = Quotes(tags=quote_data.get('tags', []), author=author, quote=quote_data['quote'])
                quote.save()
            else:
                print(f"Author '{author_fullname}' not found in the database. Skipping quote.")


load_authors("authors.json")
load_quotes("qoutes.json")

print("Data loaded successfully!")