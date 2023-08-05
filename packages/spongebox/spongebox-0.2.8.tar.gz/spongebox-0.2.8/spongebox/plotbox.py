import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# 支持中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
sns.set(font='SimHei')  # 解决Seaborn中文显示问题


def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2. -
                 0.2, 1.03 * height, '%s' % float(height))


def countplot(x, data, hue=None, prop=False, sort_by="count", ascending=False):
    _ = data.fillna("").groupby(x).count().reset_index()
    # print(_.head(1))
    _.rename(columns={_.columns[1]: "count"}, inplace=True)
    if sort_by != None:
        _.sort_values(sort_by, ascending=ascending, inplace=True)
        _.reset_index(inplace=True, drop=True)
    # print(_.head(1))
    total = _.iloc[:, 1].sum() * 1.0
    _["display"] = _.iloc[:, 1]
    if prop:
        _["display"] = _.iloc[:, 1].apply(
            lambda x: str(int(round(x / total * 100))) + "%")
    # add fake col to normalize the bar's sequences
    _[" "+x+" "] = _[x].apply(lambda x:""+str(x))
    g = sns.barplot(x=" "+x+" ", y=_.columns[1], data=_, hue=hue)
    # 在柱状图的上面显示各个类别的数量
    for index, row in _.iterrows():
        # 在柱状图上绘制该类别的数量
        g.text(row.name, row[1], row.display, color="black", ha="center")


if __name__ == "__main__":
    # l1 = [68, 96, 85, 86, 76, 87, 95]
    # l2 = [85, 68, 79, 89, 94, 82, 90]
    #
    # name = ['A', 'B', 'C', 'D', 'E', 'F', 'E']
    # total_width, n = 0.8, 2
    # width = total_width / n
    # x = [0, 1, 2, 3, 4, 5, 6]
    #
    # a = plt.bar(x, l1, width=width, label='数学', fc='y')
    # for i in range(len(x)):
    #     x[i] = x[i] + width
    # b = plt.bar(x, l2, width=width, label='语文', tick_label=name, fc='r')
    #
    # print(type(b))
    #
    # autolabel(a)
    # autolabel(b)
    #
    # plt.xlabel('学生')
    # plt.ylabel('成绩')
    # plt.title('学生成绩')
    # plt.legend()
    # plt.show()

    # def classify(x):
    #     if x == 0:
    #         return "差"
    #     elif x == 1:
    #         return "中"
    #     else:
    #         return "好"
    #
    #
    # def subject(x):
    #     if x == 0:
    #         return "文科"
    #     else:
    #         return "理科"
    #
    #
    # df = pd.DataFrame(np.random.randint(0, 3, (10, 2)), columns="语文,数学".split(","))
    # df["语文"] = df["语文"].apply(lambda x: classify(x))
    # df["数学"] = df["数学"].apply(lambda x: classify(x))
    # df["分科"] = df["语文"].apply(lambda x: subject(np.random.randint(0, 2)))
    # print(df)
    #
    # plt.subplot(1, 2, 1)
    # sns.countplot(x="语文", data=df)
    # plt.subplot(1, 2, 2)
    # sns.countplot(x="语文", hue="分科", data=df)
    # plt.show()
    #
    # countplot(x="语文", data=df, prop=True)
    # plt.show()
    #
    # sns.countplot(x="语文", hue="分科", data=df)
    # plt.show()

    df = pd.DataFrame(np.random.randint(0,10,(10,3)),columns=list("abc"))
    countplot("a",df)
    plt.show()
