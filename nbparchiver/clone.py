import os
from pathlib import Path
from rss_parser import Parser
import requests
from jinja2 import Environment, FileSystemLoader
from podcast import Podcast, config

rss_url = 'https://nakedbiblepodcast.com/feed/podcast/'

response = requests.get(rss_url)

try:
    rss = Parser.parse(response.text)
except KeyError:
    print("Looks like you've been blocked. Come from a new IP and try again.")
    exit()
items = rss.channel.items
items.reverse()

playlist = ['#EXTM3U']

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
        p.dump()
    else:
        print("Loading from pickle...")
        p = Podcast.load(cache_file)
        print(p.title)
    p.save()
    podcasts.append(p)
    playlist.append(p.mp3.file_name)


tpls_dir = os.path.join(config['app_dir'], 'tpls')
environment = Environment(loader=FileSystemLoader(tpls_dir))
template = environment.get_template("index.tpl")
content = template.render(items=podcasts)

index_file = os.path.join(config['out_dir'], 'index.html')
with open(index_file, mode='w', encoding='utf-8') as f:
    f.write(content)

playlist_file = os.path.join(config['content_dir'], 'naked_bible_podcast.m3u')
with open(playlist_file, mode='w', encoding='utf-8') as f:
    playlist_content = '\n'.join(playlist)
    f.write(playlist_content)
