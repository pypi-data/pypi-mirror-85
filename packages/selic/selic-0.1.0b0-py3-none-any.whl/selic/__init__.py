import csv
import sys
from dataclasses import astuple, dataclass
from datetime import date, datetime
from decimal import Decimal
from itertools import starmap, zip_longest

import bs4
import requests

URL = "http://sal.receita.fazenda.gov.br/PortalSalInternet/faces/pages/tabelaPratica/exibirTabela.xhtml"  # noqa


@dataclass
class Selic:
    period: date
    ufir: Decimal
    interest: Decimal

    @classmethod
    def from_triple(cls, period, ufir, interest):
        numbers = map(Decimal, map(lambda x: 0 if x == "-" else x, (ufir, interest)))
        date_ = datetime.strptime(period, "%m/%Y").date()
        return cls(date_, *numbers)


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def extract(url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    rows = (
        soup.find(id="formExibirTabela:gridListSalariosCalculo")
        .find("tbody")
        .find_all("tr")
    )
    for ridx, row in enumerate(rows):
        cells = row.find_all("span")
        triples = starmap(Selic.from_triple, grouper((cell.text for cell in cells), 3))
        yield from triples


def main():
    writer = csv.writer(sys.stdout)
    writer.writerow("Competência UFIR Juros".split())
    iterator = sorted(map(astuple, extract(URL)), key=lambda x: x[0])
    writer.writerows(iterator)


if __name__ == "__main__":
    main()
