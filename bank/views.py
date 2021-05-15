from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status, permissions
from bank.serializers import RegisterUserSerializer,LoginUserSerializers,AccountSerializers,transactionserializer
from rest_framework.authtoken.models import Token
from .models import Accounts,transactions
# Create your views here.
class registeruser(APIView):
    def post(self,request):
        serializer=RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class loginuserview(APIView):
    def post(self,request):
        serializer = LoginUserSerializers(data=request.data)
        if serializer.is_valid():
            print("works")
            username = serializer.validated_data.get("username")
            password = serializer.validated_data.get("password")
            # user = authenticate(request, username=username, password=password)
            user=User.objects.get(username=username)
            if (user.username==username)&(user.password==password):
                login(request, user)
                token,created= Token.objects.get_or_create(user=user)
                return Response({"token":token.key},status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountDetailsView(APIView):
    authentication_classes = [TokenAuthentication,BasicAuthentication ]
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request):
        lst = Accounts.objects.last()
        if lst:

            lstacc=lst.acc_no
            lstacc+=1


        else:
            lstacc=1000
        request.data["acc_no"]=lstacc
        # request.data["user"]=request.User
        serializer=AccountSerializers(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class TransactionView(APIView):
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request,acc_no):
        faccount = Accounts.objects.get(acc_no=acc_no)
        request.data["fromacc"]=acc_no
        serializer=transactionserializer(data=request.data)

        if serializer.is_valid():
            amt=serializer.validated_data.get("amt")
            toacc=serializer.validated_data.get("toacc")
            # fromacc=serializer.validated_data.get("fromacc")


            taccount=Accounts.objects.get(acc_no=toacc)
            if (faccount.bal>=amt) & (toacc==taccount.acc_no):
                faccount.bal-=amt
                taccount.bal+=amt
                faccount.save()
                taccount.save()
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response("accno errror or insuff bal", status=status.HTTP_400_BAD_REQUEST)

class balanceView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,acc_no):
        bal=Accounts.objects.get(acc_no=acc_no)
        if bal:
            serializer=AccountSerializers(bal)
            return Response("Balance ="+str(serializer.data["bal"]), status=status.HTTP_200_OK)

class transactionhistview(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,acc_no):
        trn=transactions.objects.filter( toacc=acc_no) | transactions.objects.filter (fromacc=acc_no)
        serializer=transactionserializer(trn,many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)

class credittransaction(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,acc_no):
        trn = transactions.objects.filter(toacc=acc_no)
        serializer = transactionserializer(trn, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class debittransaction(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,acc_no):
        trn=transactions.objects.filter(fromacc=acc_no)
        serializer = transactionserializer(trn, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


