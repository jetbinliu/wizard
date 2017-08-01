# -*-coding: UTF-8-*-

import pymysql


def mdb(sql, host, port, user, passwd, db='', dictType = False, ex = False):
    '''
    封装mysql连接和获取结果集方法
    '''
    conn = None
    rows = None
    results = None
    # Connect to the cluster database
    try:
        conn = pymysql.connect(host=host,
                               port=port,
                               user=user,
                               passwd=passwd,
                               db=db,
                               charset='utf8mb4')
    except pymysql.Error as e:
        print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
    if dictType:
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                rows = cursor.execute(sql)
                results = cursor.fetchall()
                if ex:
                    conn.commit()
        except pymysql.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
        finally:
            conn.close()
    else:
        try:
            with conn.cursor() as cursor:
                rows = cursor.execute(sql)
                _results = cursor.fetchall()
                results = list(map(list, _results))
                if ex:
                    conn.commit()
        except pymysql.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
        finally:
            conn.close()
    return results

def mdb_query(sql, host, port, user, passwd, db='', dictType = False):
    '''
    封装mysql连接和获取结果集方法
    '''
    conn = None
    rows = None
    results = None
    field_names = None
    # Connect to the cluster database
    try:
        conn = pymysql.connect(host=host,
                               port=port,
                               user=user,
                               passwd=passwd,
                               db=db,
                               charset='utf8mb4')
    except pymysql.Error as e:
        print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
    if dictType:
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                rows = cursor.execute(sql)
                field_names = [i[0] for i in cursor.description]
                results = cursor.fetchall()
        except pymysql.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
        finally:
            conn.close()
    else:
        try:
            with conn.cursor() as cursor:
                rows = cursor.execute(sql)
                field_names = [i[0] for i in cursor.description]
                _results = cursor.fetchall()
                results = list(map(list, _results))
        except pymysql.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
        finally:
            conn.close()
    return field_names, results