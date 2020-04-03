from django.conf.urls import url
from user import views

urlpatterns = [
    # 登录功能
    url(r'login/$', views.Login.as_view(), name='login'),
    url(r'info/$', views.UserInfo.as_view(), name='userInfo'),
    url(r'logout/$', views.Logout.as_view(), name='logout'),
]
