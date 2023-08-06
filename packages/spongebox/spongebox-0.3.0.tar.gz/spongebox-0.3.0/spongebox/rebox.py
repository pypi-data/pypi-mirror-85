import re


class judger:

    def __init__(self, suspect):
        self.suspect = suspect

    def isdigit(self):
        return False if re.match("^\d+\.\d+$|^\d+$", self.suspect) == None else True


# def filterlist_(lst, exp):
    # match = [re.search(exp, item) for item in lst]
    # return [item.group() for item in match if item is not None]


def filter_list(lst, pattern=None, judge_func=None):
    if pattern is not None:
        for item in lst:
            match_obj = re.search(pattern,item)
            if match_obj is not None:
                yield item
        return
    if judge_func is not None:
        for item in lst:
            if judge_func(item):
                yield item
        return
    raise TypeError("filter_list() missing arguments:either 'pattern' or 'judge_func' should be provided")


if __name__ == "__main__":
    print(list(filter_list(["aasdfs", "110dfadf"], "^\d+.*")))
    print(list(filter_list(["8899adf", "1109d09"], "^\d+.*")))
    print(list(filter_list(["eace", "123dfadf"], "^\d+.*")))
    print(list(filter_list(["eace", "123dfadf"])))
    print(judger("1.23").isdigit())
    print(judger("3").isdigit())
