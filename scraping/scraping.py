import os
import datetime
import csv
import urllib.request
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta

import warnings
warnings.simplefilter("ignore")


# 文字列を浮動小数点型に変換
def str2float(weather_data):
    try:
        return float(weather_data)
    except:  # NOQA
        return float(0)


# スクレイピングの実施
def scraping(url, date):
    # 気象データのページを取得
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html)
    trs = soup.find("table", {"class": "data2_s"})

    data_list = []
    data_list_per_day = []
    # table の中身を取得
    for tr in trs.findAll("tr")[4:]:
        tds = tr.findAll("td")

        if tds[1].string is None:
            break

        data_list.append(date.year)
        data_list.append(date.month)
        data_list.append(tds[0].string)
        data_list.append(str2float(tds[2].string))
        data_list.append(str2float(tds[3].string))
        data_list.append(str2float(tds[6].string))
        data_list.append(str2float(tds[7].string))
        data_list.append(str2float(tds[8].string))
        data_list.append(str2float(tds[9].string))
        data_list.append(str2float(tds[10].string))
        data_list.append(str2float(tds[11].string))
        data_list.append(str2float(tds[12].string))
        data_list.append(tds[13].string)
        data_list.append(str2float(tds[16].string))

        data_list_per_day.append(data_list)

        data_list = []

    return data_list_per_day


def create_csv(area_name, prec_no, block_no):
    # CSV 出力先ディレクトリ
    output_dir = r"../training/data"

    # 出力ファイル名
    output_file = f"{area_name}.csv"

    # データ取得開始・終了日
    start_date = datetime.date(1973, 1, 1)
    end_date = datetime.date(2022, 12, 1)

    # CSV の列名
    fields = [
        "年",
        "月",
        "日",
        "気圧",
        "降水量",
        "平均気温",
        "最高気温",
        "最低気温",
        "平均湿度",
        "最小湿度",
        "平均風速",
        "最大風速（風速）",
        "最大風速（風向）",
        "日照時間",
    ]

    # CSVへの書き込み
    with open(os.path.join(output_dir, output_file), "w") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(fields)

        date = start_date
        while date != end_date + relativedelta(months=1):
            # 対象url
            url = (
                "http://www.data.jma.go.jp/obd/stats/etrn/view/daily_s1.php?"
                f"prec_no={prec_no}&block_no={block_no}&year={date.year}&month={date.month}&day=&view=" # NOQA
            )

            # 1日毎のデータを取得
            data_per_day = scraping(url, date)

            for dpd in data_per_day:
                writer.writerow(dpd)

            date += relativedelta(months=1)


if __name__ == "__main__":
    # 主要13都市の情報を取得
    areas = {
        "naha": [91, 47936],
        "kagoshima": [88, 47827],
        "fukuoka": [82, 47807],
        "hiroshima": [67, 47765],
        "kochi": [74, 47893],
        "osaka": [62, 47772],
        "nagoya": [51, 47636],
        "kanazawa": [56, 47605],
        "tokyo": [44, 47662],
        "niigata": [54, 47604],
        "sendai": [34, 47590],
        "sapporo": [14, 47412],
        "kushiro": [19, 47418],
    }
    for area in areas:
        create_csv(area, areas[area][0], areas[area][1])
