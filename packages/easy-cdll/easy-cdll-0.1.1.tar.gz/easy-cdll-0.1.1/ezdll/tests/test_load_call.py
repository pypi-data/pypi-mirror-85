import os
import sys
import glob
import numpy as np
from ezdll.cstyles import cstyles


def test_platform():
    assert sys.platform == 'linux' or sys.platform == 'darwin'

def test_compile():
    dll_path = glob.glob('./**/libtest.so', recursive = True)
    if not len(dll_path):
        tests_path = glob.glob('./**/tests/', recursive = True)[0]
        os.system('g++ -std=c++17 -shared -fPIC -o {} {}'.format(os.path.join(tests_path, 'libtest.so'), os.path.join(tests_path, 'test.cpp')))
    dll_path = glob.glob('./**/libtest.so', recursive = True)
    a = cstyles.Cdll(dll_path[0])
    raw_data = {'a': [1,], 'b': [2, 3], 'c': [[4, 5], [6, 7]]}
    results = a.call_function('api', raw_data)
    os.remove(dll_path[0])
    with open('test_output.txt', 'r') as f:
        buf = f.read()
    os.remove('test_output.txt')
    assert buf.strip().split('\n')[:7] == ['a', '1', 'b', '2 3', 'c', '4 5', '6 7']
    assert str(results.contents.objective) == '1.23456789'
