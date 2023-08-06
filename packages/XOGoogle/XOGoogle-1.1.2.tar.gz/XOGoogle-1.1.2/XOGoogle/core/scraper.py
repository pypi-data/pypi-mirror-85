#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import datetime
import requests
from bs4 import BeautifulSoup

from XOGoogle.core.settings import USER_AGENT


def scrape_google(cve: str, base_url="https://www.google.com/search?q=", start_page=1, page=1, crawl=False) -> dict:
    start = (start_page - 1) * 10
    query = cve.replace(' ', '+')
    search_results = []
    for page_no in range(start, start + (page * 10), 10):
        headers = {"user-agent": USER_AGENT}
        URL = base_url + '{}'.format(query) + '&start={}'.format(page_no)
        resp = requests.get(URL, headers=headers)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, "html.parser")
            for div in soup.findAll('div', {'class': 'g'}):
                search_result = {}
                try:
                    link = div.find(
                        'div', {'class': 'rc'}).find('a')['href']
                    if link:
                        search_result['link'] = link
                    title = div.find(
                        'div', {'class': 'rc'}).find('h3').text
                    if title:
                        search_result['title'] = title
                    breadcrumb = div.find('cite').text
                    if breadcrumb:
                        search_result['breadcrumb'] = breadcrumb
                    desc = div.find('div', {'class': 'rc'}).find(
                        'span', {'class': 'st'})
                    if desc:
                        short_desc = desc.text.replace('\xa0', '').replace('...', '')
                    else:
                        short_desc = None
                    try:
                        date_span = div.find('div', {'class': 'rc'}).find(
                            'span', {'class': 'f'})
                    except:
                        date_span = None
                except Exception as e:
                    continue
                if crawl:
                    try:
                        page_resp = requests.get(
                            search_result['link'], timeout=5)
                        if page_resp.status_code == 200:
                            page_soup = BeautifulSoup(
                                page_resp.text, "html.parser")                                    
                            [x.decompose() for x in page_soup.findAll('script')]
                            [x.decompose() for x in page_soup.findAll('footer')]
                            [x.decompose() for x in page_soup.findAll('header')]
                            [x.decompose() for x in page_soup.findAll('option')]
                            [x.decompose() for x in page_soup.findAll('style')]
                            [x.decompose() for x in page_soup.findAll('a')]
                            [x.decompose() for x in page_soup.findAll('iframe')]
                            [x.decompose() for x in page_soup.findAll('img')]
                            [x.decompose() for x in page_soup.findAll('input')]
                            [x.decompose() for x in page_soup.findAll('label')]
                            [x.decompose() for x in page_soup.findAll('button')]
                            [x.decompose() for x in page_soup.findAll('form')]
                            [x.decompose() for x in page_soup.findAll('aside')]
                            [x.decompose() for x in page_soup.findAll('code')]
                            [x.decompose() for x in page_soup.findAll('noscript')]
                            [x.decompose() for x in page_soup.findAll('ins')]                            
                            page_data = re.sub('\s{2,}|\n',' ',page_soup.find('body').get_text(separator="\n", strip=True))
                        else:
                            page_data = 'Not Avail'
                    except:
                        page_data = 'Not Avail'
                    search_result['page_data'] = page_data
                if date_span:
                    date_span_text = date_span.text.replace(' - ', '')
                    try:
                        date_span = datetime.datetime.strptime(
                            date_span_text, "%b %d, %Y").date()
                    except:
                        date_span = None
                else:
                    date_span = None
                if short_desc:
                    search_result['short_desc'] = short_desc.replace(
                    date_span_text + ' - ', '')
                else:
                    search_result['short_desc'] = short_desc
                search_result['date'] = date_span
                search_result['page'] = (page_no / 10) + 1
                search_results.append(search_result)
    results = {'ID': cve, 'gsearch_results': search_results}
    return results
