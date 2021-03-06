from django.shortcuts import render
from kouyu100_managent.settings import users
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
        response = users.get(ret)
        dataObj.success(response)
        return Response(dataObj.ret())


class Logout(APIView):
    @staticmethod
    def post(request):
        ret = {'code': 20000, 'data': 'success'}
        return Response(ret)
