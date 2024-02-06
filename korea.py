#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
import requests
import time
from utils import send_message, construct_links_message

KOREAN_CAR_MODELS = {"Kia": "Morning"}
BASE_URL = "https://www.autowini.com"


def get_url(make, model, min_year, max_price):
    make = make.strip().replace(' ', '+')
    model = model.strip().replace(' ', '+')
    search_term = make + '-' + model
    url = f'{BASE_URL}/Cars/{search_term}/car-search?i_sIndexVal=bq&i_sSearchType=quick&i_sStartYear={min_year}&i_sPriceTo={max_price}&i_iPageSize=40&i_sFlagGuaranteeYn=Y'
    return url


def get_autowini_webpage(url):
    try:
        cookies = {
            'COUNTRY_INFO': '"{\\"country_code\\":\\"CA\\",\\"country_nm\\":\\"Canada\\",\\"country_subCode\\":\\"C0310\\",\\"country_location\\":\\"C190\\"}"',
            'PROPERTY_LANGUAGE': 'en',
            'SESSION': '4ff88637-1d7d-418a-b4bc-8750eec4b39e',
            '_ga': 'GA1.2.1202513680.1655476109',
            '_gid': 'GA1.2.812999875.1655476109',
            '__utma': '28333612.1202513680.1655476109.1655476109.1655476109.1',
            '__utmc': '28333612',
            '__utmz': '28333612.1655476109.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
            '__utmt': '1',
            '__utmb': '28333612.1.10.1655476109',
            '_gcl_au': '1.1.989034764.1655476109',
            '_fbp': 'fb.1.1655476108958.893622438',
            'bm_mi': 'B4881C403A6019E391F4E2690B70DAAC~YAAQTKfcF7lGgyqBAQAAoL8QchDqSTkKHtX3SBEgDNwl00vJh5BzK/6SkcJwd5TSI+GSh1FbL3IiPBuLBmf87AYIL3xeDtSjdoCXEg9IoQWmTSYzmTPTAGQRvVMtDZyStjBvG+mw1r20B2kRGSSLSvhXWaL0iJk1voTwiV3OXc9B6tKta2Tral34JrFb/V0pma8xJCFbAQHpJPpLBwqbOtqsUPIjgvSeO1u/lcopcKCA5ocGffEhsJ13mZMkD1drxbFQTUubXFmWMHJ243lauUeM3ycxGAlJrdlFyWSJCY8696DXhxSLwerGACmj4LgdZx/W1wh0P2kjbSGqOa5VkyKlqrExatGaECI=~1',
            'ak_bmsc': 'CC8E5F3D4718F953C15B4570714A9A45~000000000000000000000000000000~YAAQTKfcF7xGgyqBAQAAv8AQchBO5BDkPIBBmz4p/dl2xMsFJQGvhGMO0WNNquYkW33MoiFuLZexfNf0fW9Oc0tPxO6+LR5LwzVr81iZTebFfcGXol/upj4hnqEAqZlHeRTQpUD6GqccNV+NfUBCPOlGYXe96aoiyZEIg/Uq7aNq13NcmoTEwZTsDCVYxRsf2xF9yu8TkZNUH+1ZX58cOBY4U+E1p4kCTz0SDVCc+u0wZUFGVQUfeOof2BwnC6PydU8re20KRD1/uS/iDbrMCGnlA9TZwgL9LJS2M/o25RqPF8hm27qdzn4JRsTrpWH8RO32HBuAB3+bS/h5t+WTmXWnOcnPXbvFN7eqoQgOcEC/7tM4SbseKEcp2zBoAXbmrFBa73jJj7HbnhfVs3bgwg4D49uOXBoPPrB8a9f7vk2O83aeFEs4GFnU1+dIpS1025dduS+jM2cFU8QtCUH7fPn8o+DTrH8SE6E+g0O7osw5r9kM5Q==',
            'bm_sv': '0F4E67175512C2F1C2E9A76E1E844A12~YAAQTKfcF71GgyqBAQAAz8sQchDCflfSGkidPuuVp5ddDy6l/umzr8KMZQWCW6T7dqXsVYX63VQ2jOt+hjXiru+QM2F/R/CakAIr/PdPkZHs9wk1HYYmXpkYElaOJYyB29wQBT3R+rkt/CzwmdaxtriOqZJWJc7wtHM9jn3UecrIjsJ3l97IBZUkhLqgta/IiRHBa07A8/YoXqSPG3Eer/o8GHSpo9t1oLCHnFmTDaOvSAcAOrshsZzgp0yb7S7iRoY=~1',
        }
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
        }

        html_content = requests.get(url, headers=headers, cookies=cookies, timeout=5)
        return html_content.text
    except Exception:
        send_message("Could not search autowini")
        return None


def extract_links_autowini(html):
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all('li', {'class': 'list'})
    links = []
    for item in results:
        atag = item.find_all('a')[1].get('href')
        url = f'{BASE_URL}/{str(atag)}'
        links.append(url)
    return links


def find_available_car_deals_from_autowini():
    msg = f"Search Results from {BASE_URL}\n\n"
    for make, model in KOREAN_CAR_MODELS.items():
        url = get_url(make, model, min_year='2012', max_price='2500')
        html = get_autowini_webpage(url)
        if not html:
            return
        links = extract_links_autowini(html)
        msg += construct_links_message(f'{make} {model}', url, links)
    send_message(msg)
