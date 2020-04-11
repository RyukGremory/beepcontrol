import requests


def accion (number=1,accion=''):
    URL = "http://192.168.1.15/?"
    endPoint = URL+'boton'+str(number)+'='+ accion
    requests.get(url = endPoint)