from multiprocessing import Pool
from multiprocessing import current_process
from tqdm import tqdm
from functools import wraps
import ctypes

def _exe_function(entry):
    adress, data = entry
    func = ctypes.cast(adress, ctypes.py_object).value
    return func(data)

def parallel(nproz=4, tag=None):
    """
    Function wrapper to run the function code on each 
    element of the input list in parallel.
    """
    def run_parallel(func):
        @wraps(func)
        def run(data):
            address = id(func)
            def pack(entry):
                return address, entry
            iterator = map(pack, data)
            with Pool(nproz) as pool:
                res = list(tqdm(
                    pool.imap(_exe_function, iterator),
                    total=len(data),
                    desc=tag
                ))
            return res
        return run
    return run_parallel
