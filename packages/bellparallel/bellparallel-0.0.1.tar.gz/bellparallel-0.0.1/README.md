# Bell Parallel
This is a collection of usefull tools for parallel data processing.

# Usage
```python
from bell_parallel import parallel

@parallel(tag='Increment', nproz=4)
def inc(entry):
    return entry + 1
    
data = range(10000)
out = inc(data)
```
