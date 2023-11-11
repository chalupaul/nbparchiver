import os
from pathlib import Path
from rss_parser import Parser
import requests
from jinja2 import Environment, FileSystemLoader
from podcast import Podcast, config

rss_url = 'https://nakedbiblepodcast.com/feed/podcast/'

response = requests.get(rss_url)

rss = Parser.parse(response.text)
items = rss.channel.items
items.reverse()

for k in config.keys():
    if k.startswith('_'):
        continue
    Path(config[k]).mkdir(parents=True, exist_ok=True)

podcasts = []
for item in items:
    checksum = Podcast.get_hash(item)
    cache_file = os.path.join(config['cache_dir'], checksum)
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


tpls_dir = os.path.join(config['app_dir'], 'tpls')
environment = Environment(loader=FileSystemLoader(tpls_dir))
template = environment.get_template("index.tpl")
content = template.render(items=podcasts)

index_file = os.path.join(config['out_dir'], 'index.html')
with open(index_file, mode='w', encoding='utf-8') as f:
    f.write(content)

