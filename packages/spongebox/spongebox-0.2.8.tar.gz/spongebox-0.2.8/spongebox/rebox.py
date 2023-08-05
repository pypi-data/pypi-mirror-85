import re


class judger:

    def __init__(self, suspect):
        self.suspect = suspect

    def isdigit(self):
        return False if re.match("^\d+\.\d+$|^\d+$", self.suspect) == None else True


def filter_list(lst, exp):
    match = [re.search(exp, item) for item in lst]
    return [item.group() for item in match if item is not None]


if __name__ == "__main__":
    print(filter_list(["aasdfs", "110dfadf"], "^\d+.*"))
    print(filter_list(["8899adf", "1109d09"], "^\d+.*"))
    print(filter_list(["eace", "123dfadf"], "^\d+.*"))
    print(judger("1.23").isdigit())
    print(judger("3").isdigit())
