# 信号处理程序
import signal
from time import sleep


def sigintHandler(signum, frame):
    print("中断发生。")
    # 需要最后做的事情
    print("执行最后的清理工作。")
    # 停止异步数据接收
    exit()


def registSignal(fun=sigintHandler):
    # 信号捕捉程序必须在循环之前设置
    signal.signal(signal.SIGINT, fun)  # 由Interrupt Key产生，通常是CTRL+C或者DELETE产生的中断
    # signal.signal(signal.SIGHUP, fun)  # 发送给具有Terminal的Controlling Process，当terminal 被disconnect时候发送
    signal.signal(signal.SIGTERM, fun)  # 请求中止进程，kill命令缺省发送
    # signal.signal(signal.SIGQUIT, fun)  # 终止进程 按 ctrl+\或者ctrl+D
    # signal.signal(signal.SIGTSTP, fun)  # 终止进程 终端来的停止信号
    # signal.signal(signal.SIGKILL, fun)  # 终止进程 无法捕获或忽略


if __name__ == "__main__":
    registSignal()

    while True:
        sleep(60 * 60 * 24)
