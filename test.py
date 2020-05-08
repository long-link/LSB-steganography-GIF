import struct
import os
# a = 5
# b = 2
# for a in range(4):
#     b += a
#     print(b)
# b = [0, 4, 5, 7]
# a = "qwe"
# c = a[:-2]
# a = a[2:]
# print(c)
# a = a.encode('utf-8')

# c = '9'
# a = 'asd'
# binary_message = bin(int.from_bytes(c.encode('utf-8'), byteorder='big'))
# print(binary_message)
# c = b'a'
# print(c.decode('utf-8'))
# a = int.from_bytes(c, byteorder='big')
# a = bin(a)
#
# print(a)
#
# b = '01100001'
# a = int(b, 2).to_bytes(1, byteorder='big')
# print(a)

# b = 0b10
# a = b.to_bytes(1, byteorder='big')
# print(a)
# e = 0b0 + 10
# print(struct.pack(">b", b))
# 0b110001

# array_bytes = []
# with open('image.gif', 'rb') as file:
#     while True:
#         byte = file.read(1)
#         if byte:
#             array_bytes.append(byte)
#         else:
#             break
#
# file2 = "popka"
#
# with open(os.path.join("C:\\Users\\evgen\\PycharmProjects\\steganographyGIF", file2 + ".gif"), "wb") as f:
#     # f.write(chr(array_bytes))
#     #f = "".join([chr(i) for i in array_bytes])
#     #f.append([int(i) for i in array_bytes])
#     for i in array_bytes:
#         f.write(i)

# def pisya(a):
#     if a == 2:
#         return True
#     return 5
#
# qw = 3
# b = pisya(qw)
# if not b:
#     print(b)
# else:
#     print(b)
#
# errors = {
#     2: 'qwe',
#     4: 'asd',
#     5: 'zxc',
#     8: 'rty',
#     9: 'fgh'
# }
#
# print(errors[b])

def read_bytes(file_name):
    try:
        array_bytes = []
        with open(file_name, 'rb') as file:
            while True:
                byte = file.read(1)
                if byte:
                    array_bytes.append(byte)
                else:
                    break
        return array_bytes
    except FileNotFoundError:
        pass

print(read_bytes(''))