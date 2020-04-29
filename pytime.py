#!/usr/bin/env python3
from selenium import webdriver
import argparse
import statistics
import sys

hyperlink = "http://nrk.no"


def open_webpage(url):
    driver = webdriver.Chrome()
    driver.get(url)

    navigation_start = driver.execute_script("return window.performance.timing.navigationStart")
    response_start = driver.execute_script("return window.performance.timing.responseStart")
    dom_complete = driver.execute_script("return window.performance.timing.domComplete")

    backend_performance_calc = response_start - navigation_start
    frontend_performance_calc = dom_complete - response_start
    total_time = backend_performance_calc + frontend_performance_calc

    print("URL       : %s" % url)
    print("Back End  : %s" % backend_performance_calc)
    print("Front End : %s" % frontend_performance_calc)
    print("Total time: %s" % total_time)

    driver.quit()
    return backend_performance_calc, frontend_performance_calc


def main():
    parser = argparse.ArgumentParser(description=sys.modules[__name__].__doc__)
    parser.add_argument('url', nargs='?', default=hyperlink)
    parser.add_argument('iterations', nargs='?', type=int, default=1)
    args = parser.parse_args()

    backend_performance_list = []
    frontend_performance_list = []
    for _ in range(args.iterations):
        result = open_webpage(args.url)
        backend_performance_list.append(result[0])
        frontend_performance_list.append(result[1])

    print('Backend       : {}'.format(backend_performance_list))
    print('Backend mean  : {}'.format(statistics.mean(backend_performance_list)))
    print('Backend median: {}'.format(statistics.median(backend_performance_list)))
    print('Backend min   : {}'.format(min(backend_performance_list)))
    print('Backend max   : {}'.format(max(backend_performance_list)))

    print('Frontend: {}'.format(frontend_performance_list))


if __name__ == '__main__':
    main()
