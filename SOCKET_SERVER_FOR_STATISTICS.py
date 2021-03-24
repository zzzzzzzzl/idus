import socket
import time


def socket_server_for_statistics(host, num, port):
    result_dict = {}
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('port : ', port)
    s.bind((host, port))
    s.listen(num)
    while True:
        c, addr = s.accept()
        print(addr)
        d = c.recv(1024)
        info = d.decode('utf-8')
        if info != 'over':
            info_list = info.split('--')
            if info_list[0] not in result_dict.keys():
                result_dict[info_list[0]] = int(info_list[1])
            else:
                result_dict[info_list[0]] = result_dict[info_list[0]] + int(info_list[1])
            print(str(result_dict).strip('{').strip('}') + ' time: ' + time.strftime("%Y-%m-%d %H-%M-%S",
                                                                                     time.localtime()))
        else:
            print('The finally result info is :')
            print(str(result_dict).strip('{').strip('}') + ' time: ' + time.strftime("%Y-%m-%d %H-%M-%S",
                                                                                     time.localtime()))
            break


def socket_client_for_statistics(host, str_info, port):
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect((host, port))
    c.send(str_info.encode('utf-8'))


if __name__ == '__main__':
    socket_server_for_statistics('192.168.3.118', 2000, 12345)
