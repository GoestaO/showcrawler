# -*- coding: utf-8 -*-

import feedparser
import pprint
from utilities import create_crawljob_and_upload, read_config, get_show_information
from db import persist_download, download_exists
from pathlib import Path
from guessit import guessit
from utilities import CURRENT_FOLDER, WATCH_FOLDER, CONFIG_FILE, FTP_CONFIG, DB_FILENAME, DB_FILENAME

home = str(Path.home())
WATCHED_FOLDER = "folderwatch"

config = read_config(path_to_file=CONFIG_FILE).get('RMZ_Shows')


# Checks, if
def filter_relevant_show_info(show_info):
    if 'title' in show_info and 'season' in show_info and 'episode' in show_info and 'screen_size' in show_info:
        title = show_info['title']
        season = show_info['season']
        episode = show_info['episode']
        screen_size = show_info['screen_size']
    return title, season, episode, screen_size


def filter_for_shows(entries, shows):
    prefiltered_shows = list(filter(lambda x: x in entries, shows))
    return prefiltered_shows




if __name__ == '__main__':
    d = feedparser.parse('http://rmz.cr/feed')
    download_folder = config.get('downloadfolder')
    quality = config.get('quality')
    shows = config.get('shows')

    # Iterate through the entries and fetch the title and link, which is the relevant data
    for entry in d['entries']:
        for show in shows:
            raw_title = entry['title']
            link = entry['link']

            # Fetch show infos from the guessit library
            show_info = get_show_information(raw_title)

            # Check, if show_info contains the keys 'title', 'episode' and 'screen_size' to avoid KeyErrors
            if 'title' in show_info and 'season' in show_info and 'episode' in show_info and 'screen_size' in show_info:
                title = show_info['title']
                season = show_info['season']
                episode = show_info['episode']
                screen_size = show_info['screen_size']

                if show == title and quality == screen_size and not download_exists(title=title, season=season,
                                                                                    episode=episode):
                    # create crawljob and upload to server
                    create_crawljob_and_upload(jobname=show, link=link, download_folder=download_folder)

                    print("create crawljob for " + title)
                    # save download to avoid multiple downloads of the same file
                    persist_download(title=title, season=season, episode=episode)
