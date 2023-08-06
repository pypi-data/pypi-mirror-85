import tables as tb

HDF5_COMPRESS_LEVEL = 9


def open_h5file(dest_dir):
    """
    打开h5文件
    :param dest_dir: 目标h5路径
    :param market: 市场，sh，sz
    :param ktype: K线类型 1min，5min,day,分时time,分笔trans
    :return:
    """
    h5file = tb.open_file(dest_dir, "a",
                          filters=tb.Filters(complevel=HDF5_COMPRESS_LEVEL, complib='zlib', shuffle=True))
    return h5file


def get_h5table(h5file, tablename, groupname='data'):
    """
    获取表
    :param h5file: h5文件实例
    :param tablename: 表名
    :param groupname:
    :return:
    """
    try:
        group = h5file.get_node("/", groupname)
    except:
        print('组不存在，创建组')
        group = h5file.create_group("/", groupname)

    try:
        table = h5file.get_node(group, tablename)

        # 也可以点出来
        # table = f.root.groupname.tablename
        # for x in table.iterrows():
    except:
        print(f'表不存在{tablename}')
        return None
        # table = h5file.create_table(group, tablename, H5Record)
    return table


def create_table(h5file, tablename, obj, groupname='data'):
    """
    创建表
    :param h5file:
    :param tablename:
    :param groupname:
    :param obj:
    :return:
    """
    if obj is None:
        print('请输入映射表obj')
        return None
    return h5file.create_table(f'/{groupname}', tablename, obj)


def add_to_table(h5file, table_name: str, data: list = None, obj=None, groupname='data'):
    startDate = 199012191500
    table = get_h5table(h5file, tablename=table_name, groupname=groupname)
    if table is None:
        table = create_table(h5file, tablename=table_name, obj=obj, groupname=groupname)
    # today = datetime.date.today()
    last_datetime = table[-1]['datetime'] if table.nrows > 0 else startDate
    # today_datetime = (today.year * 10000 + today.month * 100 + today.day) * 10000
    print(f'最新记录日期：{last_datetime}')

    add_record_count = 0
    row = table.row
    for item in data:
        if item.datetime_str > last_datetime:
            add_record_count += 1
            row['datetime'] = item.datetime_str
            row['openPrice'] = item.openPrice
            row['highPrice'] = item.highPrice
            row['lowPrice'] = item.lowPrice
            row['closePrice'] = item.closePrice
            row['transAmount'] = item.transAmount
            row['transCount'] = item.transCount
            row.append()  # append把数据写入到I/O buffer中
    if add_record_count > 0:
        table.flush()  # 调用flush函数把数据写入到硬盘中，并且会释放被占用的内存，这样我们就可以处理海量的数据，而不用担心内存不足。
    elif table.nrows == 0:
        table.remove()
    # table.close() 不用关闭
    return add_record_count


class H5Record(tb.IsDescription):
    """
    HDF5基础K线数据格式（日线、分钟线、5分钟线）
    """
    datetime = tb.UInt64Col()  # IGNORE:E1101
    openPrice = tb.Float64Col()  # IGNORE:E1101
    highPrice = tb.Float64Col()  # IGNORE:E1101
    lowPrice = tb.Float64Col()  # IGNORE:E1101
    closePrice = tb.Float64Col()  # IGNORE:E1101
    transAmount = tb.Float64Col()  # IGNORE:E1101
    transCount = tb.Float64Col()  # IGNORE:E1101


class redata:
    datetime_str = 234243243222222
    openPrice = 2222.033
    highPrice = 2222.033
    lowPrice = 2222.033
    closePrice = 2222.033
    transAmount = 2222.033
    transCount = 2222.033


if __name__ == '__main__':
    h5file = open_h5file('D:/sh_day.h5')

    record = []
    for i in range(1000000):
        record.append(redata())

    add_to_table(h5file, table_name='test', obj=H5Record, data=record)
    h5file.close()
