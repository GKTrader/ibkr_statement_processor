# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from ibkr_statement_getter.ibkr_statement_getter.spiders.ibkr_spider import IbkrSpider


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    s = get_project_settings()

    process = CrawlerProcess(s)

    process.crawl(IbkrSpider)
    process.start() # the script will block here until the crawling is finished

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
