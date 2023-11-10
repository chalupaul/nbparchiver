import os
from rss_parser import Parser
import requests
from jinja2 import Environment, FileSystemLoader
from podcast import Podcast

rss_url = 'https://nakedbiblepodcast.com/feed/podcast/'

response = requests.get(rss_url)

rss = Parser.parse(response.text)
items = rss.channel.items
items.reverse()

podcasts = []
for item in items:
    p = Podcast(item)
    podcasts.append(p)
    break

cwd = os.path.dirname(os.path.realpath(__file__))
tpls_dir = os.path.join(cwd, 'tpls')
environment = Environment(loader=FileSystemLoader(tpls_dir))
template = environment.get_template("index.tpl")
content = template.render(items=podcasts)

with open('index.html', mode='w', encoding='utf-8') as f:
    f.write(content)


#print(podcasts[-1].to_json())
#podcasts[-1].get_transcript()