# example of building binary python package

## Package directory structure

directory struct of the example

```powershell
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

2. Create some python files (`main1.py, main2.py`) to run your codes. These files are execuators of your codes and can be read by others.

3. Create the `setup.py` file and run `python setup.py bdist_wheel --exclude-source-files`. It will create the binary package (`pyd`) and exclude the source files. The `pyd` files are [hard to reverse engineer](https://stackoverflow.com/questions/12075042/how-hard-to-reverse-engineer-pyd-files), so it can protect your source code.

```powershell
dist
|
│  pkga-0.0.1-cp310-cp310-win_amd64.whl
│
└─pkga-0.0.1-cp310-cp310-win_amd64
    ├─pkga
    │  │  A.cp310-win_amd64.pyd
    │  │  B.cp310-win_amd64.pyd
    │  │
    │  └─pkgb
    │          A.cp310-win_amd64.pyd
    │
    └─pkga-0.0.1.dist-info
            METADATA
            RECORD
            top_level.txt
            WHEEL
```

These package can be deployed to other machine or upload to our ElephasPyPi.

## Our wheel package tool : elephas_wheel
The official wheel tool can't exclude source files, so we create our own wheel tool [elephas_wheel](https://github.com/elephasquant/elephas_wheel). 
```powershell
python -m pip install elephas-wheel
```


## ElephasPyPi

### Install package from ElephasPyPi

```powershell
python.exe -m pip install --index-url http://192.168.0.157:8081/simple/ ElephasReader -U --trusted-host 192.168.0.157
```

### Upload your package

1. Create file `~/.pypirc`

```ini
[distutils]
index-servers =
        elephaspypi 
[elephaspypi]
repository: http://192.168.0.157:8081
username:
password:
```

2. Upload package

```powershell
# upload source distribution
python.exe .\setup.py sdist upload -r elephaspypi

# upload binary distribution
python setup.py bdist_wheel --exclude-source-files upload -r elephaspypi
```