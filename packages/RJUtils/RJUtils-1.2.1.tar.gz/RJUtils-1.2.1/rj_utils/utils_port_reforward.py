import socket
import threading

"""
端口转发
"""

"""
端口映射配置信息

入口-> 本地接收地址 -> 远端监听地址
"""
# 接收数据缓存大小
PKT_BUFF_SIZE = 2048


# 调试日志封装
def __send_log(content):
    print(content)


def __tcp_mapping_worker(conn_receiver, conn_sender):
    """
    单向流数据传递
    :param conn_receiver: 接收socket
    :param conn_sender: 发送socket
    :return:
    """
    while True:
        try:
            data = conn_receiver.recv(PKT_BUFF_SIZE)
        except Exception:
            __send_log('Event: Connection closed.')
            break

        if not data:
            __send_log('Info: No more data is received.')
            break

        try:
            conn_sender.sendall(data)
        except Exception:
            __send_log('Error: Failed sending data.')
            break

        # send_log('Info: Mapping data > %s ' % repr(data))
        __send_log('Info: Mapping > %s -> %s > %d bytes.' % (
            conn_receiver.getpeername(), conn_sender.getpeername(), len(data)))

    conn_receiver.close()
    conn_sender.close()

    return


def __tcp_mapping_request(local_conn, remote_ip, remote_port):
    """
    端口映射请求处理
    :param local_conn:
    :param remote_ip:
    :param remote_port:
    :return:
    """
    remote_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        remote_conn.connect((remote_ip, remote_port))
    except Exception:
        local_conn.close()
        __send_log('Error: Unable to connect to the remote server.')
        return

    threading.Thread(target=__tcp_mapping_worker, args=(local_conn, remote_conn)).start()
    threading.Thread(target=__tcp_mapping_worker, args=(remote_conn, local_conn)).start()

    return


def tcp_mapping(remote_ip, remote_port, local_ip, local_port):
    """
    端口映射函数
    :param remote_ip:
    :param remote_port:
    :param local_ip:
    :param local_port:
    :return:
    """
    local_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    local_server.bind((local_ip, local_port))
    local_server.listen(5)

    __send_log('Event: Starting mapping service on ' + local_ip + ':' + str(local_port) + ' ...')

    while True:
        try:
            (local_conn, local_addr) = local_server.accept()
        except Exception:
            local_server.close()
            __send_log('Event: Stop mapping service.')
            break

        threading.Thread(target=__tcp_mapping_request, args=(local_conn, remote_ip, remote_port)).start()
        __send_log('Event: Receive mapping request from %s:%d.' % local_addr)
    return


# 主函数
if __name__ == '__main__':
    # 远端监听地址
    CFG_REMOTE_IP = '127.0.0.1'
    CFG_REMOTE_PORT = 10001

    # 本地接收地址
    CFG_LOCAL_IP = '127.0.0.1'
    CFG_LOCAL_PORT = 10035
    tcp_mapping(CFG_REMOTE_IP, CFG_REMOTE_PORT, CFG_LOCAL_IP, CFG_LOCAL_PORT)
