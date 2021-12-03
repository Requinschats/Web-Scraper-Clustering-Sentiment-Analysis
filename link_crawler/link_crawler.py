# https://github.com/x4nth055/pythoncode-tutorials/blob/master/web-scraping/link-extractor/link_extractor.py
import os.path
from urllib.parse import urlparse, urljoin

import colorama
import requests
from bs4 import BeautifulSoup

from link_crawler.outputs import output_link_crawler_statistics

colorama.init()
GREEN, GRAY, RESET, YELLOW = colorama.Fore.GREEN, colorama.Fore.LIGHTBLACK_EX, colorama.Fore.RESET, colorama.Fore.YELLOW
internal_urls, external_urls = set(), set()
total_urls_visited = 0


def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def select_url_from_href(a_tag):
    return a_tag.attrs.get("href")


def select_is_url_valid_format(url):
    return ".html" in url


def select_is_valid_url(url, robots_parser):
    if not is_valid_url(url): return False
    if not select_is_url_valid_format(url): return False
    if url in internal_urls: return False
    if not robots_parser.can_fetch_url(url): return False
    return True


def select_formatted_url(current_page_url, url):
    url = urljoin(current_page_url, url)
    parsed_href = urlparse(url)
    return parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path


def get_all_website_links(current_page_url, robots_parser):
    urls = set()
    domain_name = urlparse(current_page_url).netloc
    soup = BeautifulSoup(requests.get(current_page_url).content, "html.parser")
    for a_tag in soup.findAll("a"):
        href = select_url_from_href(a_tag)
        if href == "" or href is None: continue

        href = select_formatted_url(current_page_url, href)
        if not select_is_valid_url(href, robots_parser): continue

        if domain_name not in href:
            if href not in external_urls:
                print(f"{GRAY}[!] External link: {href}{RESET}")
                external_urls.add(href)
            continue
        print(f"{GREEN}[*] Internal link: {href}{RESET}")

        urls.add(href)
        internal_urls.add(href)
    return urls


def crawl(url, max_urls=5, robots_parser=None):
    global total_urls_visited
    total_urls_visited += 1
    print(f"{YELLOW}[*] Crawling: {url}{RESET}")
    links = get_all_website_links(url, robots_parser)
    for link in links:
        if total_urls_visited > max_urls: break
        crawl(link, max_urls, robots_parser)


def are_links_already_fetched():
    return os.path.isfile("paths/www.concordia.ca_internal_links.txt")


def link_crawler(url, max_url_count, robots_parser):
    if are_links_already_fetched(): return

    max_urls = max_url_count
    crawl(url, max_urls, robots_parser)

    output_link_crawler_statistics(internal_urls, external_urls, max_urls)
    domain_name = urlparse(url).netloc

    path = "paths/"
    with open(path + domain_name + "_internal_links.txt", "w+") as f:
        for internal_link in internal_urls:
            print(internal_link.strip(), file=f)

    with open(path + domain_name + "_external_links.txt", "w+") as f:
        for external_link in external_urls:
            print(external_link.strip(), file=f)

    return internal_urls
