# fmap
Lazy map for Iterable and Sequence


Install
-------

    pip install git+https://github.com/betafcc/fmap.git

What?
-----

##### In Python 2
Only eager evaluation:
```py
> range(1, 11)
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # bad

> range(1, 11)[5:6]
[6]  # bad

> def fib(x):
.     if x in [0, 1]: return x
.     return fib(x - 1) + fib(x - 2)
> map(fib, range(1, 101))[30]
...  # End of the universe, really bad
```

##### In Python 3
Lazy evaluation, but losing the interface:
```py
> range(1, 11)
range(1, 11)  # good

> range(1, 11)[5:6]
range(6, 7)  # really good

> map(fib, range(1, 101))
<map at 0x7f12881fe0>  # meh

> map(fib, range(1, 101))[30]
TypeError: 'map' object is not subscriptable  # bad
```

##### With fmap
Lazy evaluation, preserving the interface:
```py
> from fmap import fmap
> fmap(fib, range(1, 101))
fmap(fib, range(1, 101))  # good

> fmap(fib, range(1, 101))[20:80]
fmap(fib, range(21, 81))  # really good

> fmap(fib, range(1, 101))[30]
1346269  # awesome
```

##### Also
Convenience for composition, fusing the functions:
```py
> def sq(x): return x*x
> fmap(sq, fmap(fib, range(1, 101)))
fmap(sq . fib, range(1, 101))

> fmap(fib, range(1, 101)) | sq
fmap(sq . fib, range(1, 101))
```
