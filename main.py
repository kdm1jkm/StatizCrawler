from datetime import datetime
import os
from parser import Parser


def parser_test():
    urls = [
        "http://www.statiz.co.kr/stat.php?opt=0&sopt=0&re=0&ys=2022&ye=2022&se=0&te=&tm=&ty=0&qu=auto&po=0&as=&ae=&hi=&un=&pl=&da=1&o1=WAR_ALL_ADJ&de=1&lr=0&tr=&cv=&ml=1&sn=30&si=&cn=",
        "http://www.statiz.co.kr/player.php?opt=1&sopt=0&name=%EA%B3%A0%EC%9A%B0%EC%84%9D&birth=1998-08-06&re=1",
        "http://www.statiz.co.kr/player.php?opt=10&sopt=0&name=%EA%B3%A0%EC%9A%B0%EC%84%9D&birth=1998-08-06&re=1&da=1&lg=&year=2022",
        "http://www.statiz.co.kr/stat.php?mid=stat&re=0&ys=2022&ye=2022&se=0&te=&tm=&ty=0&qu=auto&po=0&as=&ae=&hi=&un=&pl=&da=1&o1=WAR_ALL_ADJ&o2=TPA&de=1&lr=0&tr=&cv=&ml=1&sn=30&pa=0&cn=&si=999&si_it=&si_wd=&si_tm=&si_ha=&si_te=&si_st=&si_as=&si_or=&si_ty=&si_pl=&si_in=&si_on=&si_um=&si_oc=2&si_bs=&si_sc=&si_cnt=&si_aft=&si_li=",
    ]

    parsers = [Parser(url) for url in urls]

    print("HEADERS")
    for parser in parsers:
        parser.print_headers()
        print("-" * 50, end="\n\n")

    print("\nCONTENTS")
    for parser in parsers:
        parser.print_contents()
        print("-" * 50, end="\n\n")

    print("TABLE")
    for parser in parsers:
        print(parser, end="\n\n")


def main():
    url = input("url을 입력하세요: ")
    parser = Parser(url)
    print(*map(lambda i: f"{i[0]}: {i[1]}", enumerate(parser.header)), sep=" " * 2)

    indexes = []
    while True:
        index = input("열 번호 입력: ")
        if index == "":
            break
        indexes.append(int(index))

    parser.select_columns(indexes)
    print(parser)

    if not os.path.isdir("./extracted"):
        os.mkdir("./extracted")
    with open(
        f"extracted/{datetime.now().strftime('%Y%m%d-%H%M%S')}.csv",
        "w",
        encoding="euc-kr",
    ) as f:
        f.write(parser.to_csv_string())


if __name__ == "__main__":
    main()
