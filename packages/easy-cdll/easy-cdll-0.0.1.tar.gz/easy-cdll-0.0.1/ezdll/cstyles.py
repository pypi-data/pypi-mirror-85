import os
import sys
import numpy
import ctypes
import numpy as np


class Cdll:

    '''
    >>> import ezdll
    >>> a = ezdll.Cdll('./libtest.so')
    >>> raw_data = {'a': [1,], 'b': [2, 3], 'c': [[4, 5], [6, 7]]}
    >>> results = a.call_function('api', raw_data)

    >>> print(results.contents.objective)

    >>>
    a
    1
    b
    2 3
    c
    4 5
    6 7
    1.23456789
    '''

    def __init__(self, library_path):
        '''
        check the current platform: linux should use .so, mac should use .dylib
        windows family platforms are not implemented yet
        '''
        self.numpy_data_type = ['int64', 'float64']
        self.default_output_structure = type('OutputStruct', (ctypes.Structure,), {'_fields_': [
            ('objective', ctypes.c_double),
            ('sol', ctypes.c_double * 1024 * 1024),
            ('others', ctypes.c_double * 1024),
        ]})
        if sys.platform == 'linux':
            if 'lib' not in library_path or '.so' not in library_path:
                raise NameError
            self.lib = ctypes.cdll.LoadLibrary(library_path)
        elif sys.platform == 'darwin':
            if 'lib' not in library_path or '.dylib' not in library_path:
                raise NameError
            self.lib = ctypes.cdll.LoadLibrary(library_path)
        else:
            raise NotImplementedError

    def _n_dim_dynamic_assign(self, iters, values):

        assert isinstance(iters, ctypes.Array), 'iters must be ctypes array'

        np.warnings.filterwarnings('error', category=np.VisibleDeprecationWarning)
        try:
            values = np.array(values)
        except:
            print('values cannot be converted to numpy array (ragged or not numeric)')
            raise TypeError
        assert values.dtype in self.numpy_data_type, 'currently support only signed intergers and floating points'

        if values.shape == tuple():
            iters[0] = values
            return

        for idx, (iter_, value) in enumerate(zip(iters, values)):
            if value.shape == tuple():
                iters[idx] = value
            else:
                self._n_dim_dynamic_assign(iter_, value)

    def call_function(self, function_name, input_raw_data, output_data_structure=None):

        fields = []
        shapes = []

        for key in input_raw_data:

            raw_data = np.array(input_raw_data[key])

            if raw_data.dtype == 'int64':
                type_ = ctypes.c_long
            elif raw_data.dtype == 'float64':
                type_ = ctypes.c_double
            else:
                print('values cannot be converted to numpy array (ragged or not numeric)')
                raise TypeError

            for s in raw_data.shape:
                shapes.append(s)
            shapes.append(0)

            if raw_data.shape == tuple():
                type_ = type_ * 1
            else:
                for s in raw_data.shape[::-1]: type_ = type_ * s

            fields.append((key, type_))
        shapes.append(-1)

        Parameters = type('Parameters', (ctypes.Structure,), {'_fields_': fields})
        params = Parameters()

        for key in input_raw_data:
            a = []
            exec('a.append(params.%s)' % (key))
            a = a[0]
            self._n_dim_dynamic_assign(a, input_raw_data[key])

        cdll_func = getattr(self.lib, function_name)
        cdll_func.argtypes = [ctypes.c_void_p, ctypes.POINTER(Parameters)]
        cdll_func.restype = ctypes.POINTER(self.default_output_structure if output_data_structure == None else output_data_structure)

        res = cdll_func(ctypes.c_void_p(np.array(shapes).ctypes.data), ctypes.byref(params))
        return res
