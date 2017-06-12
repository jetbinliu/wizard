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
