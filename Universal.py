import math

def pattern2int(pattern):
    l = len(pattern)
    n = 0
    for bit in (pattern):
        n = (n << 1) + int(bit)
    return n

def Universal(bits):
    n = len(bits)

    expected_value = [0, 0.73264948, 1.5374383, 2.40160681, 3.31122472,
                      4.25342659, 5.2177052, 6.1962507, 7.1836656,
                      8.1764248, 9.1723243, 10.170032, 11.168765,
                      12.168070, 13.167693, 14.167488, 15.167379]

    variance = [0, 0.690, 1.338, 1.901, 2.358, 2.705, 2.954, 3.125,
                3.238, 3.311, 3.356, 3.384, 3.401, 3.410, 3.416, 3.419, 3.421]

    #L = 5
    L = 2
    if (n >= 387840):
        L = 6
    if (n >= 904960):
        L = 7
    if (n >= 2068480):
        L = 8
    if (n >= 4654080):
        L = 9
    if (n >= 10342400):
        L = 10
    if (n >= 22753280):
        L = 11
    if (n >= 49643520):
        L = 12
    if (n >= 107560960):
        L = 13
    if (n >= 231669760):
        L = 14
    if (n >= 496435200):
        L = 15
    if (n >= 1059061760):
        L = 16

    #Q = 10*(2**L)
    Q = 4
    K = int(math.floor(n/L)) - Q

    p = 2**L

    # c = 0.7 - 0.8/float(L) + (4 + 32/float(L)) * pow(K, -3/float(L))/15
    #
    # sigma = c*math.sqrt(variance[L] / K)

    sqrt2 = math.sqrt(2)
    sum = 0.0
    T=[0]*p
    b = ''.join(bits)
    # for i in range(Q):
    #     decRep = b[i*L:(i+1)*L]
    #     #print(decRep)
    #     idx = pattern2int(decRep)
    #     #print(idx)
    #     T[idx] = i+1
    #
    # for i in range(Q,Q+K):
    #     decRep = b[i*L:(i+1)*L]
    #     j = pattern2int(decRep)
    #     #print(i+1-T[j])
    #     sum += math.log((i+1-T[j]),2)
    #     T[j] = i+1
    # print(sum)
    for i in range(1,Q+1):
        decRep = 0
        for j in range(L):
            decRep += int(bits[(i - 1) * L + j]) * pow(2, L - 1 - j);
            T[decRep] = i


    for i in range(Q,Q+K):
        decRep = 0
        for j in range(L):
            decRep += int(bits[i*L + j]) * pow(2, L - 1 - j);
        sum += math.log(i+1 - T[decRep] , 2)
        T[decRep] = i+1
    #print(sum)

    phi = float(sum/float(K))
    print(phi)
    sigma = math.sqrt(variance[L])
    print(sigma)

    arg = abs(phi-expected_value[L])/(sqrt2 * sigma)
    p = math.erfc(arg)
    print(p)
    success = (p >= 0.01)
    return success, p, None

def change(bits):
    new_bits = []
    n = 10**6
    N = int(n/len(bits))
    for i in range(N):
        new_bits += bits
    m = n - N*len(bits)
    new_bits += bits[:m]
    return new_bits

if __name__ == "__main__":
    bits = ['1', '0', '0', '0', '0', '0', '0', '1', '0', '1', '0', '0', '0', '1', '1', '1', '0', '1', '1', '1', '1',
            '1', '0', '1', '0', '1', '1', '1', '0', '1', '1', '1', '1', '0', '0', '1', '1', '0', '1', '0', '1', '0',
            '1', '1', '1', '1', '0', '1', '0', '1', '0', '1', '0', '0', '1', '1', '1', '0', '0', '0', '1',
            '1', '0', '1', '1', '0', '0', '0', '0', '1', '1', '1', '1', '0', '0', '0', '0', '0', '0', '1', '1', '1',
            '1', '1', '1', '1', '0', '0', '0', '0', '1', '0', '0', '1', '0', '0', '0', '0', '0', '1', '1', '1', '0',
            '1', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1', '0', '1', '0', '0', '1',
            '1', '0', '0', '0', '0', '1', '1', '1', '0', '0', '0', '1', '1', '1', '0', '0', '1', '1', '0', '1', '1',
            '0', '1', '1', '0', '0', '1', '0', '1', '1', '1', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '1',
            '1', '0', '1', '1', '0', '0', '0', '1', '0', '0', '1', '1', '1', '1', '1', '1', '0', '0', '1', '1', '0',
            '0',
            '0', '1', '0', '1', '0', '0', '1', '0', '0', '0', '1', '1', '0', '1', '0', '0', '0', '1', '0', '0', '0',
            '0', '0', '0', '1', '0', '1', '1', '1', '0', '0', '0', '1', '1', '0', '1', '0', '0', '0', '0', '0', '1',
            '1', '1', '0', '0', '1', '0', '1', '0', '1', '1', '0', '0', '0', '1', '0', '1', '1', '0', '1', '1', '1',
            '1', '0']
    # bits='01011010011101010111'
    # bits=list(bits)
    bits = change(bits)
    s1, s2, s3 = Universal(bits)
    if s1 == True:
        print("通过检测,p value is %s" % s2)
    else:
        print("未通过检测")


