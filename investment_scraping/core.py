import math
import os
from time import sleep

from investment_scraping import PROJECT_DIR
from investment_scraping.csv_writer import write_csv
from investment_scraping.scraping.ghosts import ChromeGhost
from investment_scraping.scraping.render import get_bnp_pariba_pages
from investment_scraping.scraping.scrap import get_data

CHROME_PATH = "/opt/homebrew-cask/Caskroom/google-chrome/latest/Google Chrome.app/Contents/MacOS/Google Chrome"
CHROMEDRIVER_PATH = os.path.join(PROJECT_DIR, 'resources', 'chromedriver')

BATCH_SIZE = 500

if __name__ == '__main__':
    ghost = ChromeGhost(CHROME_PATH, CHROMEDRIVER_PATH)
    i = 1
    rows_batch = []
    for page in get_bnp_pariba_pages(ghost):
        rows = get_data(page)
        rows_batch += rows
        if i % BATCH_SIZE == 0:
            batch_num = int(i / BATCH_SIZE)
            write_csv(rows_batch, batch_num)
            print(f'CSV {batch_num} written')
            rows_batch = []

        i += 1
        sleep(0.4)

    if rows_batch:
        write_csv(rows_batch, math.ceil(i/BATCH_SIZE))
