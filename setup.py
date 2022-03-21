import asyncio
import json
import random

import requests
from lxml import etree


def read_input_file():
    """ Read the file input.json and returns its values

    :return: List of keywords, list of proxies and type
    """
    with open('input.json') as input_file:
        input_json = json.loads(''.join(input_file.readlines()))
        return input_json.get('keywords'), input_json.get('proxies'), input_json.get('type').lower()


def write_output_file(json_str):
    """ Write the result into the output.json file

    :param json_str: String with the json results
    """
    with open('output.json', 'w') as output_file:
        output_file.write(json_str)


def request_url_and_parse_to_xml(url, proxy_list):
    """ Perform a GET request with a random proxy from the list and return the HTML parsed in a XML

    :param url: Url to request
    :param proxy_list: List of proxies
    :return: XML of the HTML
    """
    r = requests.get(url, proxies=get_proxy_map(proxy_list))
    return etree.fromstring(r.content, parser=etree.HTMLParser())


def get_proxy_map(proxy_list):
    """ Get a random proxy form the list

    :param proxy_list: List of proxies
    :return: Proxy map for requests library
    """
    return {'https': 'https://{}'.format(random.choice(proxy_list))} if proxy_list else None


async def extract_data(url, owner, proxy_list):
    """ Perform a GET request to obtain the repository main page, extract the language info and return the result

    :param url: Repository url
    :param owner: Owner name
    :param proxy_list: List of proxies
    :return: Map with the results
    """
    xml_content = request_url_and_parse_to_xml(url, proxy_list)

    languages = dict()
    for language_node in xml_content.xpath('//div[@class="Layout-sidebar"]/div/div[last()]/div/ul/li/a'):
        languages[language_node.xpath('./span[1]/text()')[0]] = language_node.xpath('./span[2]/text()')[0]

    return create_result_node(url, owner, languages)


def create_result_node(url, owner, language_stats):
    """ Create a map with the results

    :param url: Repository url
    :param owner: Owner name
    :param language_stats: Language info dict
    :return: Map with the results
    """
    return {
        "url": url,
        "extra": {
            "owner": owner,
            "language_stats": language_stats
        }
    }


if __name__ == '__main__':
    keywords, proxies, search_type = read_input_file()

    if search_type != 'repositories':
        print('Type "{}" not supported.'.format(search_type))
        exit()

    search_url = 'https://github.com/search?q={}&type={}'.format('+'.join(keywords), search_type)
    xml = request_url_and_parse_to_xml(search_url, proxies)

    loop = asyncio.get_event_loop()

    tasks = list()
    for repository_node in xml.xpath('//ul[@class="repo-list"]/li'):
        href = repository_node.xpath('./div[2]/div[1]/div/a/@href')[0]
        owner_name = href[1: href.rfind('/')]

        repo_url = "https://github.com{}".format(href)

        tasks.append(loop.create_task(extract_data(repo_url, owner_name, proxies)))

    loop.run_until_complete(asyncio.wait(tasks))
    results = loop.run_until_complete(asyncio.gather(*tasks))

    write_output_file(json.dumps(results, indent=4))
