# import pytest

lwb = 1
upb = 5
start = lwb
stop = upb + 1
type(range(start, stop))
r = range(start, stop)

for seq in r:
    print(seq)

assert(sum(r)) == 15
# assert(sum(r)) == 16  # returns AssertionError
 




