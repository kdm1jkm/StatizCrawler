from email.iterators import body_line_iterator
from bs4 import BeautifulSoup
from urllib import request
from prettytable import PrettyTable
from itertools import chain


class Parser:
    def __init__(self, url: str) -> None:
        # 데이터를 가져옴
        html = request.urlopen(url)
        self.bs = BeautifulSoup(html, "lxml")

        self.extract_headers()

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

    def print_headers(self):
        print(*self.header, sep=" ")


def main():
    urls = [
        "http://www.statiz.co.kr/stat.php?opt=0&sopt=0&re=0&ys=2022&ye=2022&se=0&te=&tm=&ty=0&qu=auto&po=0&as=&ae=&hi=&un=&pl=&da=1&o1=WAR_ALL_ADJ&de=1&lr=0&tr=&cv=&ml=1&sn=30&si=&cn=",
        "http://www.statiz.co.kr/player.php?opt=1&sopt=0&name=%EA%B3%A0%EC%9A%B0%EC%84%9D&birth=1998-08-06&re=1",
        "http://www.statiz.co.kr/player.php?opt=10&sopt=0&name=%EA%B3%A0%EC%9A%B0%EC%84%9D&birth=1998-08-06&re=1&da=1&lg=&year=2022",
        "http://www.statiz.co.kr/stat.php?mid=stat&re=0&ys=2022&ye=2022&se=0&te=&tm=&ty=0&qu=auto&po=0&as=&ae=&hi=&un=&pl=&da=1&o1=WAR_ALL_ADJ&o2=TPA&de=1&lr=0&tr=&cv=&ml=1&sn=30&pa=0&cn=&si=999&si_it=&si_wd=&si_tm=&si_ha=&si_te=&si_st=&si_as=&si_or=&si_ty=&si_pl=&si_in=&si_on=&si_um=&si_oc=2&si_bs=&si_sc=&si_cnt=&si_aft=&si_li=",
    ]

    parsers = [Parser(url) for url in urls]

    for parser in parsers:
        parser.print_headers()
        print("-" * 50, end="\n\n")


if __name__ == "__main__":
    main()
