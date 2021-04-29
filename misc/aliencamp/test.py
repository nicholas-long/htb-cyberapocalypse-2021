from pwn import *

p = remote('188.166.156.174', 31860)

def put_back_prompt(data):
    lines = data.split(b'\n')
    last = lines[-1]
    if last.endswith(b'> '):
        p.unrecv(last)

def fix_prompt():
    data = p.recv(timeout=TIMEOUT)
    put_back_prompt(data)

p.sendlineafter('> ', '1')
prompts = p.recvuntil('1.')
prompts += p.recvuntil('> ')
put_back_prompt(prompts)
print(prompts)

promptkeys = prompts.split(b'Here is a little help:\n\n')[1].split(b'\n\n1.')[0]
print(promptkeys)

mappings = {}

tokens = promptkeys.split(b' ')
index = 0
while index < len(tokens) - 2:
    symbol = tokens[index]
    index += 1
    assert(tokens[index] == b'->')
    index += 1
    number = tokens[index]
    index += 1
    mappings[symbol] = number

print(mappings)

p.sendlineafter('> ', '2') # take test
preamble = p.recvuntil('\n\n')

for i in range(500):
    prompt = p.recvuntil(': ')
    print(prompt)
    question = prompt.split(b'\n\n')[1]
    print(question)
    for key in mappings:
        question = question.replace(key, mappings[key])

    print(question)
    q = question.split(b' = ')[0].decode('latin-1')
    answer = eval(q)
    print(answer)
    p.sendline(f"{answer}")
    time = p.recvuntil(': ')

p.interactive()