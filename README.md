# example of publish binary python package

## package directory structure

directory struct of the example01

```bash
example01
|
│  main1.py
|  main2.py
│  setup.py
│
└─pkga
    │  A.py
    │  B.py
    │
    └─pkgb
          A.py
```

1. Pack all your code in one directory (`pkga` in the example). Codes in these directories are compiled to binary which can't be read by human. 

2. In your package, don't use relative import (something like `from . import your_module`)

3. Create some python files (`main1.py, main2.py`) to run your codes. These files are execuators of your codes and can be read by every one.

4. 

## 