from multiprocessing import Pool
from multiprocessing import current_process
from tqdm import tqdm
from functools import wraps
import ctypes
import types

CNX_INDI = '_cnx_'

def _exe_function(entry):
    adress, data = entry 
    func = ctypes.cast(adress, ctypes.py_object).value
    if isinstance(data, tuple) and data[0] == CNX_INDI and isinstance(data[1], tuple):
        adress, data = data[1]
        cnx = ctypes.cast(adress, ctypes.py_object).value
        return func(cnx, data)
    return func(data)

def _pack(address):
    """
    Adds the memory address to the data entry
    """
    def _pack_entry(entry):
        return address, entry
    return _pack_entry

def parallel(nproz=4, tag=None):
    """
    Function wrapper to run the function code on each 
    element of the input list in parallel.
    """
    def run_parallel(func):
        @wraps(func)
        def run(*data, length=None):
            if len(data) == 1:
                data = data[0]
            elif len(data) == 2 and func.__name__ != func.__qualname__:
                # requires context
                address = id(data[0])
                # set length since we want to use generator
                length = len(data[1]) if length is None else length
                data = map(_pack(address), data[1])
                # add context indicator
                data = map(_pack(CNX_INDI), data)
            else:
                raise ValueError('Invalid function specification or arguments')
            address = id(func)
            iterator = map(_pack(address), data)
            with Pool(nproz) as pool:
                res = list(tqdm(
                    pool.imap(_exe_function, iterator),
                    total=len(data) if length is None else length,
                    desc=tag
                ))
            return res
        return run
    return run_parallel
