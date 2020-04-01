from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 

from .models import User
from .serializers import UserSerializer

from google.cloud import storage
from django.conf import settings
import json
from os import urandom
from django.core.mail import send_mail

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# bucketName = settings.GCP_BUCKET_NAME
# storage_client = storage.Client()
# bucket = storage_client.get_bucket(settings.GCP_BUCKET_NAME)

class AttrDict(dict):
    def __getattr__(self, item):
        return self[item]

class ForgotPassword(APIView):
    """docstring for ForgotPassword"""
    def get(self, request):
        return render(request, 'password_reset.html', {})
    def post(self, request):
        json_data = json.loads(request.body)
        print("json_data['reset_token']",json_data['reset_token'])
        try:
            current_user = User.objects.get(reset_token=json_data['reset_token'])
        except Exception as e:
            content = {
                "status" : False,
                "message": "Something wrong somewhere: "+e
            }
            return Response(content)
        
        print("Trigger Request for password_reset")
        try:
            current_user.__dict__.update(reset_token=None)
            current_user.set_password(json_data['password'])
            current_user.save()
            content = {
                "status" : True,
                "message": "Password has beeen reset."
            }
        except Exception as e:
            print("oppes", e)
            content = {
                "status" : False,
                "message": "Something wrong somewhere."
            }
        return Response(content)
class RequestForgotPassword(APIView):
    """docstring for ForgotPassword"""
    def post(self, request):
        json_data = json.loads(request.body)
        try:
            current_user = User.objects.get(email=json_data['email'])
            reset_token = urandom(9).hex()
            current_user.__dict__.update(reset_token=reset_token)
            current_user.save()
            send_mail(
                '[LORRY135] Request For Password Reset',
                'Please follow the link to reset your password: https://elorry.appspot.com/api/ForgotPassword/?token='+reset_token,
                'kacangcreativestudios@gmail.com',
                [current_user.email]
            )
            print("Trigger password reset for:"+current_user.email)
            content = {
                "status" : True,
                "message": "Password reset link has been email to user."
            }
        except Exception as e:
            print("opps ", e)
            content = {
                "status" : False,
                "message": "Opps Something Wrong Somewhere."
            }
        return Response(content)
