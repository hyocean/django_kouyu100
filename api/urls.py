from django.conf.urls import url
from api import views

urlpatterns = [
    # 登录功能
    # url(r'api-token/$', views.CustomAuthToken.as_view()),

    # 数据库更新接口
    url(r'database_update/slb_ecs_info/$', views.DataCollection.as_view(), name='database_update'),
    url(r'database_update/slb_load_info/$', views.UpdateDbSlbLoads.as_view(), name='slb_load_info'),

    # 获取slb负载监控信息
    url(r'getSlbLoadInfo/$', views.GetDbSlbLoads.as_view(), name='slb_status'),

    # hawkeye监控鹰眼更新
    url(r'process_monitor/$', views.ProcessMonitor.as_view(), name='process_monitor'),

    # slb权重更新
    url(r'process_slb_load/$', views.ProcessSlbLoad.as_view(), name='process_slb_load'),
]
