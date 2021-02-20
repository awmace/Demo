import os
output = os.popen('ping www.baidu.com')
print(output.read())
print('111')
