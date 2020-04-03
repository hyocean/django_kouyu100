import json
from .data_parse import slb_update_db, ecs_update_db, slb_ecs_update_load, get_loads_ecsInfo, post_update_slbInfo
from api.hawkeye import hawkeye_update_status
from .restful_data_response import RestFulObject
import logging
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

log = logging.getLogger('mydjango')


class DataCollection(APIView):
    """
    slb数据ecs更新
    """

    @staticmethod
    def get(request):
        dataObj = RestFulObject()
        try:
            slb_message = slb_update_db()
            ecs_message = ecs_update_db()
            response = {'slb_status': slb_message, 'ecs_status': ecs_message}
            dataObj.success(response)
        except Exception as e:
            log.error(e)
            dataObj.error('数据库ecs和slb数据更新失败')

        response = dataObj.ret()
        return Response(response)


class UpdateDbSlbLoads(APIView):
    """
    更新数据库中 对应机器的负载均衡 权重
    """

    @staticmethod
    def get(request):
        dataObj = RestFulObject()
        try:
            update_status = slb_ecs_update_load()
            response = {'update_status': update_status}
            dataObj.success(response)
        except Exception as e:
            log.error(e)
            dataObj.error('权重数据更新失败')

        response = dataObj.ret()
        return Response(response)


class GetDbSlbLoads(APIView):
    """
    获取SLb权重信息
    """
    @staticmethod
    def get(request):
        dataObj = RestFulObject()
        try:
            func = get_loads_ecsInfo()
            response = {'slb_status': func}
            dataObj.success(response)
        except Exception as e:
            log.error(e)
            dataObj.error('权重信息获取失败')

        response = dataObj.ret()
        return Response(response)


class ProcessMonitor(APIView):
    """
    监控更新
    """
    http_method_names = ['post']

    @staticmethod
    def post(request):
        dataObj = RestFulObject()
        try:
            response = request.body.decode('utf-8')
            response = json.loads(response)
            response = hawkeye_update_status(response)
            dataObj.success(response)
        except Exception as e:
            log.error(e)
            dataObj.error('监控更新失败')

        response = dataObj.ret()
        return Response(response)


class ProcessSlbLoad(APIView):
    """
    负载均衡权重更新
    """
    http_method_names = ['post']

    @staticmethod
    def post(request):
        dataObj = RestFulObject()
        try:
            response = request.body.decode('utf-8')
            response = json.loads(response)
            response = post_update_slbInfo(response)
            dataObj.success(response)
        except Exception as e:
            log.error(e)
            dataObj.error('负载均衡权重更新失败')

        response = dataObj.ret()
        return Response(response)
