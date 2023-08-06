import re


def filter_list(lst, exp):
    match = [re.search(exp, item) for item in lst]
    return [item.group() for item in match if item is not None]


if __name__ == "__main__":
    print(filter_list(["aasdfs", "110dfadf"], "^\d+.*"))
    print(filter_list(["8899adf","1109d09"], "^\d+.*"))
    print(filter_list(["eace", "123dfadf"], "^\d+.*"))
