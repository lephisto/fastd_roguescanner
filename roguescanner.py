"""
    FastD Roguescanner

    Author: Bastian Maeuser
    https://github.com/lephisto/roguescanner

    You will need python3-requests module installed.

"""

import os
import json
import requests
import socket
from roguescannerconfig import *


def analyze(j):
    for p in j['peers']:
        mac = j['peers'][p]['connection']['mac_addresses'][0]
        ip = j['peers'][p]['address']
        print("Key:" + p + " MAC:" + mac, end=' ')
        for s in links:
            if s['source_addr'] == mac:
                print("Found as Source: " + s['source'], end = ' ')
                for n in nodes:
                    if n['node_id'] == s['source']:
                        print("Hostname:" + n['hostname'] + " (" + ip + ")")
            elif s['target_addr'] == mac:
                print("Found as Target: " + s['target'], end = ' ')
                for n in nodes:
                    if n['node_id'] == s['target']:
                        print("Hostname:" + n['hostname'] + " (" + ip + ")")


# Read MV Json
response = requests.get(mvjson)
json_response = response.json()
nodes = json_response['nodes']
links = json_response['links']

# Read FastD Status Socket
for fd_socket in fastd_sockets:
    result = b''
    if os.path.exists(fd_socket):
        print(fd_socket)
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.connect(fd_socket)
        while True:
            data = s.recv(128)
            if data:
                result += data
            else:
                break

    fd_json = json.loads(result.decode('utf-8'))
    analyze(fd_json)
