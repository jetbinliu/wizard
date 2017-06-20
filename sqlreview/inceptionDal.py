# -*-coding: utf-8-*-

import re
import json
import MySQLdb


from .models import workflow
from dbconfig.models import cluster_config
from common.aes_decryptor import Prpcrypt
from lib.configgetter import Configuration
from lib.mysqllib import mdb

conf = Configuration("conf/global.conf")



class InceptionDao(object):
    def __init__(self):
        try:
            self.inception_host = conf.get("INCEPTION", "INCEPTION_HOST")
            self.inception_port = int(conf.get("INCEPTION", 'INCEPTION_PORT'))

            self.inception_remote_backup_host = conf.get("INCEPTION", 'INCEPTION_REMOTE_BACKUP_HOST')
            self.inception_remote_backup_port = int(conf.get("INCEPTION", 'INCEPTION_REMOTE_BACKUP_PORT'))
            self.inception_remote_backup_user = conf.get("INCEPTION", 'INCEPTION_REMOTE_BACKUP_USER')
            self.inception_remote_backup_password = conf.get("INCEPTION", 'INCEPTION_REMOTE_BACKUP_PASSWORD')
            self.prpCryptor = Prpcrypt()
        except Exception as e:
            print("Error: %s" % e)

    def criticalDDL(self, sqlContent):
        '''
        识别DROP DATABASE, DROP TABLE, TRUNCATE PARTITION, TRUNCATE TABLE等高危DDL操作，因为对于这些操作，inception在备份时只能备份METADATA，而不会备份数据！
        如果识别到包含高危操作，则返回“审核不通过”
        '''
        if re.match(
                r"([\s\S]*)drop(\s+)database(\s+.*)|([\s\S]*)drop(\s+)table(\s+.*)|([\s\S]*)truncate(\s+)partition(\s+.*)|([\s\S]*)truncate(\s+)table(\s+.*)",
                sqlContent.lower()):
            return ((
                    '', '', 2, '', '不能包含【DROP DATABASE】|【DROP TABLE】|【TRUNCATE PARTITION】|【TRUNCATE TABLE】关键字！', '', '',
                    '', '', ''),)
        else:
            return None

    def sqlautoReview(self, sqlContent, clusterName, isBackup='否'):
        '''
        将sql交给inception进行自动审核，并返回审核结果。
        '''
        listMasters = cluster_config.objects.filter(cluster_name=clusterName)
        if len(listMasters) != 1:
            print("Error: 集群配置返回为0")
        masterHost = json.loads(listMasters[0].cluster_hosts)[0]
        masterPort = listMasters[0].cluster_port
        masterUser = listMasters[0].cluster_user
        masterPassword = self.prpCryptor.decrypt(listMasters[0].cluster_password)

        # 这里无需判断字符串是否以；结尾，直接抛给inception enable check即可。
        # if sqlContent[-1] != ";":
        # sqlContent = sqlContent + ";"

        if conf.has_option("INCEPTION", 'CRITICAL_DDL_ON_OFF'):
            if conf.get("INCEPTION", 'CRITICAL_DDL_ON_OFF').lower() == "on":
                criticalDDL_check = self.criticalDDL(sqlContent)
            else:
                criticalDDL_check = None

            if criticalDDL_check:
                result = criticalDDL_check
            else:
                sql = "/*--user=%s;--password=%s;--host=%s;--enable-check=1;--port=%s;*/\
                  inception_magic_start;\
                  %s\
                  inception_magic_commit;" % (masterUser, masterPassword, masterHost, str(masterPort), sqlContent)
                result = mdb(sql, self.inception_host, self.inception_port, '', '', '')
        print("sqlautoReview", result)
        return result

    def executeFinal(self, workflowDetail, dictConn):
        '''
        将sql交给inception进行最终执行，并返回执行结果。
        '''
        strBackup = ""
        if workflowDetail.is_backup == 1:
            strBackup = "--enable-remote-backup;"
        else:
            strBackup = "--disable-remote-backup;"

        # 根据inception的要求，执行之前最好先split一下
        sqlSplit = "/*--user=%s; --password=%s; --host=%s; --enable-execute;--port=%s; --enable-ignore-warnings;--enable-split;*/\
             inception_magic_start;\
             %s\
             inception_magic_commit;" % (
        dictConn['masterUser'], dictConn['masterPassword'], dictConn['masterHost'], str(dictConn['masterPort']),
        workflowDetail.sql_content)
        splitResult = mdb(sqlSplit, self.inception_host, self.inception_port, '', '', '')
        print("splitResult", splitResult)

        tmpList = []
        # 对于split好的结果，再次交给inception执行.这里无需保持在长连接里执行，短连接即可.
        for splitRow in splitResult:
            print(sqlSplit)
            sqlTmp = splitRow[1]
            sqlExecute = "/*--user=%s;--password=%s;--host=%s;--enable-execute;--port=%s; --enable-ignore-warnings;%s*/\
                    inception_magic_start;\
                    %s\
                    inception_magic_commit;" % (
            dictConn['masterUser'], dictConn['masterPassword'], dictConn['masterHost'], str(dictConn['masterPort']),
            strBackup, sqlTmp)

            executeResult = mdb(sqlExecute, self.inception_host, self.inception_port, '', '', '')
            print("executeResult", executeResult)
            tmpList.append(executeResult)
        print(tmpList)

        # 二次加工一下，目的是为了和sqlautoReview()函数的return保持格式一致，便于在detail页面渲染.
        finalStatus = 8
        finalList = []
        for splitRow in tmpList:
            for sqlRow in splitRow:
                # 如果发现任何一个行执行结果里有errLevel为1或2，并且stagestatus列没有包含Execute Successfully字样，则判断最终执行结果为有异常.
                if (sqlRow[2] == 1 or sqlRow[2] == 2) and re.match(r"\w*Execute Successfully\w*", sqlRow[3]) is None:
                    finalStatus = 7
                finalList.append(list(sqlRow))

        return (finalStatus, finalList)

    def getRollbackSqlList(self, workflowId):
        workflowDetail = workflow.objects.get(id=workflowId)
        listExecuteResult = json.loads(workflowDetail.execute_result)
        listBackupSql = []
        for row in listExecuteResult:
            # 获取备份目标库名
            if row[8] == 'None':
                continue;
            backupDbName = row[8]
            sequence = row[7]
            opidTime = sequence.replace("'", "")
            sqlTable = "select tablename from %s.$_$Inception_backup_information$_$ where opid_time='%s';" % (
            backupDbName, opidTime)
            listTables = mdb(sqlTable, self.inception_remote_backup_host, self.inception_remote_backup_port,
                                        self.inception_remote_backup_user, self.inception_remote_backup_password, '')
            if listTables is None or len(listTables) != 1:
                print("Error: returned listTables more than 1.")

            tableName = listTables[0][0]
            sqlBack = "select rollback_statement from %s.%s where opid_time='%s'" % (backupDbName, tableName, opidTime)
            listBackup = mdb(sqlBack, self.inception_remote_backup_host, self.inception_remote_backup_port,
                                        self.inception_remote_backup_user, self.inception_remote_backup_password, '')
            if listBackup is not None and len(listBackup) != 0:
                for rownum in range(len(listBackup)):
                    listBackupSql.append(listBackup[rownum][0])
        return listBackupSql




























