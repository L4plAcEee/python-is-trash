# pip install mysqlclient
import MySQLdb


# 连接数据库
def ConnectSql():
    # 数据库连接
    global global_con
    # 游标
    global global_cur
    global_con = MySQLdb.connect(host='localhost', user='root', password='123456', database='facepro', charset='utf8')
    global_cur = global_con.cursor()


# 查询数据库(返回所有数据)
def SearchAll(searchSql):
    global_cur.execute(searchSql)
    all = global_cur.fetchall()
    return all


# 查询数据库(返回单条数据)
def SearchSingle(searchSql):
    global_cur.execute(searchSql)
    single = global_cur.fetchone()
    return single


def SearchExist(searchSql):
    global_cur.execute(searchSql)
    single = global_cur.fetchone()
    return single is not None


# 修改和增加调用此方法
def ExecuteData(SqlStr):
    global_cur.execute(SqlStr)
    global_con.commit()


# 判断数据库是否存在数据
def HasData(searchSql):
    all = SearchAll(searchSql)
    if len(all) > 0:
        return True
    else:
        return False


# 关闭数据库连接（程序运行结束的时候，手动调用）
def CloseMySql():
    global_cur.close()
    global_con.close()

# def ConnectMySql():
#    # 连接数据库
#    con = MySQLdb.connect(host='localhost', user='root', password='123456', database='facepro', charset='utf8')
#    # 创建游标
#    cur = con.cursor()
#    datetime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#    print(datetime)
#    # 生成数据库
#    # sql = 'select * from signindata'
#    sqlInsert="insert into signindata(username,time,signaturepic,facepic) \
#                       values('%s','%s','%s','%s')" % \
#                        ('菲',datetime, '445454','666666')
#    #name="zhouzhou"
#    sqlInsert2 = "insert into signindata(username,time,signaturepic,facepic) values('www','2023-07-05 10:30:24','22','33')"
#
#    # 获取结果
#    #cur.execute(sqlInsert)
#    # 获取所有记录  fetchall--获取所有记录   fetchmany--获取多条记录，需传参  fetchone--获取一条记录
#    cur.execute(sqlInsert2)
#    #all = cur.fetchall()
#    # 输出查询结果
#    #print(len(all))
#    con.commit()
#    # 关闭游标
#    # ConnectMySql()
