import socket
import threading
import time
import requests as rq


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def boardcast_params(client_list=[], data={}):
    # for each client
    threads = []
    ret = [None]*len(client_list)

    def generate_req_fn(client_addr, idx):
        def req():
            resp = rq.post(client_addr, json=data)
            ret[idx] = resp
            print(f'{idx} end')

        return req

    for idx, addr in enumerate(client_list):
        req_fn = generate_req_fn(addr, idx)

        th = threading.Thread(target=req_fn)
        th.start()
        threads.append(th)

    # until all the requests(threads) done
    for th in threads:
        th.join()

    return ret


if __name__ == '__main__':
    client_list = [
        'http://127.0.0.1:3250',
        'http://127.0.0.1:3250',
        'http://127.0.0.1:3250'
    ]

    ret = boardcast_params(client_list, {'data': 'hello'})
    print(ret)
