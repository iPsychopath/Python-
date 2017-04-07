#   导入MySQLdb模块
import MySQLdb

#   配置连接MySQL
config = {
          'host':'127.0.0.1',
          'port':3306,
          'user':'root',
          'password':'root',
          'db':'test',
          'charset':'utf8',
          }

#   链接数据库
conn = MySQLdb.connect(**config)

#   获取对象，并且设置返回的记录为字典(dict)
cursor = conn.cursor(MySQLdb.cursors.DictCursor)
#   获取对象，不设置返回的记录类型，默认为列表(list)
# cursor = conn.cursor()+

#   数据库语句   ##  select避免使用*号，消耗性能
sql="select `id`,`name` from test"
sql_insert='insert into `test`(`id`,`name`) VALUES(null,"admin2")'
try:
    #   执行插入SQL语句
    cursor.execute(sql_insert)
    #   输出影响行数
    print(cursor.rowcount)
    #   执行SQL查询语句
    cursor.execute(sql)
    #   输出查询总行数
    print(cursor.rowcount)
    #   获取全部记录赋值给rs
    rs=cursor.fetchall()
    #   输出全部记录
    print(rs)
    #   以上全部执行成功，执行事务更新数据库
    conn.commit()
except Exception as e:
    #   输出错误
    print(e)
    #   执行错误，执行回滚事务
    conn.rollback()
#   关闭
cursor.close()
conn.close()
