import threading
from time import sleep


def print1():
    while True:
        print(1)
        sleep(1)


def print2():
    while True:
        print(2)
        sleep(1)


class Thread1(threading.Thread):
    def run(self) -> None:
        print1()


class Thread2(threading.Thread):
    def run(self) -> None:
        print2()


if __name__ == '__main__':
    thread1 = Thread1()

    thread2 = Thread2()

    thread1.start()
    thread2.start()
