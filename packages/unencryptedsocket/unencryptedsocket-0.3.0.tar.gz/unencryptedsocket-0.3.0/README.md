# Unencrypted Socket

<badges>[![version](https://img.shields.io/pypi/v/unencryptedsocket.svg)](https://pypi.org/project/unencryptedsocket/)
[![license](https://img.shields.io/pypi/l/unencryptedsocket.svg)](https://pypi.org/project/unencryptedsocket/)
[![pyversions](https://img.shields.io/pypi/pyversions/unencryptedsocket.svg)](https://pypi.org/project/unencryptedsocket/)  
[![donate](https://img.shields.io/badge/Donate-Paypal-0070ba.svg)](https://paypal.me/foxe6)
[![powered](https://img.shields.io/badge/Powered%20by-UTF8-red.svg)](https://paypal.me/foxe6)
[![made](https://img.shields.io/badge/Made%20with-PyCharm-red.svg)](https://paypal.me/foxe6)
</badges>

<i>Simple socket server-client for interprocess communications without security</i>

# Hierarchy

```
unencryptedsocket
|---- SS
'---- SC
```

# Example

## python
```python
# You can transmit objects as long as
# both sides have access to their classes

from unencryptedsocket import *


# server
def test(data):
    return f"Data:\t{data}"
functions = dict(test=test)
SS(functions=functions).start()
print("test socket server started.", flush=True)
# # Nothing is printed, you must start it from an other thread

# client
sc = SC()
for i in range(5):
    print(sc.request(command="test", data=args(f"Hello, {i}!")))
for i in range(5):
    print(SC().request(command="test", data=args(f"Hello, {i}!")))
print("test socket client started.", flush=True)
# # both for loops produce same result
# # while the later one uses a new key in each loop
# Data:   Hello, 0!
# Data:   Hello, 1!
# Data:   Hello, 2!
# Data:   Hello, 3!
# Data:   Hello, 4!
# test socket client started.
```
