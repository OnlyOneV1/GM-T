from __future__ import print_function
from sm3 import sm3
import binascii
def get_bits(s):
    msgStr = s
    msg = msgStr.encode()  # 输入 ASCII字符串转为字节流
    y = sm3(msg)
    y = binascii.hexlify(y)
    m = int(y, 16)
    r = bin(m).replace('0b', '')
    return list(r)

def change(bits):
    new_bits = []
    n = 10**6
    N = int(n/len(bits))
    for i in range(N):
        new_bits += bits
    m = n - N*len(bits)
    new_bits += bits[:m]
    return new_bits


import argparse
import sys
parser = argparse.ArgumentParser(description='15 test methods were used to detect the randomness of sm3 output data.')
parser.add_argument('-sm3', type=str,help='Use SM3 for encryption')
parser.add_argument('-t', '--testname', nargs='?',default='None', help='Select the test to run. Defaults to running all tests. Use --list_tests to see the list')
parser.add_argument('--list_tests', action='store_true',help='Display the list of tests')

args = parser.parse_args()

testlist = [
        'ApproximateEntropy',
        'Autocorrelation',
        'binaryDerivate',
        'blockFrequency',
        'Cusum',
        'DiscreteFourierTransform',
        'Frequency',
        'LinearComplexity',
        'LongestRunOfOnes',
        'Matrix',
        'poker',
        'Runs',
        'Serial',
        'Universal',
        'RunsDistribution']

if args.sm3:
    bits = get_bits(args.sm3)
    print(bits)
    file = open('test.txt', mode='w')
    file.writelines(bits)
    file.close()



print("-----Output Randomness Detection-----")
if args.list_tests:

    for i, testname in zip(range(len(testlist)), testlist):
        print(str(i + 1).ljust(4) + ": " + testname)
    exit()

if args.testname:
    if args.testname in testlist:
        m = __import__(args.testname)
        func = getattr(m, args.testname)
        print("TEST: %s" % args.testname)
        file = open('test.txt', mode='r')
        bits = file.readline()
        # bits = ['1', '0', '0', '0', '0', '0', '0', '1', '0', '1', '0', '0', '0', '1', '1', '1', '0', '1', '1', '1', '1',
        #         '1', '0', '1', '0', '1', '1', '1', '0', '1', '1', '1', '1', '0', '0', '1', '1', '0', '1', '0', '1', '0',
        #         '1', '1', '1', '1', '0', '1', '0', '1', '0', '1', '0', '0', '1', '1', '1', '0', '0', '0', '1', '1', '0',
        #         '1', '1', '0', '0', '0', '0', '1', '1', '1', '1', '0', '0', '0', '0', '0', '0', '1', '1', '1', '1', '1',
        #         '1', '1', '0', '0', '0', '0', '1', '0', '0', '1', '0', '0', '0', '0', '0', '1', '1', '1', '0', '1', '1',
        #         '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1', '0', '1', '0', '0', '1', '1', '0',
        #         '0', '0', '0', '1', '1', '1', '0', '0', '0', '1', '1', '1', '0', '0', '1', '1', '0', '1', '1', '0', '1',
        #         '1', '0', '0', '1', '0', '1', '1', '1', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '0',
        #         '1', '1', '0', '0', '0', '1', '0', '0', '1', '1', '1', '1', '1', '1', '0', '0', '1', '1', '0', '0', '0',
        #         '1', '0', '1', '0', '0', '1', '0', '0', '0', '1', '1', '0', '1', '0', '0', '0', '1', '0', '0', '0', '0',
        #         '0', '0', '1', '0', '1', '1', '1', '0', '0', '0', '1', '1', '0', '1', '0', '0', '0', '0', '0', '1', '1',
        #         '1', '0', '0', '1', '0', '1', '0', '1', '1', '0', '0', '0', '1', '0', '1', '1', '0', '1', '1', '1', '1',
        #         '0']
        bits = change(bits)
        file.close()
        #print(bits)
        success, p, plist = func(bits)
        gotresult = True
        if success:
            print("PASS")
        else:
            print("FAIL")

        if p:
            print("P=" + str(p))

        if plist:
            for pval in plist:
                print("P=" + str(pval))
    else:
        print("Test name (%s) not known" % args.testname)
        exit()

else:
    results = list()
    for testname in testlist:
        print("TEST: %s" % testname)
        m = __import__(testname)
        func = getattr(m, testname)
        bits = ['1', '0', '0', '0', '0', '0', '0', '1', '0', '1', '0', '0', '0', '1', '1', '1', '0', '1', '1', '1', '1',
                '1', '0', '1', '0', '1', '1', '1', '0', '1', '1', '1', '1', '0', '0', '1', '1', '0', '1', '0', '1', '0',
                '1', '1', '1', '1', '0', '1', '0', '1', '0', '1', '0', '0', '1', '1', '1', '0', '0', '0', '1', '1', '0',
                '1', '1', '0', '0', '0', '0', '1', '1', '1', '1', '0', '0', '0', '0', '0', '0', '1', '1', '1', '1', '1',
                '1', '1', '0', '0', '0', '0', '1', '0', '0', '1', '0', '0', '0', '0', '0', '1', '1', '1', '0', '1', '1',
                '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1', '0', '1', '0', '0', '1', '1', '0',
                '0', '0', '0', '1', '1', '1', '0', '0', '0', '1', '1', '1', '0', '0', '1', '1', '0', '1', '1', '0', '1',
                '1', '0', '0', '1', '0', '1', '1', '1', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '0',
                '1', '1', '0', '0', '0', '1', '0', '0', '1', '1', '1', '1', '1', '1', '0', '0', '1', '1', '0', '0', '0',
                '1', '0', '1', '0', '0', '1', '0', '0', '0', '1', '1', '0', '1', '0', '0', '0', '1', '0', '0', '0', '0',
                '0', '0', '1', '0', '1', '1', '1', '0', '0', '0', '1', '1', '0', '1', '0', '0', '0', '0', '0', '1', '1',
                '1', '0', '0', '1', '0', '1', '0', '1', '1', '0', '0', '0', '1', '0', '1', '1', '0', '1', '1', '1', '1',
                '0']

        #bits = change(bits)

        (success, p, plist) = func(bits)

        summary_name = testname
        if success:
            print("  PASS")
            summary_result = "PASS"
        else:
            print("  FAIL")
            summary_result = "FAIL"

        if p != None:
            print("  P=" + str(p))
            summary_p = str(p)

        if plist != None:
            for pval in plist:
                print("P=" + str(pval))
            summary_p = str(min(plist))

        results.append((summary_name, summary_p, summary_result))

    print()
    print("SUMMARY")
    print("-------")

    for result in results:
        (summary_name, summary_p, summary_result) = result
        print(summary_name.ljust(40), summary_p.ljust(18), summary_result)