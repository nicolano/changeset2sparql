from posixpath import dirname
from urllib.parse import urlparse
from urllib.request import urlopen
import validators.url

from bs4 import BeautifulSoup

CHANGESETS_FOLDER_FILE_EXTENSION = ".osm.gz"


def get_all_numeric_directories(url: str) -> list[str]:
    """
    Returns a list of all directories at the url, that have a numeric name, e.g. '001', '232', ...
    """
    page = urlopen(url)
    html = page.read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    dirs: list[str] = []
    for a in soup.find_all('a', href=True):
        dir_name = dirname(urlparse(a['href']).path)
        if dir_name and dir_name != '/' and dir_name.isnumeric():
            dirs.append(dir_name)

    return dirs


def get_all_numeric_file_names(url: str) -> list[str]:
    """
    Returns a list of all files at the url, with the extension '.osm.gz',
    that have a numeric name, e.g. '001', '232', ...
    """
    page = urlopen(url)
    html = page.read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    files: list[str] = []
    for a in soup.find_all('a', href=True):
        dir_name = urlparse(a['href']).path
        if dir_name and dir_name != '/' and dir_name.endswith(CHANGESETS_FOLDER_FILE_EXTENSION):
            files.append(dir_name)

    return files


def url_builder(base_url: str, components: [str]) -> str:
    """
    Concatenates the passed components to the base_url and returns it.
    :raises ValidationException: The url is invalid.
    """
    url = base_url
    for component in components:
        url = url + '/' + component

    if not validators.url(url):
        raise ValidationError(message=f'Invalid URL: {url}')

    return url


class ValidationError(Exception):
    def __init__(self, message):
        super().__init__(message)