import requests as rq
import ipfshttpclient as ipfs

firstline = 10
insert = 10


def fn():
    print('call')


res = rq.get(
    'https://bafybeibzzmt5yvyitoivhvk4pi5go7iwq4q2pyk5dynl734f52ccsfb2py.ipfs.dweb.link/cifar10_model.json')

print(res.status_code)
if res.status_code == 200:
    print(len(res.json()['params']))
else:
    print('error')

# client = ipfs.connect()
# client.pin.add('bafybeibzzmt5yvyitoivhvk4pi5go7iwq4q2pyk5dynl734f52ccsfb2py')
# pin_list = client.pin.ls(type="recursive")
# print(pin_list)
