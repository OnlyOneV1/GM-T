import math
from scipy.special import gamma, gammainc, gammaincc


def change(n,m):
    if len(n) < m:
        r = '0'*(m-len(n)) + n
    else:
        r = n
    return r
def helper(m,n,bits):
    res = [0]*(2**m)
    for i in range(2**m):
        r = bin(i).replace('0b', '')
        r = change(r,m)
        s = list(r)
        for j in range(m-1,n+m):
            if s == bits[j-m:j]:
                res[i] +=1
    sum = 0
    for k in range(2**m):
        sum += res[k]**2
    result = (2**m/n) * sum - n
    return result


def Serial(bits):
    m = 3
    n = len(bits)
    new_bits = bits
    for i in range(m-1):
        new_bits.append(bits[i])
    new_n = n+m-1
    psim0 = helper(m, n, new_bits)
    psim1 = helper(m-1, n, new_bits)
    psim2 = helper(m-2, n, new_bits)


    del1 = psim0 - psim1
    del2 = psim0 - 2.0 * psim1 + psim2

    p_value1 =  gammaincc(2**(m-1)/2,del1/2.0)
    p_value2 =  gammaincc(2**(m-2)/2,del2/2.0)

    success = False
    if p_value1 >= 0.01 and p_value2 >= 0.01:
        success = True
    return success, None, [p_value1,p_value2]


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
    bits = '0011011101'
    bits = list(bits)
        #serial_test(bits)
    s1, s2 ,s3 = Serial(bits)
    print(s3)
    if s1 == True:
        print("通过检测")
    #     print("p value1 is %s" % s2)
    #     print("p value2 is %s" % s3)
    # else:
    #     print("未通过检测")