import os
import inspect
from pathlib import Path
import pickle
import requests
import hashlib

from bs4 import BeautifulSoup

class Empty(object):
    def __init__(self):
        self.content = None
        self.attributes = {'url': None}

class LocalFile(object):
    url: str
    file_name: str
    loc: str
    local: str
    
    def __init__(self, url):
        output_dir = os.path.join('out', 'content')
        self.url = url
        self.file_name = url.split('/')[-1]
        cwd = os.path.dirname(os.path.realpath(__file__))
        parent = os.path.dirname(cwd)
        self.local = os.path.join(output_dir, self.file_name)
        self.loc = os.path.join(parent, self.local)
        

    def __str__(self):
        return f"{self.file_name}: {self.url}, {self.loc}"
    
    def __repr__(self):
        return self.local
    
    def save(self):
        if os.path.exists(self.loc):
            return
        print(f"fetching {self.url}...")
        r = requests.get(self.url)
        with open(self.loc, 'wb') as outfile:
            outfile.write(r.content)
        

class Podcast(object):
    pub_date: str
    description: str
    mp3: LocalFile
    transcript: LocalFile
    guid_url: str
    link: str
    title: str

    @staticmethod
    def __retrieve(field, data):
        value = getattr(data, field)
        if value is None:
            return Empty()
        return value
    
    @staticmethod
    def get_guid_url(data):
        return Podcast.__retrieve('guid', data).content
    
    @staticmethod
    def get_hash(data):
        url = Podcast.get_guid_url(data).encode('utf-8')
        hash = hashlib.md5(url).hexdigest()
        return hash

    @staticmethod
    def get_transcript_from_url(podcast_url):
        raw_html = requests.get(podcast_url).text
        soup = BeautifulSoup(raw_html, 'html.parser')
        divs = soup.find_all('div', {'class': 'podcast_meta'})
        links = []
        for d in divs:
            ls = d.find_all('a', href=True)
            for l in ls:
                if l is None or l['href'].find('.pdf') == -1:
                    continue
                links.append(l['href'])
        return LocalFile(links[0])
    
    def dump(self):
        cache_file = os.path.join(self.cache_dir, self.hash)
        with open(cache_file, mode='wb') as f:
            pickle.dump(self, f)

    @staticmethod  
    def load(cache_file):
        with open(cache_file, mode='rb') as f:
            p = pickle.load(f)
            return p

    def __init__(self, data):
        self.pub_date = self.__retrieve('pub_date', data).content
        self.description = self.__retrieve('description', data).content
        self.guid_url = Podcast.get_guid_url(data)
        self.link = self.__retrieve('link', data).content
        self.title = self.__retrieve('title', data).content

        mp3_url = self.__retrieve('enclosure', data).attributes['url']
        self.mp3 = LocalFile(mp3_url)
        self.transcript = Podcast.get_transcript_from_url(self.link)

        self.hash = Podcast.get_hash(data)
        self.cwd = os.path.dirname(os.path.realpath(__file__))
        self.cache_dir = os.path.join(self.cwd, 'cache')
        Path(self.cache_dir).mkdir(parents=True, exist_ok=True)

        self.content_dir = os.path.join(self.cwd, 'out', 'content')
        Path(self.content_dir).mkdir(parents=True, exist_ok=True)

    def save(self):
        self.mp3.save()
        self.transcript.save()

    def to_json(self):
        members = dict(inspect.getmembers(self))
        keys = members['__annotations__'].keys()
        return {k: getattr(self, k) for k in keys}
