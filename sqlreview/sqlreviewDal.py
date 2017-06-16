# -*- coding: UTF-8 -*-

from django.db import connection

_CHART_DAYS = 90

def getWorkChartsByMonth(self):
    cursor = connection.cursor()
    sql = "select date_format(create_time, '%%m-%%d'),count(*) from sql_workflow where create_time>=date_add(now(),interval -%s day) group by date_format(create_time, '%%m-%%d') order by 1 asc;" % (Dao._CHART_DAYS)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

def getWorkChartsByPerson(self):
    cursor = connection.cursor()
    sql = "select engineer, count(*) as cnt from sql_workflow where create_time>=date_add(now(),interval -%s day) group by engineer order by cnt desc limit 50;" % (Dao._CHART_DAYS)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result