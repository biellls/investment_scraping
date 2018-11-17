from datetime import datetime
from typing import List, Tuple

from scrapy import Selector

from investment_scraping.models import FundsTableRow
from investment_scraping.scraping import TABLE_XPATH


def _get_rows_html(html):
    rows = Selector(text=html).xpath(TABLE_XPATH + '/tbody/tr').extract()
    return rows[1:]


def _get_row_links(row_html):
    tds = Selector(text=row_html).xpath('//td').extract()
    return (
        Selector(text=tds[0]).xpath('//a/@href').extract_first(),
        Selector(text=tds[2]).xpath('//a/@href').extract_first(),
        Selector(text=tds[-1]).xpath('//a/@href').extract_first(),
    )


def _make_row(row_html):
    data = _get_row_text(row_html)
    links = _get_row_links(row_html)
    row = FundsTableRow(
        funds=data[0],
        funds_link=links[0],
        isin=data[1],
        registration_fees_link=links[1],
        manager=data[2],
        category=data[3],
        subcategory=data[4],
        currency=data[5],
        stock=float(data[6]),
        value_date=datetime.strptime(data[7], '%d/%m/%Y').strftime('%Y-%m-%d'),
        legal_info_link=links[2],
    )
    return row


def _get_rows(rows_html):
    return [_make_row(row_html) for row_html in rows_html]


def _get_row_text(row_html):
    links_text = Selector(text=row_html).xpath('//td/a/text()').extract()
    regular_text = Selector(text=row_html).xpath('//td/text()').extract()
    all_text = links_text + regular_text
    return [x.strip() for x in all_text]


def get_data(html: str) -> List[FundsTableRow]:
    rows_html = _get_rows_html(html)
    return _get_rows(rows_html)
