import os, time, MySQLdb

conn = MySQLdb.connect(
    host='47.113.200.109',
    # mysql所在主机的ip
    port=33063,  # mysql的端口号
    user="aiit",  # mysql 用户名
    password="aiit9876",  # mysql 的密码
    db="hx_sales",  # 要使用的库名
    charset="utf8"  # 连接中使用的字符集
)
p_crate_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
cursor = conn.cursor()
sql = 'select *from goods limit 10;'
cursor.execute(sql)
data = cursor.fetchone()
print(data)
