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

import pymysql
import spacy
from timexy import Timexy
import spacy.cli
import pandas as pd

# January，February，March，April，May，June，July，August，September，October，November，December
MONTH = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
         "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12,
         "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11,
         "Dec": 12}
DAY = {"1st": 1, "2nd": 2, "3rd": 3, "4th": 4, "5th": 5, "6th": 6, "7th": 7, "8th": 8, "9th": 9, "10th": 10, "11th": 11,
       "12th": 12, "13th": 13, "14th": 14, "15th": 15, "16th": 16, "17th": 17, "18th": 18, "19th": 19, "20th": 20,
       "21st": 21, "22nd": 22, "23rd": 23, "24th": 24, "25th": 25, "26th": 26, "27th": 27, "28th": 28, "29th": 29,
       "30th": 30, "31st": 31}


class ThinkTankDB:
    def __init__(self, host, user, password, database):
        self.db = pymysql.connect(host='',
                                  port=3306,
                                  user='admin',
                                  password='',
                                  db='',
                                  charset='utf8')

    def get_data(self, sql):
        cursor = self.db.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        return data


def test_1(test_str):
    # ex = extractor()
    # print( ex.extract_time("27.10.2007")) ok
    # print( ex.extract_time(r"November 16th, 2020")) no
    # print( ex.extract_time("February, 2021")) no
    # print( ex.extract_time("Posted on March 1, 2007 | ")) ok
    # print( ex.extract_time(" 2022-02-09 ")) ok
    # spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

    # Optionally add config if varying from default values
    config = {
        "kb_id_type": "timex3",  # possible values: 'timex3'(default), 'timestamp'
        "label": "timexy",  # default: 'timexy'
        "overwrite": False  # default: False
    }
    nlp.add_pipe("timexy", config=config, before="ner")

    doc = nlp(test_str)
    for e in doc.ents:
        print(f"{e.text}\t{e.label_}\t{e.kb_id_}")


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
    pattern7 = r'[0-9]{2}\W[0-9]{4}'
    # 针对07/30/2014 这种情况
    pattern8 = r'[0-9]{2}\/[0-9]{2}\/[0-9]{4}'
    #针对2022-02 这种情况
    pattern9 = r'[0-9]{4}\W[0-9]{2}'
    result = []
    error = []
    if re.search(pattern1, test_str):
        s = re.search(pattern1, test_str).group()
        time_info = s.split(" ")
        day = time_info[0]
        month = MONTH[time_info[1]]
        year = time_info[2]
        result.append([year, month, day])
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
            time_info = s.split(" ")
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
            result.append([0, 0, 0])
            # error.append(test_str)
        elif len(test_str) == 4 and test_str.isdigit() and int(test_str)>1900 and int(test_str)<2100:
            result.append([test_str, "01", "01"])
        else:
            error.append(test_str)
    print(result)
    return result, error
    # print(error)


if __name__ == '__main__':
    df = pd.read_csv("data/time_correct.csv")
    total = []
    totol_error = []
    for index, row in df.iterrows():
        # print(row["time"])
        try:
            result, error = extract_time(row["time"])
            total.extend(result)
            totol_error.extend(error)
        except:
            continue
    df1 = pd.DataFrame(total, columns=["year", "month", "day"])
    df1.to_csv("data/time_correct_result.csv", index=False)
    df2 = pd.DataFrame(totol_error, columns=["error"])
    df2.to_csv("data/time_correct_error.csv", index=False)


    # test_1()
    # test_2("data/think_tank_base.csv")
    # extract_time("hhhhh 你啊后 17 September 201asccdcd  (10 January 2019)Julkaistu18.08.2011")
    # extract_time("针对17 September 2009这种情况")
    # extract_time("November 19, 2015, 3:15 pm")
    # extract_time("March 20, 2013")
    # extract_time("2021-06-19")
    # extract_time("['26 Jan 2009						']")
    # extract_time("August 29, 2005")
    # extract_time("April 29, 2020")
    # extract_time("October 8, 2020 at 10:17 am")
    # extract_time("15 July 2010")
    # extract_time("December 27, 2021")
    # extract_time("September 2005")
    # extract_time("14.01.2005")
    # extract_time("September 2005 ")
    # extract_time("和February, 2020")
    # extract_time("02/2019")
    # extract_time("07/30/2014")
    # extract_time("14.01.2005")
    # extract_time("2018-02")
    # extract_time("2018")
