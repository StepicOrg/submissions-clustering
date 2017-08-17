import errno
import os

import requests

__all__ = ["download_file"]

URL = "https://docs.google.com/uc?export=download"
CHUNK_SIZE = 32768
NAME2ID = {
    "amorph-server.jar": "0B6udzTbX1EFPcXFQRGF2NGZUMk0"
}


def _get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None


def _save_response_content(response, destination):
    if not os.path.exists(os.path.dirname(destination)):
        try:
            os.makedirs(os.path.dirname(destination))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:
                f.write(chunk)


def _download_file_from_google_drive(id_, destination):
    session = requests.Session()
    response = session.get(URL, params={'id': id_}, stream=True)
    token = _get_confirm_token(response)
    if token:
        params = {'id': id_, 'confirm': token}
        response = session.get(URL, params=params, stream=True)
    _save_response_content(response, destination)


def download_file(name):
    dst_path = "data/{}".format(name)
    if not os.path.exists(dst_path):
        _download_file_from_google_drive(NAME2ID[name], dst_path)
    return dst_path
