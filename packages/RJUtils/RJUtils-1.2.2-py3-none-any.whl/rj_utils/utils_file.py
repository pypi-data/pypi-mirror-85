def save_to_csv_file(data, filepathWithName: str):
    """

    :param data:
    :param filepathWithName: 'c:/houseInfo.csv'
    :return:
    """
    # with open('houseInfo.txt', 'a', encoding='utf-8') as f:
    #     f.write(str(data) + '\n')
    with open(filepathWithName, 'w+', encoding='utf-8', newline='') as f:
        import csv
        # writer = csv.DictWriter(f, ['name', 'phone', 'addr', 'price'])
        writer = csv.writer(f)
        writer.writerow(data)


def save_to_file(data, filepath: str):
    with open(filepath, 'w+', encoding='utf-8') as f:
        f.write(str(data))
        f.write('\n')


def removeFile(filepathWithName: str):
    """
    删除文件
    :param filepathWithName: 'c:/houseInfo.csv'
    :return:
    """
    import os
    if os.path.exists(filepathWithName):
        os.remove(filepathWithName)


def data2json2file(data, filepathWithName: str):
    """
    数据转json保存到文件
    :param data:list或dict类型，支持序列化json的类型
    :param filePath:保存的文件位置，'c:/houseInfo.txt'
    :return:
    """
    with open(filepathWithName, 'w') as file:
        import json
        bJson = json.dumps(data, ensure_ascii=False)  # dict转json
        file.writelines(bJson)


def file2dict(filepathWithName: str):
    """
    从文件读取json数据转dict
    :param path:'c:/conf/tt.conf'
    :return:dict
    """
    # 读取配置文件
    with open(filepathWithName) as f:
        import json
        return json.load(f)
