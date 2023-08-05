import base64
import numpy as np

array = np.full(fill_value=5, shape=(75, 75), dtype="int64")

print(array)
s = base64.b64encode(array)
print(s)
r = base64.b64decode(s)
array = np.frombuffer(r, dtype="int64")
print(array)