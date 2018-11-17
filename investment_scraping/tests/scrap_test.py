import os

from investment_scraping import PROJECT_DIR
from investment_scraping.scraping.scrap import get_data


def read_file(filename):
    file_path = os.path.join(
        PROJECT_DIR,
        'tests',
        filename,
    )
    with open(file_path, 'r') as f:
        return f.read()


def test_get_table():
    html = read_file('page1.html')
    data = list(get_data(html))
    assert data == -1
