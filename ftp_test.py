from ftplib import FTP
from utilities import read_config
import os

if __name__ == '__main__':
    connection = read_config("ftp.yml").get('ftp_connection')
    file = open('/home/goesta/PycharmProjects/showcrawler/HouseHuntersRenovation.crawljob', 'rb') # file to send
    filename = os.path.basename(file.name)
    username = connection.get('username')
    ftp = FTP(host=connection.get('host'), user=username, passwd=connection.get('password'))
    ftp.cwd(connection.get('folderwatch'))
    ftp.storbinary("STOR " + filename, file)
    file.close()
    ftp.quit()

