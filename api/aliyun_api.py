#!/usr/bin/env python
# coding=utf-8
import json
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest
from aliyunsdkslb.request.v20140515.DescribeLoadBalancersRequest import DescribeLoadBalancersRequest
from aliyunsdkslb.request.v20140515.DescribeLoadBalancerAttributeRequest import DescribeLoadBalancerAttributeRequest
from aliyunsdkslb.request.v20140515.SetBackendServersRequest import SetBackendServersRequest
from kouyu100_managent import settings

client = settings.client

class ECS:
    """
    ECS API
    """

    @staticmethod
    def ecs_detail(page_number=1):
        """
        ecs实例详细信息
        :param page_number: ecs页面页数
        :return:
        """
        request = DescribeInstancesRequest()
        request.set_accept_format('json')
        request.set_PageSize(100)
        request.set_PageNumber(page_number)
        response = client().do_action_with_exception(request)
        response = json.loads(response)
        return response


class SLB:
    """
    SLB API
    """

    @staticmethod
    def slb(ecs_id):
        """
        查询所属ecs的负载均衡情况
        :param ecs_id: ecsid
        :return:
        """
        request = DescribeLoadBalancersRequest()
        request.set_accept_format('json')
        request.set_ServerId(ecs_id)
        response = client().do_action_with_exception(request)
        response = json.loads(response)
        if response.get('TotalCount') == 0:
            return {'slbId': None}
        slbListInfo = response.get('LoadBalancers')['LoadBalancer']
        if len(slbListInfo) > 1:
            slb_id = [i['LoadBalancerId'] for i in slbListInfo]
            return {'slbId': slb_id}
        return {'slbId': slbListInfo[0]['LoadBalancerId']}

    @staticmethod
    def loadBalancingCreated(page_num=1):
        """
        查询所有SLB详细信息
        :param page_num:
        :return:
        """
        request = DescribeLoadBalancersRequest()
        request.set_accept_format('json')
        request.set_PageSize(page_num)
        request.set_PageSize(50)
        response = client().do_action_with_exception(request)
        response = json.loads(response)
        return response

    @staticmethod
    def ecs_load_status(slb_id):
        """
        负载组ECS权重状态
        :param slb_id:
        :return:
        """
        request = DescribeLoadBalancerAttributeRequest()
        request.set_LoadBalancerId(slb_id)
        response = client().do_action_with_exception(request)
        response = json.loads(response)
        return response

    @staticmethod
    def request_slb_load(slbId, ecsId, weight):
        request = SetBackendServersRequest()
        request.set_accept_format('json')
        request.set_LoadBalancerId(slbId)
        request.set_BackendServers([{"ServerId": ecsId, "Weight": weight}])
        response = client().do_action_with_exception(request)
        response = json.loads(response)
        return response
