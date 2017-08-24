"""Stuff related to dealing with google dist external files."""

import errno
import logging
import os

import requests

__all__ = ["NAMES", "download_file"]

logger = logging.getLogger(__name__)

_URL = "https://docs.google.com/uc?export=download"
_CHUNK_SIZE = 32768
_NAME_TO_ID = {
    "amorph-server.jar": "0B6udzTbX1EFPcXFQRGF2NGZUMk0"
}
NAMES = list(_NAME_TO_ID.keys())
"""List of avialible names."""


def _get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None


def _save_response_content(response, destination):
    if not os.path.exists(os.path.dirname(destination)):
        try:
            os.makedirs(os.path.dirname(destination))
        except OSError as error:
            if error.errno != errno.EEXIST:
                raise
    with open(destination, "wb") as file:
        for chunk in response.iter_content(_CHUNK_SIZE):
            if chunk:
                file.write(chunk)


def _download_file_from_google_drive(id_, destination):
    session = requests.Session()
    response = session.get(_URL, params={'id': id_}, stream=True)
    token = _get_confirm_token(response)
    if token:
        params = {'id': id_, 'confirm': token}
        response = session.get(_URL, params=params, stream=True)
    _save_response_content(response, destination)


def download_file(name):
    """Download file with name, output local path."""
    dst_path = "data/{}".format(name)
    if not os.path.exists(dst_path):
        logger.info("download file %s from gdisk, saving to %s",
                    name, dst_path)
        _download_file_from_google_drive(_NAME_TO_ID[name], dst_path)
    logger.info("the file is on %s", dst_path)
    return dst_path
