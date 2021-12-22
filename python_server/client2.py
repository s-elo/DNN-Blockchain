import requests
import time

SERVER_DOMAIN = 'http://localhost'
SERVER_PORT = '5000'

resp = requests.get(f'{SERVER_DOMAIN}:{SERVER_PORT}/cifar10')

print(resp.json())
