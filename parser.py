from bs4 import BeautifulSoup
from urllib import request
from texttable import Texttable
from itertools import chain


class Parser:
    def __init__(self, url: str) -> None:
        # 데이터를 가져옴
        html = request.urlopen(url)
        self.bs = BeautifulSoup(html, "lxml")

        self.extract_headers()
        self.extract_contents()

    def extract_headers(self):
        # 표를 가져옴(한 페이지에 표는 하나라 가정)
        tables = self.bs.select("table")
        # 데이터 정리
        headers = [
            [
                {
                    "rowspan": int(header.attrs["rowspan"])
                    if "rowspan" in header.attrs.keys()
                    else 1,
                    "colspan": int(header.attrs["colspan"])
                    if "colspan" in header.attrs.keys()
                    else 1,
                    "content": header.text,
                }
                for header in header_row.select("th")
            ]
            for table in tables
            for header_row in table.select("tr")
            if len(header_row.select("th")) != 0
        ]
        # 중복되는 헤더 제거
        header_max_rowspan = max(map(lambda header: header["rowspan"], headers[0]))
        headers = headers[:header_max_rowspan]

        # rowspan, colspan에 맞춰서 재가공

        # colspan먼저
        headers = [
            list(chain(*[[data for _ in range(data["colspan"])] for data in header]))
            for header in headers
        ]

        # 첫째 행, 둘째 행 합치기(rowspan 처리)
        header = []
        if len(headers) == 1:
            header = [data["content"] for data in headers[0]]
        elif len(headers) == 2:
            header_iter = headers[1].__iter__()
            for data in headers[0]:
                if data["rowspan"] == 1:
                    header.append(f'{next(header_iter)["content"]}({data["content"]})')
                else:
                    header.append(data["content"])

        self.header = header

    def extract_contents(self):
        tables = self.bs.select("table")
        contents = [
            [data.text for data in row.select("td")]
            for table in tables
            # if "class" in table.attrs.keys() and "table" in table.attrs["class"]
            for row in table.select("tr")
            if len(row.select("td")) == len(self.header)
        ]

        self.contents = contents

    def print_headers(self):
        print(*self.header, sep=" ")

    def print_contents(self):
        print(*map(lambda content: "|".join(content), self.contents), sep="\n\n")

    def __str__(self) -> str:
        table = Texttable()
        table.set_max_width(0)
        table.header(self.header)
        table.add_rows(self.contents, header=False)
        return table.draw()
