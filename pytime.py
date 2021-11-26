#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from time import sleep
import chromedriver_autoinstaller
import argparse
import requests
import sys
import logging


logging.basicConfig(
    handlers=[logging.FileHandler("connection.log"), logging.StreamHandler()],
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

url_list = [
    "https://www.google.no/",
    "https://www.nrk.no/",
    "https://www.eidskog.kommune.no/",
]


def open_webpage(url):
    timeout = 5  # seconds
    chrome_options = Options()
    chrome_options.headless = True
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(timeout)
    driver.delete_all_cookies()
    selenium_error = False

    try:
        driver.get(url)

        navigation_start = driver.execute_script(
            "return window.performance.timing.navigationStart"
        )
        domain_start = driver.execute_script(
            "return window.performance.timing.domainLookupStart"
        )
        connect_end = driver.execute_script(
            "return window.performance.timing.connectEnd"
        )
        response_start = driver.execute_script(
            "return window.performance.timing.responseStart"
        )
        dom_complete = driver.execute_script(
            "return window.performance.timing.domComplete"
        )

        backend_performance_calc = response_start - navigation_start
        dns_tcp_calc = connect_end - domain_start
        frontend_performance_calc = dom_complete - response_start
        total_time = dom_complete - navigation_start

        log_msg = f"200 {url} {dns_tcp_calc} {backend_performance_calc} {frontend_performance_calc} "
        logging.info(log_msg)
    except WebDriverException as e:
        try:
            r = requests.get(url, timeout=timeout)
            logging.error(f'{r.status_code} {url} "{e.msg}"')
        except requests.exceptions.RequestException as e:
            logging.error(f"408 {url} Timeout")

    driver.quit()


def main():
    chromedriver_autoinstaller.install()

    if args.urllist:
        for _ in range(args.iterations):
            for link in url_list:
                open_webpage(link)
    else:
        for _ in range(args.iterations):
            open_webpage(args.url)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=sys.modules[__name__].__doc__)
    parser.add_argument(
        "-u", "--urllist", action="store_true", help="Use predefined list of urls"
    )
    parser.add_argument("url", nargs="?", default=url_list[0])
    parser.add_argument("iterations", nargs="?", type=int, default=1)
    args = parser.parse_args()

    while True:
        main()
        sleep(10*60)  # Run each 10 minutes
