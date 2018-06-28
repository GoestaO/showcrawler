from pathlib import Path
import yaml
import pysftp
from ftplib import FTP
import os
from guessit import guessit
from bs4 import BeautifulSoup
import requests


CURRENT_FOLDER = os.path.dirname(os.path.realpath(__file__))
WATCH_FOLDER = CURRENT_FOLDER + "/folderwatch"
CONFIG_FILE = CURRENT_FOLDER + "/config.yml"
FTP_CONFIG = CURRENT_FOLDER + "/ftp.yml"
DB_FILENAME = CURRENT_FOLDER + '/downloads.db'


def generate_absolute_path_mediaserver(folder):
    rootfolder = "/share/Web/temp/"
    return "{}{}".format(rootfolder, folder)


def generate_download_folder(folder):
    rootfolder = "/temp/"
    return "{}{}".format(rootfolder, folder)


def create_crawljob_and_upload(jobname: str, link: str, download_folder):
    with open("{}/{}.crawljob".format(WATCH_FOLDER, jobname), "w") as f:
        f.write("text = {}\n".format(link))
        f.write("downloadFolder = {}\n".format(download_folder))
        f.write("enabled = TRUE\n")
        f.write("autoStart = TRUE\n")
        f.write("forcedStart = TRUE\n")
        f.write("autoConfirm = TRUE\n")
        f.close()
    push_file_to_ftp(f)


def read_config(path_to_file: str):
    with open(path_to_file, 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            return None


def push_file_to_ftp(file):
    connection = read_config(FTP_CONFIG).get('ftp_connection')
    username = connection.get('username')
    f = open(file.name, 'rb')
    filename = os.path.basename(file.name)
    ftp = FTP(user=username, passwd=connection.get('password'))
    ftp.connect(host=connection.get('host'), port=connection.get('port'))
    ftp.cwd(connection.get('folderwatch'))
    ftp.storbinary('STOR ' + filename, f)
    f.close()
    ftp.quit()


def push_files_to_ftp(folder: str, filelist: list):
    connection = read_config(FTP_CONFIG)
    srv = pysftp.Connection(host = connection.get('host'), username=connection.get('username'), password=connection.get('password'))
    with srv.cd(folder):  # chdir to public
        for file in filelist:
            srv.put(file)  # upload file to nodejs/

    # Closes the connection
    srv.close()


def log_download(name: str):
    with open("history.txt", "a") as f:
        f.write(name + "\n")


def get_show_information(title):
    return guessit(title)


# Creates a beautifulsoup object for an url
def beautiful_soup(raw_url):
    page = requests.get(raw_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


if __name__ == "__main__":
    print(CONFIG_FILE)

