import threading
import time


def count_falsh(**kwargs):
    status = str(kwargs).strip('{').strip('}')
    print(status, end='', flush=True)
    print('\b' * len(status))
    time.sleep(.1)


def mutli_coun():
    for i in range(50):
        p1 = threading.Thread(target=count_falsh(a=str(i) + '/s'))
        p1.start()


if __name__ == '__main__':
    mutli_coun()
