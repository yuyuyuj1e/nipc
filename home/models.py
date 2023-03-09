from django.db import models


# Create your models here.
class Vul(models.Model):
    # 漏洞编号
    no = models.CharField(max_length=20, blank=True, null=True)
    # 漏洞名称
    name = models.TextField(blank=True, null=True)
    # cve编号
    cve = models.CharField(max_length=15, blank=True, null=True)
    # cwe
    class_field = models.TextField(db_column='class', blank=True, null=True)
    # 发布时间
    publishtime = models.DateTimeField(blank=True, null=True)
    # 更新时间
    updatetime = models.DateTimeField(blank=True, null=True)
    # 描述
    description = models.TextField(blank=True, null=True)
    # cvss
    cvss_cve = models.TextField(blank=True, null=True)
    level_choices = (
        (0, "未知"),
        (1, "低危"),
        (2, "中危"),
        (3, "高危"),
    )
    # 危险等级
    level = models.IntegerField(blank=True, null=True, choices=level_choices)
    a_v = models.TextField(blank=True, null=True)
    a_c = models.TextField(blank=True, null=True)
    auth = models.TextField(blank=True, null=True)
    poc = models.TextField(blank=True, null=True)
    affect = models.TextField(blank=True, null=True)
    solution = models.TextField(blank=True, null=True)
    # 来源
    source = models.TextField(blank=True, null=True)
    # 点击次数
    clicknum = models.IntegerField(blank=True, null=True)
    url = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vul_new'
