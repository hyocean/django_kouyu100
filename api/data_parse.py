from .aliyun_api import SLB, ECS
from message_db import models
from api.hawkeye import hawkeye_select_status
import datetime


# Create your views here.


def slb_update_db():
    """
    更新数据库slb表
    :return:
    """
    slb_page_count = SLB().loadBalancingCreated(1).get('TotalCount') // 50 + 2

    for slb_page in range(1, slb_page_count):
        response = SLB().loadBalancingCreated(slb_page).get('LoadBalancers').get('LoadBalancer')
        for info in response:
            slb_name, slb_id, slb_ip, slb_tag = info.get('LoadBalancerName'), \
                                                info.get('LoadBalancerId'), \
                                                info.get('Address'), \
                                                info.get('Tags').get('Tag')[0]['TagKey'] if info.get('Tags').get(
                                                    'Tag') else None
            models.MonitorSLB.objects.update_or_create(slb_id=slb_id, defaults={
                'name': slb_name,
                'ip': slb_ip,
                'tag': slb_tag
            })

    time_now = datetime.datetime.now().strftime("%Y-%m-%d")
    models.MonitorSLB.objects.filter(update_time__lt=time_now).delete()
    return True


def ecs_update_db():
    """
        更新ECS数据库表
        :return:
        """
    ecs_TotalCount = ECS().ecs_detail().get('TotalCount') // 100 + 2
    for page in range(1, ecs_TotalCount):
        response = ECS().ecs_detail(page)['Instances']['Instance']
        for ecs_message in response:
            NetWorkType = ecs_message.get('InstanceNetworkType')
            print(NetWorkType)
            if NetWorkType == 'vpc':
                inner_ip = ecs_message.get('VpcAttributes').get('PrivateIpAddress').get('IpAddress')[0]
            else:
                inner_ip = ecs_message.get('InnerIpAddress').get('IpAddress')[0]

            ecs_name, ecs_id, pub_ip = ecs_message.get('InstanceName'), \
                                       ecs_message.get('InstanceId'), \
                                       ecs_message.get('PublicIpAddress').get('IpAddress')[0]

            print(ecs_name, ecs_id, inner_ip, pub_ip)
            models.MonitorECS.objects.update_or_create(ecs_id=ecs_id, defaults={
                'name': ecs_name,
                'inner_ip': inner_ip,
                'pub_ip': pub_ip,
            })

    time_now = datetime.datetime.now().strftime("%Y-%m-%d")
    models.MonitorECS.objects.filter(update_time__lt=time_now).delete()
    return True


def slb_ecs_update_load():
    """
    更新数据库服务器权重表
    :return:
    """
    # 获取数据库中slb表的所有ID及name
    ret = models.MonitorSLB.objects.all().values('name', 'slb_id', 'ip')
    for i in ret:
        slb_id = i['slb_id']
        ecs_weights = SLB().ecs_load_status(slb_id)['BackendServers']['BackendServer']
        for n in ecs_weights:
            server_id, server_weight, server_type = n['ServerId'], int(n['Weight']), n['Type']
            if server_type == 'ecs':
                ecsObj = models.MonitorECS.objects.filter(ecs_id=server_id).first()
                slbObj = models.MonitorSLB.objects.filter(slb_id=slb_id).first()

                models.MonitorSlbLoad.objects.update_or_create(ecs_id=ecsObj.pk, slb_id=slbObj.pk, defaults={
                    'ecs_id': ecsObj.pk,
                    'ecs_load': server_weight,
                    'slb_id': slbObj.pk,
                })
 
    time_now = datetime.datetime.now().strftime("%Y-%m-%d")
    models.MonitorSlbLoad.objects.filter(update_time__lt=time_now).delete()
    return True


def get_loads_ecsInfo():
    """
    权重数据返回接口
    :return:
    """
    slblist = []
    SLBDict = models.MonitorSLB.objects.all()
    for slbObj in SLBDict:
        try:
            ecs_list = []
            for i in slbObj.ownSlb.all():
                name = models.MonitorECS.objects.filter(pk=i.ecs_id).first().name
                ecs_dict = {'id': i.ecs_id, 'name': name, 'load': i.ecs_load,
                            'monitor_status': hawkeye_select_status(i.ecs_id)}
                ecs_list.append(ecs_dict)
            objParse = {
                'id': slbObj.id,
                'slb': slbObj.name,
                'ecs_list': ecs_list,
            }
            slblist.append(objParse)
        except IndexError:
            pass
    return slblist


def post_update_slbInfo(params):
    ret_dict = {}
    ecs = models.MonitorECS.objects.filter(pk=params.get('ecs')).first()
    slb = models.MonitorSLB.objects.filter(pk=params.get('slb')).first()
    retObj = models.MonitorSlbLoad.objects.filter(slb=slb.pk, ecs=ecs.pk).first()

    ecsId = ecs.ecs_id if ecs else None
    slbId = slb.slb_id if slb else None
    weight = params.get('weight')

    if not ecsId or not slbId or not type(weight) is int:
        ret_dict['message'] = 'ECS实例或负载均衡实例不存在'
        ret_dict['status'] = False
        return ret_dict
    response = SLB().request_slb_load(slbId=slbId, ecsId=ecsId, weight=weight)
    responseIter = filter(lambda x: x.get('ServerId') == ecsId, response['BackendServers']['BackendServer'])
    response_list = list(responseIter)

    if len(response_list) == 1:
        ret_ecs = response_list[0].get('ServerId')
        ret_weight = response_list[0].get('Weight')
        if ret_ecs == ecsId and ret_weight == weight:
            retObj.ecs_load = ret_weight
            retObj.save()
            ret_dict['slb'], ret_dict['ecs'], ret_dict['current_weight'] = slb.name, ecs.name, retObj.ecs_load
    return ret_dict
