#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
import requests
from utils import construct_links_message, send_message

JAPANESE_CAR_MODELS = {
    "vitz": {
        "id": "275",
        "make": "1"
    },
    "yaris": {
        "id": "1244",
        "make": "1"
    },
}

BASE_URL = "https://www.beforward.jp"


def construct_url(car_model, min_year, budget):
    global JAPANESE_CAR_MODELS

    if car_model not in JAPANESE_CAR_MODELS:
        return None

    car_make_id = JAPANESE_CAR_MODELS[car_model]["make"]
    car_model_id = JAPANESE_CAR_MODELS[car_model]["id"]

    url = (
        f"{BASE_URL}/stocklist/client_wishes_id=/"
        f"description=/make={car_make_id}/model={car_model_id}/"
        f"model_code=/fuel=/fob_price_from=/fob_price_to={budget}/"
        f"veh_type=/steering=/mission=/mfg_year_from={min_year}/"
        f"mfg_month_from=/mfg_year_to=/mileage_from=/mileage_to=/"
        f"cc_from=/cc_to=/showmore=/drive_type=/color=/stock_country=/"
        f"area=/seats_from=/seats_to=/max_load_min=/max_load_max=/"
        f"veh_type_sub=/view_cnt=25/page=1/sortkey=n/sar=/steering=Left/view_cnt=100/"
        f"from_stocklist=1/keyword=/kmode=and/")
    return url


def get_html_webscraper(url):
    result = requests.get(url).text
    doc = BeautifulSoup(result, "html.parser")
    return doc


def extract_links_webscraper(base_model, doc):
    global BASE_URL
    table_body = doc.find("table", attrs={"class": "stocklist-row-wrap"})

    links = set()
    for link in table_body.find_all("a"):
        href_value = link.get("href")
        if href_value and (href_value not in links):
            if href_value.startswith("/"):
                links.add(f"https://www.beforward.jp{href_value}")

    return list(links)


def find_best_car_deals_in_japan():
    msg = f"Search Results from {BASE_URL}\n\n"
    for model in JAPANESE_CAR_MODELS:
        site = construct_url(model, 2012, 2500)
        html_page = get_html_webscraper(site)
        web_links = extract_links_webscraper(model, html_page)
        car_deals_msg = construct_links_message(model, site, web_links)
        msg += car_deals_msg

    send_message(msg)
