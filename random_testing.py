from datetime import datetime

if __name__ == "__main__":
    time = '2018/03/02 14:47:36'
    date_object = datetime.strptime(time, '%Y/%m/%d %H:%M:%S')
    print(date_object)
