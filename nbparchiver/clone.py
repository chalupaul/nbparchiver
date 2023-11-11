import os
from pathlib import Path
from rss_parser import Parser
import requests
from jinja2 import Environment, FileSystemLoader
from podcast import Podcast
import pickle

rss_url = 'https://nakedbiblepodcast.com/feed/podcast/'

response = requests.get(rss_url)

rss = Parser.parse(response.text)
items = rss.channel.items
items.reverse()


cwd = os.path.dirname(os.path.realpath(__file__))
cache_dir = os.path.join(cwd, 'cache')
Path(cache_dir).mkdir(parents=True, exist_ok=True)


podcasts = []
for item in items:
    checksum = Podcast.get_hash(item)
    cache_file = os.path.join(cache_dir, checksum)
    if not os.path.exists(cache_file):
        p = Podcast(item)
        p.save()
        p.dump()
    else:
        print("Loading from pickle...")
        p = Podcast.load(cache_file)
        print(p.title)
    podcasts.append(p)
    break


tpls_dir = os.path.join(cwd, 'tpls')
environment = Environment(loader=FileSystemLoader(tpls_dir))
template = environment.get_template("index.tpl")
content = template.render(items=podcasts)

with open('index.html', mode='w', encoding='utf-8') as f:
    f.write(content)

