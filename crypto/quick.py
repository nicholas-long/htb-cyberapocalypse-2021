h = '2e313f2702184c5a0b1e321205550e03261b094d5c171f56011904'

data = b'\x2e\x31\x3f\x27\x02\x18\x4c\x5a\x0b\x1e\x32\x12\x05\x55\x0e\x03\x26\x1b\x09\x4d\x5c\x17\x1f\x56\x01\x19\x04'

known = b'CHTB{'

key = b''
for i in range(5):
    key += bytes([ data[i] ^ known[i]])

print(key)

result = b''

index = 0
for b in data:
    result += bytes[b ^ key]
    index = (index + 1)%5 