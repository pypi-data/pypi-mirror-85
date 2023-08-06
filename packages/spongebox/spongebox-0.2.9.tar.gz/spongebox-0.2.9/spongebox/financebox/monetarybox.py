import spongebox.structbox as structbox
import re


class chinesemonetary:

    def __init__(self, min_unit="fen"):
        self.min_unit = "fen"

    def decompose_amount(self, cn_amount):
        if len(cn_amount) <= 1:
            return cn_amount
        # print(cn_amount)
        pattern = "(?P<yi>.*亿)*(?P<wan>.*万)*(?P<qian>.*[千仟])*(?P<bai>.*[百佰])*(?P<shi>.*[十拾])*(?P<yuan>.*[元圆块])*"
        grp_keys = ["yi", "wan", "qian", "bai", "shi", "yuan"]
        units = ["亿", "万", "仟千", "佰百", "拾十", "元圆块"]
        if self.min_unit == "fen":
            pattern += "(?P<jiao>.*[角毛])*(?P<fen>.*分)*"
            grp_keys.extend(["jiao", "fen"])
            units.extend(["角毛", "分"])
        elif self.min_unit == "yuan":
            pass
        else:
            raise Exception("min unit should be:yuan or fen")
        pattern += "(?P<tbd>.*)"
        grp_keys.append("tbd")

        _ = re.search(pattern, cn_amount)
        ret = [_.group(k) for k in grp_keys]
        # print(ret)

        only_tbd = True
        for p in ret[:-1]:
            if p != None:
                only_tbd = False
                break
        if only_tbd:
            return list(ret[-1] + "零零")

        ret = [amt if amt != None else "" for amt in ret]
        print(ret)

        def switch(i, stop):
            if ret[i - 1] == "" and i > stop:
                ret[i - 1], ret[i] = ret[i], ret[i - 1]
                switch(i - 1, stop)
            else:
                pass

        if ret[-1] != "":
            stop = 0 - len(ret)
            if "零" in ret[-1]:
                if self.min_unit == "fen":
                    stop = -4
                else:
                    stop = -2
            switch(-1, stop)

        self.min_unit = "yuan"

        # print(units)
        for i in range(0, len(ret) - 1):
            for unit in units[i]:
                ret[i] = ret[i].replace(unit, "")
        ret = [x.lstrip("零") for x in ret]
        ret = [x if x != "" else "零" for x in ret]
        ret[1] = self.decompose_amount(ret[1])[-4:]
        # ret = flatten_list(ret)
        ret[0] = self.decompose_amount(ret[0])
        ret = [x if x != "" else "零" for x in ret]
        print(ret[:-1])
        print()
        return ret[:-1]

    def digitalize_chinese_moneytary(self, cn_amount):
        print(cn_amount)
        if cn_amount == "":
            return -1
        cn_num = {'零': 0, '壹': 1, '贰': 2, '叁': 3, '肆': 4, '伍': 5, '陆': 6, '柒': 7, '捌': 8,
                  '玖': 9, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '两': 2}
        ret = ""
        _ = ""
        if len(cn_amount) == 1:
            _ = cn_amount + "零零"
        else:
            _ = self.decompose_amount(cn_amount)
            _ = "".join(structbox.flatten_list(_))
        for n in _:
            ret += str(cn_num[n])
        ret = int(ret)
        print(ret)
        print()
        return ret


if __name__ == "__main__":
    _ = []

    _.append(chinesemonetary().digitalize_chinese_moneytary("玖仟捌佰柒拾陆万伍仟肆佰叁拾贰亿壹仟零玖拾捌万柒仟陆佰伍拾肆元叁角贰分") == 987654321098765432)
    _.append(chinesemonetary().digitalize_chinese_moneytary("柒仟陆佰伍拾肆元叁角贰分") == 765432)
    _.append(chinesemonetary().digitalize_chinese_moneytary("柒仟陆佰伍拾肆元贰分") == 765402)
    _.append(chinesemonetary().digitalize_chinese_moneytary("一千零四") == 100400)
    _.append(chinesemonetary().digitalize_chinese_moneytary("一千零四拾") == 104000)
    _.append(chinesemonetary().digitalize_chinese_moneytary("一千零四拾五") == 104500)
    _.append(chinesemonetary().digitalize_chinese_moneytary("一块两毛二") == 122)
    _.append(chinesemonetary().digitalize_chinese_moneytary("三百四") == 34000)
    _.append(chinesemonetary().digitalize_chinese_moneytary("三百零四") == 30400)
    _.append(chinesemonetary().digitalize_chinese_moneytary("三百零四块") == 30400)
    _.append(chinesemonetary().digitalize_chinese_moneytary("三千叁佰万") == 3300000000)
    _.append(chinesemonetary().digitalize_chinese_moneytary("二十") == 2000)
    _.append(chinesemonetary().digitalize_chinese_moneytary("一块二") == 120)
    _.append(chinesemonetary().digitalize_chinese_moneytary("三毛一") == 31)
    _.append(chinesemonetary().digitalize_chinese_moneytary("三块") == 300)
    _.append(chinesemonetary().digitalize_chinese_moneytary("三百") == 30000)
    _.append(chinesemonetary().digitalize_chinese_moneytary("三") == 300)
    _.append(chinesemonetary().digitalize_chinese_moneytary("壹二三") == 12300)
    _.append(chinesemonetary().digitalize_chinese_moneytary("九八三四") == 983400)
    _.append(chinesemonetary().digitalize_chinese_moneytary("肆万") == 4000000)
    _.append(chinesemonetary().digitalize_chinese_moneytary("肆万二") == 4200000)

    print(_)
