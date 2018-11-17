from typing import NamedTuple


class FundsTableRow(NamedTuple):
    funds: str
    funds_link: str
    isin: str
    registration_fees_link: str
    manager: str
    category: str
    subcategory: str
    currency: str
    stock: float
    value_date: str
    legal_info_link: str
