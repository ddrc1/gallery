from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Account
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import pandas as pd

#Carrega um arquivo .ods, .xlsx ou .xlx. Esse arquivo deve conter as colunas username, firstname, lastname, password e authority.
#Cada linha representa um usuário. O username é um atributo único. 
# Caso o arquivo seja recarregado ou possua 2 usuarios com o mesmo username, os objeto serão atualizado no banco
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_import(request):
    #if request.method == 'POST':
    uploaded_file = request.FILES['file']
    df = pd.read_excel(uploaded_file)
    df['password'] = df['password'].astype(str)

    df = df[['username', 'password', 'firstname', 'lastname', 'authority']]
    
    for user in df.itertuples():
        existing_user = User.objects.filter(username=user[1])
        if existing_user.exists():
            existing_user = existing_user[0]
            existing_user.first_name = user[3]
            existing_user.last_name = user[4]
            existing_user.save()
            
            acc = Account.objects.get(user=existing_user)
            acc.authority = user[5]
            acc.save()
        else:
            u = User.objects.create_user(username=user[1], password=user[2], first_name=user[3], last_name=user[4])
            u.save()
            acc = Account(user=u, authority=user[5])
            acc.save()
    return HttpResponse("OK")


#Retorna a lista de todos os usuários cadastrados no banco
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_list(request):
    users = list(Account.objects.all().values())
    return HttpResponse(users)