### wd

this is a demo

when i use pip install package
i can use cli to run the package

```buildoutcfg
pip install -i https://test.pypi.org/simple/ wd==0.8
$ wd -h
usage: wd [-h] [--pow POW] [--sqrt SQRT]

num calc

optional arguments:
  -h, --help   show this help message and exit
  --pow POW    calc the number pow
  --sqrt SQRT  calc the number sqrt

$ wd --pow=4 --sqrt=16
pow 16.0
sqrt 4.0
 
```