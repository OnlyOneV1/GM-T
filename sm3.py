# -*- coding: utf-8 -*-
import binascii

IV="7380166f 4914b2b9 172442d7 da8a0600 a96f30bc 163138aa e38dee4d b0fb0e4e".replace(" ", "")
a = []
for i in range(8):
     a.append(int(IV[i*8 :(i+1)*8], 16))
IV = a

T_j = [0x79cc4519]*16 + [0x7a879d8a]*48


# 将list数据拼成字节流
def bytesFromList(hashlist):
    bytesStream = b''
    for i in hashlist:
        bytesStream += i.to_bytes(4, byteorder='big', signed=False)

    return bytesStream


# 循环左移k位
def rotate_left(a, k):
    k = k % 32
    return ((a << k) & 0xFFFFFFFF) | ((a & 0xFFFFFFFF) >> (32 - k))


# 布尔算子：FF
def FF_j(X, Y, Z, j):
    if 0 <= j and j < 16:
        ret = X ^ Y ^ Z
    elif 16 <= j and j < 64:
        ret = (X & Y) | (X & Z) | (Y & Z)

    return ret


# 布尔算子：GG
def GG_j(X, Y, Z, j):
    if 0 <= j and j < 16:
        ret = X ^ Y ^ Z
    elif 16 <= j and j < 64:
        ret = (X & Y) | ((~ X) & Z)

    return ret


# 置换算子：P0
def P_0(X):
    return X ^ (rotate_left(X, 9)) ^ (rotate_left(X, 17))


# 置换算子：P1
def P_1(X):
    return X ^ (rotate_left(X, 15)) ^ (rotate_left(X, 23))


# 压缩CF
def CF(V_i, B_i):
    W = []
    for j in range(16):
        W.append(int.from_bytes(B_i[j * 4:(j + 1) * 4], 'big'))
    for j in range(16, 68):
        W_j = P_1(W[j - 16] ^ W[j - 9] ^ (rotate_left(W[j - 3], 15))) ^ (rotate_left(W[j - 13], 7)) ^ W[j - 6]
        W.append(W_j)

    W_1 = []
    for j in range(64):
        W_1.append(W[j] ^ W[j + 4])

    A, B, C, D, E, F, G, H = V_i
    for j in range(64):
        SS1 = rotate_left(((rotate_left(A, 12)) + E + (rotate_left(T_j[j], j))) & 0xFFFFFFFF, 7)
        SS2 = SS1 ^ (rotate_left(A, 12))
        TT1 = (FF_j(A, B, C, j) + D + SS2 + W_1[j]) & 0xFFFFFFFF
        TT2 = (GG_j(E, F, G, j) + H + SS1 + W[j]) & 0xFFFFFFFF
        D = C
        C = rotate_left(B, 9)
        B = A
        A = TT1
        H = G
        G = rotate_left(F, 19)
        F = E
        E = P_0(TT2)

        A = A & 0xFFFFFFFF
        B = B & 0xFFFFFFFF
        C = C & 0xFFFFFFFF
        D = D & 0xFFFFFFFF
        E = E & 0xFFFFFFFF
        F = F & 0xFFFFFFFF
        G = G & 0xFFFFFFFF
        H = H & 0xFFFFFFFF

    V_i_1 = [A ^ V_i[0], B ^ V_i[1], C ^ V_i[2], D ^ V_i[3],
             E ^ V_i[4], F ^ V_i[5], G ^ V_i[6], H ^ V_i[7]]

    return V_i_1


# 输入数据类型应为字节流
def sm3(msg_bytes):
    msg_len = len(msg_bytes)
    msg_list = []
    i = -1
    # 按512位分组
    for i in range(msg_len // 64):
        msg_list.append(msg_bytes[i * 64:(i + 1) * 64])

    i += 1
    rest_len = msg_len % 64
    if (rest_len < 56):  # 剩余位数小于448位，只需再加1组
        # 补1个1和若干个0
        tmpMsg = msg_bytes[i * 64:] + b'\x80' + b'\x00' * (55 - rest_len)
        # 补8字节，数值为参与hash数据的总位数
        tmpMsg += (msg_len * 8).to_bytes(8, byteorder='big', signed=False)
        msg_list.append(tmpMsg)
    else:  # 剩余位数超过448位，需要再加2组
        # 补1个1和若干个0，直到补满512位
        tmpMsg = msg_bytes[i * 64:] + b'\x80' + b'\x00' * (63 - rest_len)
        msg_list.append(tmpMsg)

        # 前面补56字节的0，再填写总位数
        tmpMsg = b'\x00' * 56 + (msg_len * 8).to_bytes(8, byteorder='big', signed=False)
        msg_list.append(tmpMsg)

    V = IV
    for msg in msg_list:
        V = CF(V, msg)

    return bytesFromList(V)

def change(bits):
    new_bits = []
    n = 10**6
    N = int(n/len(bits))
    for i in range(N):
        new_bits += bits
    m = n - N*len(bits)
    new_bits += bits[:m]
    return new_bits



if __name__ ==  '__main__':
    msgStr = "Beijing University of Posts and Telecommunications".replace(" ", "")
    print(msgStr)
    msg = msgStr.encode()  # 输入 ASCII字符串转为字节流
    y = sm3(msg)
    print(y)
    y=binascii.hexlify(y)
    m = int(y,16)
    r = bin(m).replace('0b', '')
    print(m)

   #  bits = change(list(r))
   #
   # # print(bits)
   #  print(len(bits))



