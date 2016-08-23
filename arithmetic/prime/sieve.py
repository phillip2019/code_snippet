#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    sxw 2016-08-23
    筛法求质数
"""
import sys


def sieve(n):
    """
    筛法求质数
    :param n:
    :return: list
    :ref: http://www.pythontab.com/html/2015/pythonhexinbiancheng_1218/997.html
    """
    # compute primes using sieve eratosthenes
    x_ = [1] * n
    x_[1] = 0
    for i in range(2, n / 2):
        j = 2 * i
        while j < n:
            x_[j] = 0
            j += i
    return x_


def prime(n, x):
    # Find nth prime
    i = 1
    j = 1
    while j <= n:
        if x[i] == 1:
            j += 1
        i += 1
    return i - 1


if __name__ == '__main__':
    x = sieve(10000)
    code = [1206, 301, 384, 5]
    key = [1, 1, 2, 2]
    sys.stdout.write("".join(chr(i) for i in [73, 83, 66, 78, 32, 61, 22]))
    for i in range(0, 4):
        sys.stdout.write(str(prime(code[i], x) - key[i]))