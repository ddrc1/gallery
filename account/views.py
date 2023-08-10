from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Account
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
import pandas as pd

@swagger_auto_schema(method='post', operation_description="Carrega um arquivo .ods, .xlsx ou .xlx. Esse arquivo deve conter as colunas username, firstname, lastname, " + \
    "password e authority. Caso o arquivo seja recarregado ou possua 2 usuarios com o mesmo username, os objeto serão atualizado no banco. " + \
    "Caso o arquivo seja recarregado ou possua 2 usuarios com o mesmo username, os objeto serão atualizado no banco",
    responses={200: 'OK', 401: 'Unauthorized'})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_import(request):
    uploaded_file = request.FILES['file']
    df = pd.read_excel(uploaded_file)
    df['password'] = df['password'].astype(str)

    df = df[['username', 'password', 'firstname', 'lastname', 'authority']]
    
    for user in df.itertuples():
        existing_user = User.objects.filter(username=user[1])
        print(existing_user)
        if existing_user.exists():

            existing_user = existing_user[0]
            existing_user.first_name = user[3]
            existing_user.last_name = user[4]
            existing_user.save()
            
            try:
                acc = Account.objects.get(user=existing_user)
                acc.authority = user[5]
            except:
                acc = Account(user=existing_user, authority=user[5])
            acc.save()
        else:
            u = User.objects.create_user(username=user[1], password=user[2], first_name=user[3], last_name=user[4])
            u.save()
            acc = Account(user=u, authority=user[5])
            acc.save()
    return HttpResponse("OK")


@swagger_auto_schema(method='get', operation_description="Retorna a lista de todos os usuários cadastrados no banco",
    responses={200: 'OK', 401: 'Unauthorized'})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_list(request):
    users = list(Account.objects.all().values())
    return HttpResponse(users)