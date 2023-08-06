import json


def getJsonFromFile(filepath):
    """

    :param filepath: json文件路径
    :return:
    """
    f = open(filepath, encoding='utf-8')
    msg = f.read()  # 使用loads（）方法需要先读文件 loads() 传的是字符串，而load()传的是文件对象
    import json
    user_dic = json.loads(msg)
    return user_dic


def dictToJson(dict_oj):
    """
    字典转json
    :param disc:{'xiaojun':'123456','xiaohei':'7891','abc':'11111'}
    :return:
    """
    import json
    res = json.dumps(dict_oj, ensuer_ascii=False)  # 含有中文要ensuer_ascii=False
    return res


def listToJson(lst):
    """
    复杂list 转成Json格式数据
    :param lst:
    :return:
    """
    import json
    import numpy as np
    keys = [str(x) for x in np.arange(len(lst))]
    list_json = dict(zip(keys, lst))
    str_json = json.dumps(list_json, indent=2, ensure_ascii=False)  # json转为string
    return str_json


def dictToFile(dict_oj, filepath):
    """

    :param dist: 字典
    :param filepath: 'c:/filepath/stus2.json'
    :return:
    """
    f = open(filepath, 'w', encoding='utf-8')
    import json
    json.dump(dict_oj, f, ensure_ascii=False)


def dictToFile2(dict_oj, filepath):
    """

    :param dist: {'xiaojun': '123456', 'xiaohei': '7890', 'lrx': '111111'}
    :param filepath: 'c:/filepath/stus2.json'
    :return:
    """
    import json
    res = json.dumps(dict_oj, indent=8, ensuer_ascii=False)
    with open(filepath, 'w', encoding='utf-8') as f:  # 使用.dumps()方法是要使用.write()方法写入
        f.write(res)


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        import decimal
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)


def specialDateToJson(dict_oj):
    """
    字典转json，包含特殊Decimal数据使用自定义解析器
    :param dist:
    :return:
    """
    return json.dumps(dict_oj, cls=DecimalEncoder)
