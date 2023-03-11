import json
from pprint import pprint
from datetime import datetime
from models import Author, Quote
import connect


def read_data(file):
    with open(file, 'r', encoding='utf-8') as fh:
        data = json.load(fh)
    return data


def fill_author(data_authors):
    Author.drop_collection()
    for data in data_authors:
        author = Author()
        author.fullname = data['fullname']
        author.born_date = datetime.strptime(data['born_date'], "%B %d, %Y").date()
        author.born_location = data['born_location']
        author.description = data['description']
        author.save()


def fill_quote(data_quotes):
    Quote.drop_collection()
    for data in data_quotes:
        quote = Quote()
        quote.tags = data['tags']
        quote.author = Author.objects(fullname=data["author"])[0].id
        quote.quote = data['quote']
        quote.save()


if __name__ == '__main__':
    fill_author(data_authors=read_data('author.json'))
    fill_quote(data_quotes=read_data('quotes.json'))
