from django.db import models


# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=16)
    password = models.CharField(max_length=15)

    class Meta:
        verbose_name_plural = "注册用户表"

    def __str__(self):
        return self.username


class MonitorECS(models.Model):
    """
    ECS
    """
    name = models.CharField('机器名称', max_length=64, unique=True)
    ecs_id = models.CharField('实例ID', max_length=64, unique=True)
    inner_ip = models.CharField('内网IP', max_length=32, unique=True)
    pub_ip = models.CharField('外网IP', max_length=32, unique=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "机器实例表"

    def __str__(self):
        return self.name


class MonitorSLB(models.Model):
    """
    负责均衡
    """
    name = models.CharField('负责均衡名称', max_length=64, unique=True)
    slb_id = models.CharField('负载均衡ID', max_length=64, unique=True)
    ip = models.CharField('Ip地址', max_length=32, unique=True)
    tag = models.CharField('Tag标签', max_length=32, null=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "负载均衡表"

    def __str__(self):
        return self.name


class MonitorSlbLoad(models.Model):
    """
    ECS 权重
    """
    slb = models.ForeignKey('MonitorSLB', verbose_name='所属SLB', null=True, blank=True, related_name='ownSlb',
                            on_delete=models.CASCADE)
    ecs = models.ForeignKey('MonitorECS', verbose_name='ECS机器', null=True, blank=True, related_name='ownEcs',
                            on_delete=models.CASCADE)
    ecs_load = models.IntegerField('ecs_load', null=True)
    update_time = models.DateField(auto_now=True)

    class Meta:
        verbose_name_plural = "ECS权重表"

    def __str__(self):
        return self.ecs_load

    __repr__ = __str__
