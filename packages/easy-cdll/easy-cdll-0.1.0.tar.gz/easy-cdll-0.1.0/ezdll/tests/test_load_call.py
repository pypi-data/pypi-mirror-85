import os
import sys
import numpy as np
from ezdll.cstyles import cstyles


def test_platform():
    assert sys.platform == 'linux' or sys.platform == 'darwin'

def test_compile():
    os.system('g++ -std=c++17 -shared -fPIC -o libtest.so test.cpp')
    a = cstyles.Cdll('./libtest.so')
    raw_data = {'a': [1,], 'b': [2, 3], 'c': [[4, 5], [6, 7]]}
    results = a.call_function('api', raw_data)
    os.remove('libtest.so')
    with open('test_output.txt', 'r') as f:
        buf = f.read()
    os.remove('test_output.txt')
    assert buf.strip().split('\n')[:7] == ['a', '1', 'b', '2 3', 'c', '4 5', '6 7']
    assert str(results.contents.objective) == '1.23456789'
