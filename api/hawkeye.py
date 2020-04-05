from api.mysqlApi import my_custom_sql
from message_db import models
from kouyu100_managent import settings

table_list = settings.hawkeye_list


def process_status(value):
    if 0 in value:
        return 0
    elif 1 in value and 0 not in value:
        return 1
    else:
        return None


def hawkeye_select_status(pk):
    ecs_obj = models.MonitorECS.objects.filter(pk=pk).first()

    if ecs_obj is not None:
        name, inner = ecs_obj.name, ecs_obj.inner_ip
    else:
        name, inner = None, None

    with my_custom_sql() as hawkeye:
        cc = set()
        for table in table_list:
            monitor_status = hawkeye(
                "select status from {2} where name='{0}' or innerIp='{1}';".format(name, inner, table))
            response = monitor_status.fetchone()
            cc.add(response[0]) if response else cc.add(response)
        ret = process_status(cc)
        return ret


def hawkeye_update_status(data):
    status, pk = data.get('status'), data.get('pk')
    ecsObj = models.MonitorECS.objects.filter(pk=pk).first()

    if not ecsObj:
        return None
    name, inner = ecsObj.name, ecsObj.inner_ip

    ret_status = False
    with my_custom_sql() as hawkeye:
        for table in table_list:
            monitor_update = hawkeye(
                "update {2} set status='{3}' where name='{0}' or innerIp='{1}';".format(name, inner, table, status))
            if monitor_update.rowcount >= 1:ret_status = True

    current_status = hawkeye_select_status(pk)
    ret = {'ecs': name, 'update_status': ret_status, 'status': current_status}
    return ret
