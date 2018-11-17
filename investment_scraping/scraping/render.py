import itertools
from typing import Generator

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from investment_scraping.scraping import PARIBAS_URL, NEXT_PAGE_XPATH, NEXT_PAGE_XPATH_2, TABLE_XPATH
from investment_scraping.scraping.ghosts import Ghost

WAIT_DELAY = 2


def _goto_next_page(ghost: Ghost) -> bool:
    assert ghost.driver is not None
    element = _find_next_page_button(ghost)
    if element:
        ghost.driver.execute_script("arguments[0].click();", element)
    return element


def _find_next_page_button(ghost, page_xpath: str= NEXT_PAGE_XPATH_2):
    assert ghost.driver is not None
    try:
        button = ghost.driver.find_element_by_xpath(page_xpath)
        if button.text != 'Página siguiente':
            print('Finished loading pages')
            return False
    except NoSuchElementException:
        if page_xpath == NEXT_PAGE_XPATH_2:
            return _find_next_page_button(ghost, NEXT_PAGE_XPATH)
        else:
            print('Finished loading pages')
            return False
    return button


def _wait_for_table_loaded(ghost: Ghost):
    WebDriverWait(ghost.driver, WAIT_DELAY).until(
        expected_conditions.presence_of_element_located((By.XPATH, TABLE_XPATH)))
    print('Table is ready')


def get_bnp_pariba_pages(ghost: Ghost) -> Generator[str, None, None]:
    with ghost as driver:
        driver.get(PARIBAS_URL)

        for page_num in itertools.count(start=1, step=1):
            _wait_for_table_loaded(ghost)

            yield driver.page_source

            has_next_page = _goto_next_page(ghost)
            if not has_next_page:
                break

            print(f'Loading page {page_num}')
