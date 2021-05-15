"""restbank URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import loginuserview,registeruser,AccountDetailsView,TransactionView,balanceView,transactionhistview,\
    debittransaction,credittransaction


urlpatterns = [
    path("register",registeruser.as_view()),
    path("login",loginuserview.as_view()),
    path("acc",AccountDetailsView.as_view()),
    path("trns/<int:acc_no>",TransactionView.as_view()),
    path("bal/<int:acc_no>",balanceView.as_view()),
    path("this/<int:acc_no>",transactionhistview.as_view()),
    path("this/dbt/<int:acc_no>",debittransaction.as_view()),
    path("this/cdt/<int:acc_no>",credittransaction.as_view())
]
