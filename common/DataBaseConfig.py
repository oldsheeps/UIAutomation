import pymysql

from common.CfgFileConfig import *


class DataBase(object):
    """数据库连接工具类封装"""

    def __init__(self, path, section):
        self.config = Config(path)
        self.config = self.config.__get__()
        self.host = self.config[section]['host']
        self.user = self.config[section]['user']
        self.port = self.config[section]['port']
        self.password = self.config[section]['password']
        self.database = self.config[section]['database']
        self.connection_info = {
            'host': self.host,
            'user': self.user,
            'port': int(self.port),
            'password': self.password,
            'database': self.database
        }
        self.conn = self.connect_database()
        self.cursor = self.connect_cursor()

    def connect_database(self):
        """
        1.建立数据库连接
        2.返回连接对象
        3.收集异常并返回False
        """
        try:
            self.conn = pymysql.connect(**self.connection_info)
            return self.conn
        except Exception as e:
            log.info(f'DataBases:数据库连接失败，传递数据不正确，请检查连接信息[{self.connection_info}]!')
            log.error(traceback.format_exc())
            return False

    def connect_cursor(self):
        """
        1.建立数据游标
        2.返回游标对象
        3.收集异常并返回False
        """
        try:
            self.cursor = self.conn.cursor()
            return self.cursor
        except Exception as e:
            log.info(f'DataBases:创建数据游标时发生异常，请检查数据库连接!')
            log.error(traceback.format_exc())
            return False

    def close_connect(self):
        """
        1.关闭数据游标、数据库连接
        2.关闭成功返回True
        3.收集异常并返回False
        """
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
            return True
        except Exception as e:
            log.info(f'DataBases:关闭资源连接失败，错误信息[{e}]!')
            log.error(traceback.format_exc())
            return False

    def execute_sql(self, sql, params=None, exe_many=False):
        """
        使用数据库连接对象执行SQL语句
        :param sql:     SQL执行语句
        :param params:  单条SQL语句参数：(1,2,3...)，多条SQL语句参数：[[1,2,3...],[2,3,4...]]
        :param exe_many:批量执行开关，True多条SQL语句，False单条SQL语句
        :return:结果总行数
        """
        if not self.conn:
            return False
        try:
            if self.conn and self.cursor:
                print('SQL语句：', sql)
                print('SQL参数：', params)
                if exe_many:
                    result_row = self.cursor.executemany(sql, params)
                else:
                    result_row = self.cursor.execute(sql, params)
                self.conn.commit()
        except:
            return False
        finally:
            self.close_connect()
        return result_row

    def query_count_data(self, **kwargs):
        """
        查询结果行数
        table：必填项，查询表名，字符串类型，如：table="test_table"
        where：非必填，查询条件，如果是字典类型表示等于，如：where={"a列": 111, "b列": 2222}；
                              如果是字符串类型表示非等于判断，如：where="c列>=333"
        """
        # 将查询表名以table作为键值设为必填参数
        table = kwargs["table"]
        # 基础SQL语句
        sql = f"select count(1) as count from {table} where 1=1 "
        # 使用params列表记录where携带的条件参数
        params = []
        # 将查询条件设置为非必填项，如果传递了where关键字，则根据传入的数据类型处理
        if 'where' in kwargs.keys():
            where = kwargs["where"]
            # 如果where参数是以字典形式携带，则表示K值=V值
            if isinstance(where, dict):
                for k, v in where.items():
                    sql += " and {} in (%s)".format(k)
                    params.append(str(v))
            # 如果where参数是以字符串形式携带，则直接将字符串and到SQL语句上
            elif isinstance(where, str):
                sql += " and %s;" % where
            # 如果是字典则会产生对应字典的数据，如果是字符串则没有
        params = tuple(params)
        try:
            self.execute_sql(sql, params)
            data = self.cursor.fetchone()
            return data
        except:
            self.conn.rollback()

    def query_first_data(self, **kwargs):
        """
        根据条件筛选数据后返回第一行数据
        table：必填项，查询表名，字符串类型，如：table="test_table"
        where：非必填，查询条件，如果是字典类型表示等于，如：where={"a列": 111, "b列": 2222}；如果是字符串类型表示非等于判断，如：where="c列>=333"
        field：非必填，查询列名，字符串类型，如：field="aaa, bbb"，不填默认*
        order：非必填，排序字段，字符串类型，如：order="a列"
        sort： 非必填，排序方式，字符串类型，如：sort="asc" 或者 "desc"，不填默认asc
        """
        # 将查询表名以table作为键值设为必填参数
        table = kwargs['table']
        # 判断是否携带查询列值，如果携带则查询传递字段，否则查询所有字段
        field = "field" in kwargs and kwargs["field"] or "*"
        # 将查询条件以where作为键值设为必填参数
        where = kwargs["where"]
        # 判断是否传递order关键字参数，如果没有传递则不拼接，否则拼接order by字段
        order = "order" in kwargs and "order by " + kwargs["order"] or ""
        # 将排序方式以sort作为键值设为必填参数，默认asc
        sort = kwargs.get("sort", "asc")
        # 如果order为空则sort也设置为空
        if order == "":
            sort = ""
        # 基础SQL语句
        sql = f"select {field} from {table} where 1=1"
        # where条件携带参数
        params = []
        # 如果where参数是以字典形式携带，则表示K值=V值
        if isinstance(where, dict):
            for k, v in where.items():
                sql += " and {} in (%s)".format(k)
                params.append(str(v))
        # 如果where参数是以字符串形式携带，则直接将字符串and到SQL语句上
        elif isinstance(where, str):
            sql += f" and {where}"
        # 排序处理后筛选第1条数据
        sql += f" {order} {sort} limit 1;"
        # 如果是字典则会产生对应字典的数据，如果是字符串则没有
        params = tuple(params)
        try:
            self.execute_sql(sql, params)
            first_data = self.cursor.fetchone()
            return first_data
        except:
            self.conn.rollback()

    def query_every_data(self, **kwargs):
        """
        查批量数据
        table： 必填项，查询表名，字符串类型，如：table="test_table"
        where： 非必填，查询条件，分两种类型，如：1.字典类型用于=，如：where={"aaa": 333, "bbb": 2}；2.字符串类型用于非等于判断，如：where="aaa>=333"
        field： 非必填，查询列名，字符串类型，如：field="aaa, bbb"，不填默认*
        order： 非必填，排序字段，字符串类型，如：order="a列"
        sort：  非必填，排序方式，字符串类型，如：sort="asc" 或者 "desc"，不填默认asc
        offset：非必填，偏移数量，如翻页，不填默认0
        limit： 非必填，查询条数，不填默认100
        """
        # 将查询表名以table作为键值设为必填参数
        table = kwargs["table"]
        # 判断是否携带查询列值，如果携带则查询传递字段，否则查询所有字段
        field = "field" in kwargs and kwargs["field"] or "*"
        # 判断是否传递order关键字参数，如果没有传递则不拼接，否则拼接order by字段
        order = "order" in kwargs and "order by " + kwargs["order"] or ""
        # 将排序方式以sort作为键值设为必填参数，默认asc
        sort = kwargs.get("sort", "asc")
        # 如果order为空则sort也设置为空
        if order == "":
            sort = ""
        # 将偏移数量以offset作为键值设为必填参数，默认0，如果查询需要分页则以offset和limit来计算
        offset = kwargs.get("offset", 0)
        # 将查询条数以limit作为键值设为必填参数，默认100
        limit = kwargs.get("limit", 100)
        # 基础SQL语句
        sql = "select %s from %s where 1=1 " % (field, table)
        # where条件携带参数
        params = []
        # 将查询条件设置为非必填项，如果使用该方法时，传递了where关键字，则根据传入的数据类型进行SQL语句处理
        if 'where' in kwargs.keys():
            where = kwargs["where"]
            # 如果where参数是以字典形式携带，则表示K值=V值
            if isinstance(where, dict):
                for k, v in where.items():
                    sql += " and {} in (%s)".format(k)
                    params.append(str(v))
            # 如果where参数是以字符串形式携带，则直接将字符串and到SQL语句上
            elif isinstance(where, str):
                sql += " and %s" % where
        # 如果是字典则会产生对应字典的数据，如果是字符串则没有
        params = tuple(params)
        # 处理SQL语句，拼接排序字段和方式以及或分页计算
        sql += " %s %s limit %s, %s;" % (order, sort, offset, limit)
        try:
            self.execute_sql(sql, params)
            data = self.cursor.fetchall()
            return data
        except:
            self.conn.rollback()

    def delete_data(self, **kwargs):
        """
        删除并返回影响行数
        table： 必填项，查询表名，字符串类型，如：table="test_table"
        where： 非必填，查询条件，分两种类型，如：1.字典类型用于=，如：where={"aaa": 333, "bbb": 2}；2.字符串类型用于非等于判断，如：where="aaa>=333"
        """
        # 将查询表名以table作为键值设为必填参数
        table = kwargs["table"]
        # 将查询条件以where作为键值设为必填参数
        where = kwargs["where"]
        # 基础SQL语句
        sql = "delete from %s where 1=1" % (table)
        # where条件携带参数
        params = []
        # 如果where参数是以字典形式携带，则表示K值=V值
        if isinstance(where, dict):
            for k, v in where.items():
                sql += " and {} in (%s)".format(k)
                params.append(str(v))
        # 如果where参数是以字符串形式携带，则直接将字符串and到SQL语句上
        elif isinstance(where, str):
            sql += " and %s" % where
        sql += ";"
        # 如果是字典则会产生对应字典的数据，如果是字符串则没有
        params = tuple(params)
        try:
            self.execute_sql(sql, params)
            rowcount = self.cursor.rowcount
            return rowcount
        except:
            self.conn.rollback()

    def update_data(self, **kwargs):
        """
        修改数据并返回影响的行数
        table：必填项，查询表名，字符串类型，如：table="test_table"
        data ：必填项，更新数据，字典类型，如：data={"aaa": "6666", "bbb": "888"}
        where：非必填，查询条件，分两种类型，如：1.字典类型用于=，如：where={"aaa": 333, "bbb": 2}；2.字符串类型用于非等于判断，如：where="aaa>=333"
        """
        # 将查询表名以table作为键值设为必填参数
        table = kwargs["table"]
        # 将更新数据以data作为键值设为必填参数
        data = kwargs["data"]
        # 将查询条件以where作为键值设为必填参数
        where = kwargs["where"]
        # 基础SQL语句
        sql = "update %s set " % table
        # where条件携带参数
        params = []
        for k, v in data.items():
            sql += "{}=%s,".format(k)
            params.append(str(v))
        sql = sql.rstrip(",")
        sql += " where 1=1 "
        # 如果where参数是以字典形式携带，则表示K值=V值
        if isinstance(where, dict):
            for k, v in where.items():
                sql += " and {} in (%s)".format(k)
                params.append(str(v))
        # 如果where参数是以字符串形式携带，则直接将字符串and到SQL语句上
        elif isinstance(where, str):
            sql += " and %s" % where
        sql += ";"
        # 如果是字典则会产生对应字典的数据，如果是字符串则没有
        params = tuple(params)
        try:
            self.execute_sql(sql, params)
            rowcount = self.cursor.rowcount
            return rowcount
        except:
            self.conn.rollback()

    # 新增并返回新增ID
    def insert_data(self, **kwargs):
        """
        table：必填，插入表名，字符类型
        data ：必填，更新数据，字典类型
        """
        # 将插入表名以table作为键值设为必填参数
        table = kwargs["table"]
        # 将更新数据以data作为键值设为必填参数
        data = kwargs["data"]
        # 设置基础SQL语句
        sql = "insert into %s (" % table
        # 记录表字段
        fields = ""
        flag = ""
        # 记录插入的数据
        params = []
        for k, v in data.items():
            fields += "%s," % k
            params.append(str(v))
            flag += "%s,"
        fields = fields.rstrip(",")
        # 如果是字典则会产生对应字典的数据，如果是字符串则没有
        params = tuple(params)
        flag = flag.rstrip(",")
        sql += fields + ") values (" + flag + ");"
        try:
            num = self.execute_sql(sql, params)
            # 获取自增id
            # res = self.cursor.lastrowid
            return num
        except:
            self.conn.rollback()


if __name__ == '__main__':
    path = '../config/database.cfg'
    db = DataBase(path, 'bosc')
    print("是否连接成功：", db.conn.open)

    print("查看当前游标中的数据行：",db.cursor.rowcount)

    # print("关闭资源连接：", db.close_connect())

    # sql = 'select * from testcase;'
    # datas = db.execute_sql(sql)
    # print('sql结果行数：',datas)

    # sql = "insert into testcase(step_no, step_action, locator_name, locator_path, step_text, step_desc, step_expect, step_result) values(%s,%s,%s,%s,%s,%s,%s,%s);"
    # sql = "insert into testcase values(%s,%s,%s,%s,%s,%s,%s,%s);"
    # params = ('6', '等待', None, None, '2', '强制等待2秒', None, None)
    # datas = db.execute_sql(sql,params)
    # print('单条SQL语句执行结果行数：',datas)

    # sql = "insert into testcase(step_no, step_action, locator_name, locator_path, step_text, step_desc, step_expect, step_result) values(%s,%s,%s,%s,%s,%s,%s,%s);"
    # params = [['6', '等待', None, None, '6', '强制等待6秒', None, None],['7', '等待', None, None, '7', '强制等待7秒', None, None]]
    # datas = db.execute_sql(sql,params,exe_many=True)
    # print('多条SQL语句执行结果行数：',datas)

    # result = db.query_count_data(table='testcase',field='*')
    # print("查询表的总行数：", result)
    # result = db.query_count_data(table='testcase',field='*', where='step_no>3')
    # print("查询表的step_no大于3的总行数：", result)
    # result = db.query_count_data(table='testcase',field='*',where={'step_no':3,'step_action':'输入'})
    # print("查询表的step_no等于3且step_action等于输入的总行数：", result)

    # result = db.query_one_data(table='testcase',field='*',where="1=1",order='step_no',sort='asc')
    # print("查询一行：",result)

    # result = db.query_more_data(table='testcase',field='*')
    # print("查询多行：",result)

    # result = db.query_count_data(table='testcase', field='*', where="1=1")
    # print("查询行数：", result)

    # insertValue = {'step_no':6, 'step_action':'等待', 'locator_name':'', 'locator_path':'', 'step_text':2, 'step_desc':"强制等待2秒", 'step_expect':'', 'step_result':''}
    # result = db.insert_data(table='testcase', data=insertValue)
    # print("插入数据：", result)

    # result = db.update_data(table='testcase', where='step_no="6"',data={"step_text":66,'step_desc':"强制等待66秒"})
    # print("修改数据：", result)

    # result = db.delete_data(table='testcase', where='step_no=6')
    # print("删除数据：", result)
