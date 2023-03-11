import redis
from redis_lru import RedisLRU
import connect
from models import Quote

client = redis.StrictRedis(host="localhost", port=6379, password=None)
redis_cache = RedisLRU(client)


def parse_input(query):
    return query.split(':')[1].lower()


@redis_cache
def search_quote_by_name(value):
    quotes = Quote.objects()
    author_name = ''
    all_quotes = []
    for quote in quotes:
        if quote.author.fullname.lower() == parse_input(value) or quote.author.fullname.lower().startswith(
                parse_input(value)):
            author_name = quote.author.fullname
            all_quotes.append(quote.quote)
    return f'{author_name}: {" ".join(all_quotes)}'


@redis_cache
def search_quote_by_tag(value):
    quotes = Quote.objects()
    for quote in quotes:
        for tag in quote.tags:
            if tag in parse_input(value):
                return f'{parse_input(value)}: {quote.quote}'


def query():
    while True:
        command = input('Enter command: ')
        check = command.split(':')[0]
        if check == 'name':
            print(search_quote_by_name(command))
        if check in ['tag', 'tags']:
            print(search_quote_by_tag(command))
        if check not in ['name', 'tag', 'tags'] and check != 'exit':
            print('wrong command')
        if 'exit' in command:
            print('Good Bye !!!')
            break


if __name__ == '__main__':
    query()
