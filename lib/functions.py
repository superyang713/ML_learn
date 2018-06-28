import os
import tarfile
import requests
import logbook
import sys
import pandas as pd


logbook.StreamHandler(sys.stdout, level=logbook.TRACE).push_application()
log = logbook.Logger('Log')


def fetch_data(url, dir_path):
    if not os.path.isdir(dir_path):
        log.trace(f"Folder does not exist. Creating folder...")
        os.makedirs(dir_path)
        log.trace(f"Folder successfully created {os.path.abspath(dir_path)}")
    tgz_path = os.path.join(dir_path, 'housing.tgz')
    download(url, tgz_path)
    try:
        with tarfile.open(tgz_path) as tar:
            tar.extractall(path=dir_path)
            log.trace('Data file has been successfully extracted.')
    except tarfile.ReadError:
        log.warn('Tar file is corrupted.')


def download(url, filepath):
    try:
        r = requests.get(url)
        r.raise_for_status()
        with open(filepath, "wb") as f:
            f.write(r.content)
        log.trace('Data file downloaded successfully')
    except requests.exceptions.HTTPError:
        log.warn('Bad url')


def load_data(dirpath, filename):
    filepath = os.path.join(dirpath, filename)
    return pd.read_csv(filepath)
