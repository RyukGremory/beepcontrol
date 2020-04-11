import requests


def accion (sentencia):
    URL = 'http://192.168.1.15'
    params = {sentencia[0:3]:sentencia[-1]}
    requests.get(url = URL,params=params)