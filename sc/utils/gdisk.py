import errno
import os

import requests

__all__ = ["gdfile_from_spec"]

URL = "https://docs.google.com/uc?export=download"
CHUNK_SIZE = 32768
NAME2ID = {"amorph-server.jar": "0B6udzTbX1EFPcXFQRGF2NGZUMk0"}
VALID_NAMES = tuple(NAME2ID.keys())


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None


def save_response_content(response, destination):
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


def download_file_from_google_drive(id_, destination):
    session = requests.Session()
    response = session.get(URL, params={'id': id_}, stream=True)
    token = get_confirm_token(response)
    if token:
        params = {'id': id_, 'confirm': token}
        response = session.get(URL, params=params, stream=True)
    save_response_content(response, destination)


def gdfile_from_spec(name):
    dst_path = f"data/{name}"
    if not os.path.exists(dst_path):
        download_file_from_google_drive(NAME2ID[name], dst_path)
    return dst_path
