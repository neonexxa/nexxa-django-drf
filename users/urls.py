from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
	# path('ActivateUser/', views.ActivateUser.as_view(), name='ActivateUser'),
	# path('VerifyUser/', views.VerifyUser.as_view(), name='VerifyUser'),
	# path('UpdateUser/', views.UpdateUser.as_view(), name='UpdateUser'),
	path('ForgotPassword/', views.ForgotPassword.as_view(), name='ForgotPassword'),
	path('RequestForgotPassword/', views.RequestForgotPassword.as_view(), name='RequestForgotPassword'),
	# path('Asset/', include('companyasset.urls')),
	# path('SupportAdmin/', include('support.urls')),
	# path('Wallet/', include('wallet.urls')),
	# path('ListFileCredential/', views.ListFileCredential.as_view(), name='ListFileCredential'),
	# path('UploadFileCredential/', views.UploadFileCredential.as_view(), name='UploadFileCredential'),
	# path('payment/', include('payments.urls')),
	# path('Configs/', include('appconfigs.urls')),
	path('', include(router.urls)),
]