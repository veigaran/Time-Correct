"""
用于纠正错误时间，统一为一种格式
https://github.com/fighting41love/cocoNLP
https://github.com/paulrinckens/timexy
把time一栏的数据全部转化为标准格式

大致思路：
1、时间归一化
2、数据库链接及校对
3、单独数据处理接口

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



def test_2(path):
    df = pd.read_csv(path)
    print(df.head())
    df1 = df[['time', 'resource']]
    # df1.to_csv("data/time_correct.csv",index=False)
    # df1.to_excel("data/time_correct.xlsx",index=False)

    grouped = df.groupby('resource')
    # time_dict ={}
    result = []
    for name, group in grouped:
        i = 0
        for index, row in group.iterrows():
            if i < 5:
                result.append([row['time'], name])
                i += 1
            else:
                break
        # result.append([name,group['time'].values])
        # time_dict[name] = group['time'].tolist()
        # print(str(name)+"："+str(len(group['time'].tolist())))
    df2 = pd.DataFrame(result, columns=['time', 'resource'])
    # df2.to_csv("data/sample.csv",index=False)
    df2.to_excel("data/sample.xlsx", index=False)


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
            result.append([year, month, day])
        elif test_str[:5] == "WIDER" and re.search(r'[0-9]{4}', test_str):
            year = re.search(r'[0-9]{4}', test_str).group()
            result.append([year, "01", "01"])
        elif re.search(pattern2, test_str):
            s = re.search(pattern2, test_str).group()
            time_info = s.split(".")
            day = time_info[0]
            month = time_info[1]
            year = time_info[2]
            result.append([year, month, day])
        elif re.search(pattern8, test_str):
            s = re.search(pattern8, test_str).group()
            time_info = s.split("/")
            day = time_info[1]
            month = time_info[0]
            year = time_info[2]
            result.append([year, month, day])
        elif re.search(pattern3, test_str):
            s = re.search(pattern3, test_str).group()
            time_info = s.split(" ")
            day = time_info[1].replace(",", "").replace("th", "").replace("st", "").replace("nd", "").replace("rd", "")
            month = MONTH[time_info[0]]
            year = time_info[2]
            result.append([year, month, day])
        elif re.search(pattern4, test_str):
            s = re.search(pattern4, test_str).group()
            time_info = s.split("-")
            day = time_info[2]
            month = time_info[1]
            year = time_info[0]
            result.append([year, month, day])
        elif re.search(pattern5, test_str):
            s = re.search(pattern5, test_str).group()
            time_info = s.split(".")
            day = time_info[0]
            month = time_info[1]
            year = time_info[2]
            result.append([year, month, day])

        else:
            if re.search(pattern6, test_str):
                s = re.search(pattern6, test_str).group()
                time_info = list(filter(None, s.split(" ")))
                day = "01"
                month = MONTH[time_info[0].replace(",", "")]
                year = time_info[1]
                result.append([year, month, day])
            elif re.search(pattern7, test_str):
                s = re.search(pattern7, test_str).group()
                time_info = s.split("/")
                day = "01"
                month = time_info[0]
                year = time_info[1]
                result.append([year, month, day])
            elif re.search(pattern9, test_str):
                s = re.search(pattern9, test_str).group()
                time_info = s.split("-")
                day = "01"
                month = time_info[1]
                year = time_info[0]
                result.append([year, month, day])
            elif test_str == "暂无数据":
                result.append([1, 1, 1])
            elif 1900 < int(test_str) < 2100:
                result.append([int(test_str), "01", "01"])
            else:
                error.append(test_str)
        if len(result[0]) > 2:
            result[0].append(test_str)
            result[0].append(str(datetime(int(result[0][0]), int(result[0][1]), int(result[0][2]))))
    except Exception as e:
        result.append([1, 1, 1, test_str, str(datetime(1, 1, 1))])
        error.append(test_str)
    return result, error


def main():
    df = pd.read_csv("data/time_correct.csv")
    total = []
    totol_error = []
    for index, row in df.iterrows():
        result, error = extract_time(row["time"])
        total.extend(result)
        totol_error.extend(error)
    df1 = pd.DataFrame(total, columns=["year", "month", "day", "origin", "datetime"])
    df1.to_csv("data/time_correct_result.csv", index=False)
    df1.to_excel("data/time_correct_result.xlsx", index=False)
    df2 = pd.DataFrame(totol_error, columns=["error"])
    df2.to_csv("data/time_correct_error.csv", index=False)
    df2.to_excel("data/time_correct_error.xlsx", index=False)


if __name__ == '__main__':
    a, b = extract_time("暂无数据")
    print(a)
    main()

    # test_1()
    # test_2("data/think_tank_base.csv")
