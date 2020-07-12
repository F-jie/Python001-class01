import json
import ping3
import socket
import argparse
import multiprocessing
from time import time

parser = argparse.ArgumentParser()
parser.add_argument('--f', default='ping', help='Scan mode to be used [default: ping]')
parser.add_argument('--n', type=int, default=4, help='Number of concurrency [default: 4]')
parser.add_argument('--ip', default=None, help='IP address or address block to be scanned [default None]')
parser.add_argument('--w', default=None, help='File used to save the scan result [default None]')
parser.add_argument('--m', default='proc', help='Use multiprocess or multi-thread [default proc]')
parser.add_argument('--v', type=bool, default=False, help='Output the time used in a scanning [default False]')
FLAGS = parser.parse_args()


def check_ip(ip_strs: list):

    for ip_str in ip_strs:
        items = [int(x) for x in ip_str.strip().split('.')]
        try:
            assert len(items) == 4
        except AssertionError:
            return []
        for item in items:
            if -1 < item < 256:
                continue
            else:
                return []
    return ip_strs


def generate_ips(ip_head: str, ip_tail: str):
    ip_list = []
    try:
        assert len(check_ip([ip_head, ip_tail])) != 0
    except AssertionError:
        return []
    ip_head_nus = [int(x) for x in ip_head.strip().split('.')]
    ip_tail_nus = [int(x) for x in ip_tail.strip().split('.')]
    for i in range(3):
        try:
            assert ip_head_nus[i] == ip_tail_nus[i]
        except AssertionError:
            return []
    pre = "{}.{}.{}".format(ip_head_nus[0], ip_head_nus[1], ip_head_nus[2])
    lower = min(ip_head_nus[3], ip_tail_nus[3])
    bigger = max(ip_head_nus[3], ip_tail_nus[3])+1
    for i in range(lower, bigger):
        ip_list.append(pre + '.{}'.format(i))
    return ip_list


def get_ip(ip_input: str) -> list:
    ip_list = []
    if '-' in ip_input:
        ip_block = ip_input.strip().split('-')
        try:
            assert len(ip_block) == 2
        except AssertionError:
            return ip_list
        ip_list = generate_ips(ip_block[0], ip_block[1])
    else:
        tmp = check_ip([ip_input])
        if len(tmp) != 0:
            ip_list.append(tmp[0])
    return ip_list


def ip_scanner(ip):
    response = ping3.ping(ip, timeout=1)
    if FLAGS.w is not None:
        if response:
            return {ip: 1}
        else:
            return {ip: 0}
    else:
        if response:
            print('address: ', ip, ' is accessible!')
        else:
            print('address: ', ip, ' is not accessible!')


def tcp_scanner(info):
    ip = info[0]
    port = info[1]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    if FLAGS.w is not None:
        print("Scanning {}:{}!".format(ip, port))
        if s.connect_ex((ip, port)) == 0:
            return {"{}:{}".format(ip, port): 1}
        else:
            return {"{}:{}".format(ip, port): 0}
    else:
        if s.connect_ex((ip, port)) == 0:
            print('address: ', ip, ':{}'.format(port), ' is accessible!')
        else:
            print('address: ', ip, ':{}'.format(port), ' is not accessible!')


if __name__ == '__main__':
    if FLAGS.v:
        start = time()
    if FLAGS.f == 'ping':
        res = []
        ips = get_ip(FLAGS.ip)
        if len(ips) != 0:
            pool = multiprocessing.Pool(FLAGS.n)
            it = pool.imap(ip_scanner, ips)
            for x in it:
                res.append(x)
            pool.close()
            pool.join()
            with open(FLAGS.w, 'w') as fp:
                json.dump(res, fp)
            print("Exit from main function!")
            pool.terminate()
        else:
            print("Please check the '--ip' param you input!")

    elif FLAGS.f == 'tcp':
        res = []
        if len(get_ip(FLAGS.ip)) != 0:
            ip = get_ip(FLAGS.ip)[0]
            pool = multiprocessing.Pool(FLAGS.n)

            it = pool.imap(tcp_scanner, [[ip, x] for x in range(430, 450)])
            for x in it:
                res.append(x)
            pool.close()
            pool.join()
            with open(FLAGS.w, 'w') as fp:
                json.dump(res, fp)
            print("Exit from main function!")
            pool.terminate()
        else:
            print("Please check the '--ip' param you input!")

    else:
        print("Please check the '--f' param you input!")
    if FLAGS.v:
        print("The time used in this scan is: {}s".format(time() - start))
