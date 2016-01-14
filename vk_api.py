import requests
from bs4 import BeautifulSoup
import logging
import re


class VKErrorException(Exception):
    pass


def url_to_post_text_converter(url):
    assert type(url) == str
    response = requests.get(url)
    if not response.ok or not response.text:
        logging.error("problem with url: " + url)
        raise VKErrorException
    soup = BeautifulSoup(response.text, 'html.parser')
    post_text = soup.find("div", attrs={'class': "wi_body"})
    post_text = soup.find("div", attrs={'class': 'pi_text'})
    post_text = str(post_text).replace("<br/>", "\n")
    post_text = BeautifulSoup(post_text, "html.parser").text
    return post_text


def simplify_vk_url(url):
    """
    >>> simplify_vk_url("https://vk.com/wall-12648877_1663646?z=photo-12648877_393811825%2Falbum-12648877_00%2Frev")
    'https://vk.com/wall-12648877_1663646'
    >>> simplify_vk_url("https://vk.com/beginenglish_ru?w=wall-12648877_1663646")
    'https://vk.com/wall-12648877_1663646'
    >>> simplify_vk_url("https://vk.com/wall-12648877_1663646")
    'https://vk.com/wall-12648877_1663646'

    :param url:
    :return str:
    """
    suffix = re.findall("wall-\d+_\d+", url)[0]
    return "https://m.vk.com/" + suffix


if __name__ == "__main__":
    # req = 'https://vk.com/wall-12648877_1677895'
    req = 'https://vk.com/wall-12648877_1663646'
    req = 'https://vk.com/wall-12648877_1226405'
    print(url_to_post_text_converter(req))
    print( simplify_vk_url(req))