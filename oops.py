fp = open('ScaryJunk.plain', 'w+b')
byte_arr = [0 for _ in range(60000)]
for i in range(1, 256):
    byte_arr.append(i)
fp.write(bytearray(byte_arr))