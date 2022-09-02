import math
from scipy.special import gamma, gammainc, gammaincc

def help(bits,n,m):
    for i in range(m - 1):
        bits.append(bits[i])

    bit = ''.join(bits)
    dic = {}
    res = [0] * (2 ** m)
    for k in range(n):

        if  bit[k:k+m] in dic:
                dic[bit[k:k+m]] += 1
        else:
            dic[bit[k:k+m]] = 1

    k = len(dic)
    sum = 0.0

    for value in dic.values():
        x = value / n
        sum += x * math.log(x, math.e)
    #print(sum)
    return sum


def ApproximateEntropy(bits):
    n = len(bits)
    m = 3

    sum1 = help(bits,n,m)
    sum2 = help(bits,n,m+1)
    v = 2*n*(math.log(2,math.e) - (sum1-sum2))
    #print(v)
    p = gammaincc(2**(m-1), v/2.0)
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
    # bits = ['1', '0', '0', '0', '0', '0', '0', '1', '0', '1', '0', '0', '0', '1', '1', '1', '0', '1', '1', '1', '1',
    #         '1', '0', '1', '0', '1', '1', '1', '0', '1', '1', '1', '1', '0', '0', '1', '1', '0', '1', '0', '1', '0',
    #         '1', '1', '1', '1', '0', '1', '0', '1', '0', '1', '0', '0', '1', '1', '1', '0', '0', '0', '1',
    #         '1', '0', '1', '1', '0', '0', '0', '0', '1', '1', '1', '1', '0', '0', '0', '0', '0', '0', '1', '1', '1',
    #         '1', '1', '1', '1', '0', '0', '0', '0', '1', '0', '0', '1', '0', '0', '0', '0', '0', '1', '1', '1', '0',
    #         '1', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1', '0', '1', '0', '0', '1',
    #         '1', '0', '0', '0', '0', '1', '1', '1', '0', '0', '0', '1', '1', '1', '0', '0', '1', '1', '0', '1', '1',
    #         '0', '1', '1', '0', '0', '1', '0', '1', '1', '1', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '1',
    #         '1', '0', '1', '1', '0', '0', '0', '1', '0', '0', '1', '1', '1', '1', '1', '1', '0', '0', '1', '1', '0',
    #         '0',
    #         '0', '1', '0', '1', '0', '0', '1', '0', '0', '0', '1', '1', '0', '1', '0', '0', '0', '1', '0', '0', '0',
    #         '0', '0', '0', '1', '0', '1', '1', '1', '0', '0', '0', '1', '1', '0', '1', '0', '0', '0', '0', '0', '1',
    #         '1', '1', '0', '0', '1', '0', '1', '0', '1', '1', '0', '0', '0', '1', '0', '1', '1', '0', '1', '1', '1',
    #         '1', '0']
    #bits = change(bits)
    bits='0100110101'
    bits=list(bits)
    s1, s2, s3 = ApproximateEntropy(bits)
    if s1 == True:
        print("通过检测,p value is %s" % s2)
    else:
        print("未通过检测")