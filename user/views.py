from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.response import Response
from api.restful_data_response import RestFulObject


# Create your views here.


class Login(ObtainAuthToken):
    http_method_names = ['get', 'post']
    dataObj = RestFulObject()

    def post(self, request, *args, **kwargs):
        dataObj = RestFulObject()
        try:
            serializer = self.serializer_class(data=request.data,
                                               context={'request': request})
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            ret = {'token': token.key}
            dataObj.success(ret)
        except Exception:
            dataObj.error('账户或密码输入不正确！')
            return Response(dataObj.ret())
        return Response(dataObj.ret())


class UserInfo(APIView):

    @staticmethod
    def get(request, *args, **kwargs):
        dataObj = RestFulObject()
        ret = request.GET.get('token')
        users = {
            '0abe17837ede9c0b98166c5dcb0f1426024f85c9': {
                "roles": ['root'],
                "introduction": 'I am a super administrator',
                "avatar": 'http://pic4.zhimg.com/50/v2-548c55b76dc4c76a8b382168505bceef_hd.jpg',
                "name": 'root'
            }}
        response = users.get(ret)
        dataObj.success(response)
        return Response(dataObj.ret())


class Logout(APIView):
    @staticmethod
    def post(request):
        ret = {'code': 20000, 'data': 'success'}
        return Response(ret)
