这是做什么的？
=======================
这是一个任意文件查找器，支持文件夹，文件名以及文件内容的关键字查找，支持正则模式，并且用突出颜色显示

怎么安装？
=========
pip install findkw

怎么使用
=========

### 1. 在终端直接使用：

```
$ findkw -k "要查找关键字" [-f --folder] [-o --filename_only] [-r --re_mode]
```

#### 参数解释：

##### -h, --help          ---> 显示帮助

##### -k, --keyword       ---> 要查找的关键字，必须值

##### -f, --folder        ---> 需要查找的文件夹，默认在运行目录下

##### -r, --re_mode       ---> y/n 是否以正则方式查找，默认n，可不指定参数值

##### -o, --filename_only ---> y/n 是否只查找文件夹名和文件名，默认n，可不指定参数值  

##### -rmf, --remove_file ---> y/n 是否删除找到的文件，默认n，可不指定参数值  

##### -rml, --remove_line ---> y/n 是否删除找到的行，默认n，可不指定参数值  

##### -qr, --quietly_remove ---> y/n 是否不经确认直接删除，默认n，可不指定参数值  

##### -rt, --replace_to ---> 替换为，支持 python re.sub 的操作  


#### 示例：

```shell script

# 当前文件夹下查找所有符合关键字的文件内容
$ findkw -k "good job"
# in file [ /root/Findkw/README.md ]: 
# >>> [ 36 ] [ $ findkw -k "good job" ]

# 上面输出的是当前 README 文件的第36行，找到了需要的关键字

# 在指定文件夹下查找关键字：
$ findkw -k "nice job" -f "/root/search_folder"

# 在当前文件夹下查找带有关键字的文件夹名或者文件名：
$ findkw -k "findkw" -o
# >>> [ folder ] [ /root/Findkw/findkw.egg-info ]
# >>> [ folder ] [ /root/Findkw/build/lib/findkw ]
# >>> [ file name ] [ /root/Findkw/findkw/findkw.py ]
# >>> [ folder ] [ /root/Findkw/findkw ]
# ...

# 正则模式查找所有以 .py 结尾的行：
$ findkw -k ".*?\.py$" -r
# in file [ /root/Findkw/findkw.egg-info/SOURCES.txt ]: 
# >>> [ 2 ] [ setup.py ]
# >>> [ 3 ] [ findkw/__init__.py ]
# >>> [ 4 ] [ findkw/findkw.py ]

# 正则模式查找所有以 .py 结尾的文件夹和文件名：
$ findkw -k ".*?\.py$" -r -o
# >>> [ file name ] [ /root/Findkw/setup.py ]
# >>> [ file name ] [ /root/Findkw/build/lib/findkw/findkw.py ]
# >>> [ file name ] [ /root/Findkw/build/lib/findkw/__init__.py ]
# >>> [ file name ] [ /root/Findkw/findkw/findkw.py ]
# >>> [ file name ] [ /root/Findkw/findkw/__init__.py ]

# 正则模式查找所有带有 0.1 版本字样的行：
$ findkw -k "[Vv]ersion[\': ]+0\.1\.\d" -r
# in file [ /root/Findkw/setup.py ]: 
# >>> [ 8 ] [ 'version': '0.1.0', ]

# in file [ /root/Findkw/findkw.egg-info/PKG-INFO ]: 
# >>> [ 3 ] [ Version: 0.1.0 ]

# 正则替换行，只保留匹配到的数字，加参数 -qr 是静默更改模式，不会出现提示：
$ findkw -k "VERSION\.(\d+)" -rt "\1" -r -qr
# line [ 19 ]: "VERSION.123" ✘
# replace to
# line [ 19 ]: "123" ✔


```


### 2. 在代码中调用：

#### 下载 Finder/findkw/findkw.py 文件到你的代码目录中

```
from findkw.findkw import Finder

folder = "/root/search_folder"
kw = "正则表达式或者关键字"
fn_only = False     # 如果只返回文件夹或文件夹名则 True
re_mode = False     # 如果kw是正则表达式则 True

fd = Finder(folder, kw, fn_only, re_mode, True)
res = fd.start()

print(res)
```