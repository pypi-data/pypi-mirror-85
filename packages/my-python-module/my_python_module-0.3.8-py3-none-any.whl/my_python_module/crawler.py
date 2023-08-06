#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re
import logging
import os

import requests
from bs4 import BeautifulSoup, SoupStrainer

from urllib.parse import urlsplit, urljoin, urldefrag

logger = logging.getLogger(__name__)


def is_relative_url(url):
    """
    is the url is a relative url (including the `/what` )
    """
    s = urlsplit(url)
    if not s.scheme:
        return True
    else:
        return False


def to_absolute_url(baseurl, url):
    """
    input the baseurl and the target url, no matter it's a relative url,
    will return a absolute url
    """
    if not is_relative_url(url):
        return url
    else:
        return urljoin(baseurl, url)


def remove_url_fragment(url):
    """
    remove the target url fragment like `#sec1` and the parameters on url will
    keeped still.
    """
    defragmented, frag = urldefrag(url)
    return defragmented


REPATTEN_URL = re.compile(
    r'https?:\/\/[\da-z\.-]+\.[a-z\.]{2,6}[\/\w\.-]*[\?\w=&#]*')


def parse_urls(text):
    """
    input a text , and return all url we found that based on the re-expression
    of `REPATTEN_URL` . which is not recommend , recommed use the `wget_links` function.
    """
    return re.findall(REPATTEN_URL, text)


def parse_webpage_links(url, html, name='a', id="", class_="", **kwargs):
    """
    :param url: 目标网页的url（或者该网站的base url也是可以的）
    :param html: 目标网页的text内容

    input html content, and use the beautifulsoup parse it, get all the
    <a href="link"> and return the link.

    we will do the extrawork: to_absolute_url and remove_url_fragment.

    sometime you may want the specific  <a href="link"> which is in where id
    or where class etc.

    you can set `name="div" id="what"'` to narrow the url target into the SoupStrainer for the first filter, so you can specific which url you want to collect.

    this function will return a set of links.

    """

    parse_kwargs = {'name': name}
    if id:
        parse_kwargs['id'] = id
    if class_:
        parse_kwargs['class_'] = class_

    if html:
        soup = BeautifulSoup(
            html, 'lxml', parse_only=SoupStrainer(**parse_kwargs))
    else:
        return set()

    links = [link.get('href') for link in soup.find_all('a', href=True)]
    links = [to_absolute_url(url, link) for link in links]
    links = [remove_url_fragment(link) for link in links]
    return set(links)


def parse_webpage_images(url, html, name="img", id="", class_="", **kwargs):
    """
    :param url: 目标网页的url（或者该网站的base url也是可以的）
    :param html: 目标网页的text内容

    input a html content , and use the beautifulsoup parse it, get all the
    <img src="link"> and return the link.

    we will do the extrawork: to_absolute_url.

    sometime you may want the specific  <img src="link"> which is in where id
    or where class etc.

    you can set `name="div" id="what"'` to narrow the url target into the SoupStrainer for the first filter, so you can specific which url you want to collect.

    this function will return a set of image links.

    """

    parse_kwargs = {'name': name}
    if id:
        parse_kwargs['id'] = id
    if class_:
        parse_kwargs['class_'] = class_

    if html:
        soup = BeautifulSoup(
            html, 'lxml', parse_only=SoupStrainer(**parse_kwargs))
    else:
        return set()

    links = [link.get('src') for link in soup.find_all('img', src=True)]
    links = [to_absolute_url(url, link) for link in links]
    return set(links)


def download(url, filename, download_timeout=30, override=False, **kwargs):
    """
    High level function, which downloads URL into tmp file in current
    directory and then renames it to filename autodetected from either URL
    or HTTP headers.
    :param out: output filename or directory
    :return:    filename where URL is downloaded to
    """
    logger.info(f'start downloading file {url} to {filename}')
    import time  # https://github.com/kennethreitz/requests/issues/1803
    start = time.time()

    if os.path.exists(filename):
        if override:
            logger.info(f'{filename} exist. but i will override it.')
        else:
            logger.info(f'{filename} exist.')
            return

    content = requests.get(url, stream=True, **kwargs)

    with open(filename, 'wb') as f:
        for chunk in content.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
            if time.time() - start > download_timeout:
                content.close()
                os.unlink(filename)
                logger.warning('{0} download failed'.format(filename))
                return False

    return filename


def is_url_insite(url, baseurl):
    """
    is the url in site. the second argument `baseurl` is a normal url insite is ok. the jugement is based on netloc.
    """
    p = urlsplit(url)
    if p.netloc == urlsplit(baseurl).netloc:
        return True
    else:
        return False


def is_url_belong(url, baseurl):
    """
    is the url belong to the baseurl.
    the check logic is strict string match.
    """
    if url.startswith(baseurl):
        return True
    else:
        return False
