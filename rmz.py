import feedparser
import pprint
from utilities import create_crawljob_and_upload, read_config
from pathlib import Path
home = str(Path.home())
WATCHED_FOLDER = "{}/jd2/folderwatch".format(home)

config = read_config(path_to_file="config.yml").get('RMZ_Shows')



if __name__ == '__main__':
    d = feedparser.parse('http://rmz.cr/feed')
    download_folder = config.get('downloadfolder')
    quality = config.get('quality')
    shows = config.get('shows')
    for entry in d['entries']:
        for show in shows:
            title = entry['title']
            link = entry['link']
            if quality in title and show in title:
                create_crawljob_and_upload(jobname=show, link=link, download_folder=download_folder)


