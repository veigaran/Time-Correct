
import re
import pandas as pd
from timeCorrect import extract_time


def change_origin_data(path):
    df = pd.read_csv(path)
    time_new = []
    for index, row in df.iterrows():
        result, error = extract_time(row["time"])
        # print(result)
        time_new.append(result[4])
    print("时间处理完成")
    df['time_new'] = time_new
    df1 = df.iloc[:10]
    df1.to_csv("test.csv", index=False)
    df.to_csv("total.csv", index=False)
    df.to_excel("total.xlsx", index=False)

    # df1.to_excel("time_correct_total.xlsx", index=False)

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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
