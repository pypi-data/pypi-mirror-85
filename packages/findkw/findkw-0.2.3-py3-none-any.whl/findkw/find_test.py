import os
import re

path = os.getcwd()
kw = "*.py"
cmd = f"find {path} -name '{kw}' "

# res = os.system(cmd)
res = os.popen(cmd).read()
# print(type(res), res)
res = res.split("\n")
print(res)
pt = re.compile(kw)
res = [x for x in res if x and re.findall(pt, x)]
print(res)
