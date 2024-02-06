#!/usr/bin/env python
# coding: utf-8
from korea import find_available_car_deals_from_autowini
from japan import find_best_car_deals_in_japan


def run():
    find_best_car_deals_in_japan()
    find_available_car_deals_from_autowini()


if __name__ == '__main__':
    run()
