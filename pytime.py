#!/usr/bin/env python3

from datetime import datetime
from selenium import webdriver
from time import sleep
import argparse
import requests
import statistics
import sys

url_list = ["https://www.google.no/",
            "https://www.nrk.no/",
            "http://www.eidskog-o-lag.no/",
            "https://www.eidskog.kommune.no/"]

filename = "webtimingslog.txt"


def write_to_file(url, backend_time, frontend_time):
    now = datetime.now()
    with open(filename, 'a') as file:
        if backend_time is not None and frontend_time is not None:
            file.write(f"{now}, {url}, {backend_time}, {frontend_time}\n")
        else:
            file.write(f"{now}, {url}, {backend_time}, {frontend_time}\n")


def open_webpage(url):
    driver = webdriver.Chrome()
    driver.delete_all_cookies()
    driver.get(url)

    navigation_start = driver.execute_script("return window.performance.timing.navigationStart")
    domain_start = driver.execute_script("return window.performance.timing.domainLookupStart")
    connect_end = driver.execute_script("return window.performance.timing.connectEnd")
    response_start = driver.execute_script("return window.performance.timing.responseStart")
    dom_complete = driver.execute_script("return window.performance.timing.domComplete")

    backend_performance_calc = response_start - navigation_start
    dns_tcp_calc = connect_end - domain_start
    frontend_performance_calc = dom_complete - response_start
    total_time = dom_complete - navigation_start

    driver.quit()

    # Only return timing if page loaded successfully, otherwise None
    try:
        r = requests.get(url, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"Timeout loading page {url}")
        return None, None

    if r.status_code == 200:
        print("URL       : %s" % url)
        print("Back End  : %s" % backend_performance_calc)
        print("DNS+TCP   : %s" % dns_tcp_calc)
        print("Front End : %s" % frontend_performance_calc)
        print("Total time: %s" % total_time)
        return backend_performance_calc, frontend_performance_calc
    else:
        print(f"Timeout loading page {url}")
        return None, None


def main():
    backend_performance_list = []
    frontend_performance_list = []

    if args.urllist:
        for _ in range(args.iterations):
            for link in url_list:
                result = open_webpage(link)
                if result[0] is not None:
                    backend_performance_list.append(result[0])
                if result[1] is not None:
                    frontend_performance_list.append(result[1])
                write_to_file(link, result[0], result[1])
    else:
        for _ in range(args.iterations):
            result = open_webpage(args.url)
            if result[0] is not None:
                backend_performance_list.append(result[0])
            if result[1] is not None:
                frontend_performance_list.append(result[1])
            write_to_file(args.url, result[0], result[1])

    print('Backend       : {}'.format(backend_performance_list))
    print('Frontend      : {}'.format(frontend_performance_list))
    if backend_performance_list and frontend_performance_list:
        print('Backend mean  : {}'.format(statistics.mean(backend_performance_list)))
        print('Backend median: {}'.format(statistics.median(backend_performance_list)))
        print('Backend min   : {}'.format(min(backend_performance_list)))
        print('Backend max   : {}'.format(max(backend_performance_list)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=sys.modules[__name__].__doc__)
    parser.add_argument('-u', '--urllist', action='store_true', help="Use predefined list of urls")
    parser.add_argument('url', nargs='?', default=url_list[0])
    parser.add_argument('iterations', nargs='?', type=int, default=1)
    args = parser.parse_args()

    while True:
        main()
        sleep(15*60)  # Run each 15 minutes
