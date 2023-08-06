import os
import shutil
from urllib.parse import urlparse

import requests

"""
module for general http utils
"""


def validate_url(url):
    result = urlparse(url)
    if not all([result.scheme, result.netloc, result.path]):
        raise Exception(f'{url} is not a valid url')


def download_file(url, dest, is_https=True, delete_file_if_exists=True):
    """
    download file to local
    :param url:
    :param dest:
    :param is_https:
    :param delete_file_if_exists:
    :return:
    """
    validate_url(url)

    local_filename = os.path.join(dest, url.split('/')[-1])
    if delete_file_if_exists and os.path.isfile(local_filename):
        os.remove(local_filename)
    if is_https:
        r = requests.get(url, stream=True, verify=False)
    else:
        r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        shutil.copyfileobj(r.raw, f)
    return local_filename
