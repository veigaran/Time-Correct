后续使用直接调用get_time_api方法，输入待提取的时间字符串，输出格式化的字符，如
输入"17 May 2022" 处理后输出"2022-05-17 00:00:00"


```
def get_time_api(origin_time):
    return extract_time(origin_time)[4]
```