"""
用于纠正错误时间，统一为一种格式
"""
import re
import pandas as pd
from datetime import datetime

MONTH = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
         "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12,
         "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11,
         "Dec": 12}
DAY = {"1st": 1, "2nd": 2, "3rd": 3, "4th": 4, "5th": 5, "6th": 6, "7th": 7, "8th": 8, "9th": 9, "10th": 10, "11th": 11,
       "12th": 12, "13th": 13, "14th": 14, "15th": 15, "16th": 16, "17th": 17, "18th": 18, "19th": 19, "20th": 20,
       "21st": 21, "22nd": 22, "23rd": 23, "24th": 24, "25th": 25, "26th": 26, "27th": 27, "28th": 28, "29th": 29,
       "30th": 30, "31st": 31}


def extract_time(test_str):
    # 针对 " 17 September 2018 asccdcd  (10 January 2019) " 这种情况
    pattern1 = r'[0-9]+\W[a-zA-z]+\W[0-9]{4}'
    # 针对 18.08.2011 这种情况
    pattern2 = r'[0-9]+/.[0-9]+/.[0-9]{4}'
    # 针对 November 19th, 2020和 March 1, 2007 这种情况
    pattern3 = r'[a-zA-z]+\W[0-9a-zA-Z]+\W+[0-9]{4}'
    # 针对 2022-02-09 这种情况
    pattern4 = r'[0-9]{4}\W[0-9]{2}\W[0-9]{2}'
    # 针对 27.10.2007 这种情况
    pattern5 = r'[0-9]{2}\W[0-9]{2}\W[0-9]{4}'
    # 针对 September 2005 和February, 2020这种情况
    pattern6 = r'[a-zA-z]+\W+[0-9]{4}'
    # 针对11/2020 这种情况
    pattern7 = r'[0-9]{1,2}\W[0-9]{4}'
    # 针对07/30/2014 这种情况
    pattern8 = r'[0-9]{2}\/[0-9]{2}\/[0-9]{4}'
    # 针对2022-02 这种情况
    pattern9 = r'[0-9]{4}\W[0-9]{2}'
    result = []
    error = []
    try:
        if re.search(pattern1, test_str):
            s = re.search(pattern1, test_str).group()
            time_info = s.split(" ")
            day = time_info[0]
            month = MONTH[time_info[1]]
            year = time_info[2]
            result = [year, month, day]
        elif test_str[:5] == "WIDER" and re.search(r'[0-9]{4}', test_str):
            year = re.search(r'[0-9]{4}', test_str).group()
            result = [year, "01", "01"]
        elif re.search(pattern2, test_str):
            s = re.search(pattern2, test_str).group()
            time_info = s.split(".")
            day = time_info[0]
            month = time_info[1]
            year = time_info[2]
            result = [year, month, day]
        elif re.search(pattern8, test_str):
            s = re.search(pattern8, test_str).group()
            time_info = s.split("/")
            day = time_info[1]
            month = time_info[0]
            year = time_info[2]
            result = [year, month, day]
        elif re.search(pattern3, test_str):
            s = re.search(pattern3, test_str).group()
            time_info = s.split(" ")
            day = time_info[1].replace(",", "").replace("th", "").replace("st", "").replace("nd", "").replace("rd", "")
            month = MONTH[time_info[0]]
            year = time_info[2]
            result = [year, month, day]
        elif re.search(pattern4, test_str):
            s = re.search(pattern4, test_str).group()
            time_info = s.split("-")
            day = time_info[2]
            month = time_info[1]
            year = time_info[0]
            result = [year, month, day]
        elif re.search(pattern5, test_str):
            s = re.search(pattern5, test_str).group()
            time_info = s.split(".")
            day = time_info[0]
            month = time_info[1]
            year = time_info[2]
            result = [year, month, day]
        else:
            if re.search(pattern6, test_str):
                s = re.search(pattern6, test_str).group()
                time_info = list(filter(None, s.split(" ")))
                day = "01"
                month = MONTH[time_info[0].replace(",", "")]
                year = time_info[1]
                result = [year, month, day]
            elif re.search(pattern7, test_str):
                s = re.search(pattern7, test_str).group()
                time_info = s.split("/")
                day = "01"
                month = time_info[0]
                year = time_info[1]
                result = [year, month, day]
            elif re.search(pattern9, test_str):
                s = re.search(pattern9, test_str).group()
                time_info = s.split("-")
                day = "01"
                month = time_info[1]
                year = time_info[0]
                result = [year, month, day]
            elif test_str == "暂无数据":
                result = [1000, 1, 1]
            elif 1900 < int(test_str) < 2100:
                result = [int(test_str), "01", "01"]
            else:
                error.append(test_str)
        if len(result) > 2:
            result.append(test_str)
            result.append(str(datetime(int(result[0]), int(result[1]), int(result[2]))))
    except Exception as e:
        result = [1, 1, 1, test_str, str(datetime(1000, 1, 1))]
        error.append(test_str)
    return result, error


def get_time_api(origin_time):
    res,error = extract_time(origin_time)
    return res[4]


if __name__ == '__main__':
    print(get_time_api("17 May 2022"))
    print(get_time_api("2022-02-09"))
    print(get_time_api("27.10.2007"))
    print(get_time_api("September 2005"))
    print(get_time_api("February, 2020"))
    # main()
    # change_origin_data("data/think_tank_base.csv")
    # test_1()
    # test_2("data/think_tank_base.csv")
    # df = pd.read_csv("data/think_tank_base.csv")
    # print(len(df))
    # a, b = extract_time("暂无数据")
    # print(a)
