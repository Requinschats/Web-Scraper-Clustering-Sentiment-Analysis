# https://github.com/x4nth055/pythoncode-tutorials/blob/master/web-scraping/link-extractor/link_extractor.py
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


def get_all_website_links(url):
    urls = set()
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            continue
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid_url(href):
            continue
        if href in internal_urls:
            continue
        if domain_name not in href:
            if href not in external_urls:
                print(f"{GRAY}[!] External link: {href}{RESET}")
                external_urls.add(href)
            continue
        print(f"{GREEN}[*] Internal link: {href}{RESET}")
        urls.add(href)
        internal_urls.add(href)
    return urls


def crawl(url, max_urls=30):
    global total_urls_visited
    total_urls_visited += 1
    print(f"{YELLOW}[*] Crawling: {url}{RESET}")
    links = get_all_website_links(url)
    for link in links:
        if total_urls_visited > max_urls:
            break
        crawl(link, max_urls=max_urls)


def link_crawler(url, max_url_count):
    max_urls = max_url_count
    crawl(url, max_urls=max_urls)

    output_link_crawler_statistics(internal_urls, external_urls, max_urls)
    domain_name = urlparse(url).netloc

    with open(f"{domain_name}_internal_links.txt", "w") as f:
        for internal_link in internal_urls:
            print(internal_link.strip(), file=f)

    with open(f"{domain_name}_external_links.txt", "w") as f:
        for external_link in external_urls:
            print(external_link.strip(), file=f)

    return internal_urls


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Link Extractor Tool with Python")
    parser.add_argument("-url", help="The URL to extract links from.")
    parser.add_argument("-m", "--max-urls", help="Number of max URLs to crawl, default is 30.",
                        default=30, type=int)
    args = parser.parse_args()
    link_crawler(args.url, args.max_urls)
