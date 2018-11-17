import itertools
import math
import os
from time import sleep

from investment_scraping import PROJECT_DIR
from investment_scraping.csv_writer import write_csv
from investment_scraping.scraping.ghosts import ChromeGhost
from investment_scraping.scraping.render import get_bnp_pariba_pages
from investment_scraping.scraping.scrap import get_rows_data

CHROME_PATH = "/opt/homebrew-cask/Caskroom/google-chrome/latest/Google Chrome.app/Contents/MacOS/Google Chrome"
CHROMEDRIVER_PATH = os.path.join(PROJECT_DIR, 'resources', 'chromedriver')

BATCH_SIZE_PAGES = 2

if __name__ == '__main__':
    ghost = ChromeGhost(CHROME_PATH, CHROMEDRIVER_PATH)
    rows_batch = []
    page_num = None
    for page_html, page_num in zip(get_bnp_pariba_pages(ghost), itertools.count(start=1, step=1)):
        rows = get_rows_data(page_html)
        rows_batch += rows
        if page_num % BATCH_SIZE_PAGES == 0:
            batch_num = int(page_num / BATCH_SIZE_PAGES)
            write_csv(rows_batch, batch_num)
            print(f'CSV {batch_num} written')
            rows_batch = []

        sleep(0.4)

    if rows_batch:
        write_csv(rows_batch, math.ceil(page_num / BATCH_SIZE_PAGES))
