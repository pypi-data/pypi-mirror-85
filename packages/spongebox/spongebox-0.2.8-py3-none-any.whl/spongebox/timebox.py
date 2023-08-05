import datetime
import time
import warnings
import re


class InvalidInputError(Exception):
    pass


class UnknownDateFormatError(InvalidInputError):
    pass


def crossbar(date):
    """
    :param date: yyyymmdd:int
    :return: yyyy-mm-dd:str
    """
    return "{}-{}-{}".format(str(date)[0:4], str(date)[4:6], str(date)[6:])


def format_match(date):
    """
    :param date:
    :return:
    """
    _ = str(date)
    if re.match(r"\d{8}$", _):
        return "%Y%m%d"
    elif re.match(r"\d{12}$", _):
        return "%Y%m%d%H%M"
    elif re.match(r"\d{14}$", _):
        return "%Y%m%d%H%M%S"
    elif re.match(r"\d{4}-\d{2}-\d{2}$", _):
        return "%Y-%m-%d"
    elif re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$", _):
        return "%Y-%m-%d %H:%M:%S"
    else:
        raise UnknownDateFormatError("valid formats: %Y%m%d, %Y%m%d%H%M, %Y%m%d%H%M%S, %Y-%m-%d, %Y-%m-%d %H:%M:%S")


def strptime(date):
    """
    :param date: formated str('yyyy-mm-dd','yyyymmdd','yyyy-mm-dd H:M:S'etc) or int(yyyymmdd,yyyymmddHMS)
    :param format:
    :return: datetime.datetime object
    """
    _ = str(date)
    return datetime.datetime.strptime(_, format_match(_))


def stamp():
    """
    :return: now() in "%Y%m%d%H%M%S":str
    """
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")


def interval(start, end):
    """
    :param start: %Y-%m-%d[.*]:str or yyyymmdd:int
    :param end: %Y-%m-%d[.*]:str or yyyymmdd:int
    :return:days:int between input dates
    """
    return (strptime(end) - strptime(start)).days


def move(date, days=0):
    """
    :param date: formated str('yyyy-mm-dd','yyyymmdd','yyyy-mm-dd H:M:S'etc) or int(yyyymmdd,yyyymmddHMS)
    :param days: int
    :return: datetime.datetime object
    """
    return strptime(date) + datetime.timedelta(days=days)


def add_days(date, n):
    """
    :param date: yyyy-mm-dd[.*]:str or yyyymmdd:int or datetime.datetime
    :param n: n days before/after date ( allow negative)
    :return: date before/after input date:datetime.datetime
    """
    warnings.warn("timebox.add_days() will be deprecated in futrue,use timebox.move() instead")
    date = str(date)
    if date.isdigit():
        date = crossbar(date)
    return datetime.datetime.strptime(date[0:10], "%Y-%m-%d") + datetime.timedelta(days=n)


def format(datetime, format="%Y-%m-%d %H:%m:%S"):
    """
    :param datetime: datetime.dateime
    :param format: default %Y-%m-%d %H:%m:%S
    :return: format time str
    """
    warnings.warn("timebox.format() will be deprecated in futrue,use timebox.strftime() instead")
    return datetime.strftime(format)


def timeit(func):
    def wrap(*args, **kwargs):
        ts = time.time()
        result = func(*args, **kwargs)
        te = time.time()
        # warnings.warn("this method will be deprecated in futrue,use measurebox.timeit instead")
        print("#{}() cost:{}".format(func.__name__, te - ts))
        return result

    return wrap


if __name__ == "__main__":
    print(strptime(20200302))
    print(strptime("20200302"))
    print(strptime("2020-03-02"))
    print(strptime("2020-03-02 15:20:02"))

    print(strftime(strptime("2020-03-02")))

    print(format(strptime("2020-03-02")))

    print(move(strptime("2020-03-02"), -28))

    print(stamp())
    print(interval("2020-01-16", "2020-01-17"))
    print(interval("2020-01-16", "2021-01-17"))
    print(add_days("2020-01-16", -1))
    # print(add_days("2020er33", -1))
    print(add_days(20200225, -1))


    @timeit
    def test():
        time.sleep(3)
        print("end")


    test()
    # print(format(datetime.datetime.now()))
    #
    #
    # @timeit
    # def test_timeit(n):
    #     a = 1
    #     for i in range(n):
    #         a += 1
    #     print(a)
    #
    #
    # test_timeit(100000)
