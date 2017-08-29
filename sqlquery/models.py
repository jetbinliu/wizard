from django.db import models

# Create your models here.

# 存放各个SQL上线工单的详细内容，可定期归档或清理历史数据，也可通过alter table workflow row_format=compressed; 来进行压缩
class workflow(models.Model):
    workflow_name = models.CharField('工单名称', max_length=50)
    engineer = models.CharField('发起人', max_length=15)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    cluster_name = models.CharField('集群名称', max_length=50)     # 和master_config表的cluster_name列关联
    cluster_db = models.CharField('库名', max_length=64, default='')
    sql_content = models.TextField('具体sql内容')
    field_names = models.CharField('列名', max_length=2000, default='')
    query_results = models.TextField('查询结果的JSON格式')
