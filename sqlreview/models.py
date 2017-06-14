# -*- coding: UTF-8 -*-
from django.db import models

# Create your models here.

# 存放各个SQL上线工单的详细内容，可定期归档或清理历史数据，也可通过alter table workflow row_format=compressed; 来进行压缩
class workflow(models.Model):
    workflow_name = models.CharField('工单内容', max_length=50)
    engineer = models.CharField('发起人', max_length=15)
    review_man = models.CharField('主副审核人JSON格式', max_length=50)  # 主从审核人list通过json序列化后存入, 0位为主审核人
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    finish_time = models.DateTimeField('结束时间', null=True, blank=True)
    status = models.IntegerField('工单状态')
    reject_opinion = models.CharField('驳回意见', max_length=50, default='')
    is_backup = models.IntegerField('是否备份，0为否，1为是', default=1)
    review_content = models.TextField('自动审核内容的JSON格式')
    cluster_name = models.CharField('集群名称', max_length=50)     # 和master_config表的cluster_name列关联
    reviewok_time = models.DateTimeField('人工审核通过的时间', null=True, blank=True)
    sql_content = models.TextField('具体sql内容')
    execute_result = models.TextField('执行结果的JSON格式')

# 工单状态
WORKFLOW_STATUS = {
    1: '自动审核中',
    2: '自动审核不通过',
    3: '等待审核人审核',
    4: '发起人终止',
    5: '审核人驳回',
    6: '执行中',
    7: '执行有异常',
    8: '已正常结束',
}





#inception组件所在的地址
INCEPTION_HOST = '192.168.1.11'
INCEPTION_PORT = '6100'

#查看回滚SQL时候会用到，这里要告诉archer去哪个mysql里读取inception备份的回滚信息和SQL.
#注意这里要和inception组件的inception.conf里的inception_remote_XX部分保持一致.
INCEPTION_REMOTE_BACKUP_HOST='192.168.1.12'
INCEPTION_REMOTE_BACKUP_PORT=5621
INCEPTION_REMOTE_BACKUP_USER='inception'
INCEPTION_REMOTE_BACKUP_PASSWORD='inception'

#是否开启邮件提醒功能：发起SQL上线后会发送邮件提醒审核人审核，执行完毕会发送给DBA. on是开，off是关，配置为其他值均会被archer认为不开启邮件功能
MAIL_ON_OFF='on'

MAIL_REVIEW_SMTP_SERVER='mail.xxx.com'
MAIL_REVIEW_SMTP_PORT=25
MAIL_REVIEW_FROM_ADDR='archer@xxx.com'                                               #发件人，也是登录SMTP server需要提供的用户名
MAIL_REVIEW_FROM_PASSWORD=''                                                         #发件人邮箱密码，如果为空则不需要login SMTP server
MAIL_REVIEW_DBA_ADDR=['zhangsan@abc.com', 'lisi01@abc.com']        #DBA地址，执行完毕会发邮件给DBA，以list形式保存

#是否过滤【DROP DATABASE】|【DROP TABLE】|【TRUNCATE PARTITION】|【TRUNCATE TABLE】等高危DDL操作：
#on是开，会首先用正则表达式匹配sqlContent，如果匹配到高危DDL操作，则判断为“自动审核不通过”；off是关，直接将所有的SQL语句提交给inception，对于上述高危DDL操作，只备份元数据
CRITICAL_DDL_ON_OFF='off'
