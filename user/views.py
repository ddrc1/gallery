from django.http import HttpResponse
from .models import User
import pandas as pd

#Carrega um arquivo .ods, .xlsx, .xlx ou csv. Esse arquivo deve conter as colunas username, firstname, lastname, password e authority.
#Cada linha representa um usuário. O username é um atributo único. 
# Caso o arquivo seja recarregado ou possua 2 usuarios com o mesmo username, os objeto serão atualizado no banco
def user_import(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        filename = uploaded_file.name
        if '.csv' in filename:
            df = pd.read_csv(uploaded_file)
            df['authority'] = df['authority'].apply(lambda x: True if x == 'True' else False)
        else: 
            df = pd.read_excel(uploaded_file)

        df = df[['username', 'firstname', 'lastname', 'password', 'authority']]
        #df['password'] = df['password'].apply(lambda x: str(uuid.uuid5(x))) #encriptar senha
        
        for user in df.itertuples():
            existing_user = User.objects.filter(username=user[1])
            if existing_user.exists():
                existing_user = existing_user[0]
                existing_user.username = user[1]
                existing_user.firstname = user[2]
                existing_user.lastname = user[3]
                existing_user.password = user[4]
                existing_user.authority = user[5]
                existing_user.save()
            else:
                u = User(username=user[1], firstname=user[2], lastname=user[3], password=user[4], authority=user[5])
                u.save()
        return HttpResponse("OK")
    return HttpResponse('Method not allowed', status=405)

#Retorna a lista de todos os usuários cadastrados no banco
def user_list(request):
    if request.method == 'GET':
        users = list(User.objects.all().values())
        return HttpResponse(users)
    return HttpResponse('Method not allowed', status=405)