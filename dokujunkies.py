import feedparser
from utilities import create_crawljob_and_upload, document_download, is_in_download_history, beautiful_soup
from utilities import read_config
config = read_config(path_to_file="config.yml").get('Dokujunkies_Geschichtepolitik')


def get_raw_urls():
    """ Returns a list of tuples. A tuple contains the link and the title of a documentary that should be downloaded."""
    linklist = []
    feed_url = config.get('feed')
    d = feedparser.parse(feed_url)
    for entry in d['entries']:
        if not is_blacklisted(entry):
            link = entry['link']
            title = entry['title'].split(" – ")[0] if len(entry['title'].split(" – ")[0]) > 0 else 'title'
            if not is_in_download_history(title):
                linklist.append((link, title))
    return linklist


def is_blacklisted(entry):
    blacklist = config.get('blacklist')
    for tag in entry['tags']:
        if tag['term'] in blacklist:
            return True
    return False


def get_download_link(soup):
    quality = config.get('quality')
    hoster = config.get('hoster')
    paragraphs = soup.findAll('p')
    for p in paragraphs:
        if quality in p.text and hoster in p.text:
            downloadable_links = p.findAll('a')
            for dl in downloadable_links:
                if hoster in dl.next_sibling:
                    return dl['href']





if __name__ == '__main__':
    raw_urls = get_raw_urls()
    for raw_url in raw_urls:
        soup = beautiful_soup(raw_url[0])
        downloadable_link = get_download_link(soup)
        download_folder = config.get('downloadfolder')
        title = raw_url[1]
        create_crawljob_and_upload(jobname=title, link=downloadable_link, download_folder=download_folder)
        document_download(title)
