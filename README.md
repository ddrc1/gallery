# gallery
Passo a passo para executar o código:
- execute pip install -r requirements.txt
- python manage.py migrate
- python manage.py makemigrations
- python manage.py runserver 0.0.0.0:8000

É necessário ter instalado e configurado o postgres. Em gallery/galery/setting.py, na variável DATABASES, encontra-se as configurações do banco. Modifique-as!
