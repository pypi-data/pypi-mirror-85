def get_node_by_class(html, classname):
    """
    获取html页面classname对应的节点
    :param html:
    :param classname:
    :return:
    """
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    page_num = soup.find(class_=classname).text
    return int(page_num)
