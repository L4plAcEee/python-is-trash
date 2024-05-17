import time
import MySqlTool

MySqlTool.ConnectSql()
label = 1
name_list = {
    1: "小明"
}
currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
sqlStr4 = "select * from attendance where name= '%s' " % f"{name_list[label]}"
# print("当前时间为：" + currentTime)
# sqlStr1 = "insert into attendance(name,time)values('%s', '%s')" % ("小明", currentTime)
# MySqlTool.ExecuteData(sqlStr1)
# 甽除数据
# sqlStr2 = "delete from Attendance where name='小明'"
# MySqlTool.ExecuteData(sqlStr2)
# 修改数据
# sqlStr3 = "update Attendance set name='大红红' where id=6 "
# MySqlTool.ExecuteData(sqlStr3)
# 查询单条数据
# sqlStr4 = "select *from Attendance where name='小明'"
result4 = MySqlTool.SearchSingle(sqlStr4)
print(result4)
# 查询所有数据
# sqlStr5 = "select *from Attendance"
# result5 = MySqlTool.SearchAll(sqlStr5)
# print(result5)
# 关闭数据库
MySqlTool.CloseMySql()
