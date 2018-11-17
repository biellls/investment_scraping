import csv
from typing import Iterable

from investment_scraping.models import FundsTableRow


# noinspection PyUnresolvedReferences,PyProtectedMember
def write_csv(rows: Iterable[FundsTableRow], batch_num=1):
    header = rows[0]._asdict().keys()
    with open(f'output/part{batch_num}.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
        f.flush()
