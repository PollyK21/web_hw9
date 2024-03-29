from models import Authors, Quotes
import re
import connect
import sys
import redis
from redis_lru import RedisLRU

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def search_quotes_by_author(author_name):
    print(f"Function call")
    regex = re.compile(re.escape(author_name), re.IGNORECASE)
    author = Authors.objects(fullname=regex).first()
    if author:
        quotes = Quotes.objects(author=author)
        return quotes


@cache
def search_quotes_by_tag(tag):
    regex = re.compile(re.escape(tag), re.IGNORECASE)
    quotes = Quotes.objects(tags__icontains=regex)
    return quotes


@cache
def search_quotes_by_tags(tags):
    tags_list = tags.split(',')
    quotes = Quotes.objects(tags__in=tags_list)
    return quotes


def main():
    while True:
        command = input("Enter command (name:author_name, tag:tag_name, tags:tag1,tag2,..., exit to quit): ")
        command_parts = command.split(':')
        if len(command_parts) == 2:
            action = command_parts[0].strip()
            value = command_parts[1].strip()
            if action == "name":
                quotes = search_quotes_by_author(value)
            elif action == "tag":
                quotes = search_quotes_by_tag(value)
            elif action == "tags":
                quotes = search_quotes_by_tags(value)
            else:
                print("Invalid command. Please try again.")
                continue
            if quotes:
                print("Results:")
                for quote in quotes:
                    print(f"Quote: {quote.quote.encode('utf-8')}")
            else:
                print("Not found")
        elif command == "exit":
            sys.exit(0)
        else:
            print("Invalid command format. Please use the format action: value.")

if __name__ == "__main__":
    main()
