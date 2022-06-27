from bs4 import BeautifulSoup
from urllib import request, parse
from prettytable import PrettyTable


class Parser:
    def __init__(self, name: str) -> None:
        url = f"http://www.statiz.co.kr/player.php?name={parse.quote(name)}"
        html = request.urlopen(url)

        self.bs = BeautifulSoup(html, "lxml")

        callout = self.bs.select_one("div.callout > div > button > font")

        if callout.text == "선수 정보":
            table = PrettyTable()
            rows = [[data.text for data in row.select("td")] for row in self.bs.select("table > tr")]
            table.field_names = rows[0]
            table.add_rows(rows[1:])

            print(table)
            index = int(input("선수 선택(번호): "))

            birthday = self.bs.select("table > tr")[index].select("td")[2].text
            url = f"http://www.statiz.co.kr/player.php?name={parse.quote(name)}&birth={birthday}"
            html = request.urlopen(url)

            self.bs = BeautifulSoup(html, "lxml")


def main():
    parser = Parser("이정후")
    parser = Parser("고우석")
    
if __name__ == "__main__":
    main()