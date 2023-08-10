from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .models import Photo
from .models import Comment
from .models import Like
from account.models import Account
from django.contrib.auth.models import User
import json

#Realiza o upload de uma imagem
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload(request):
    uploaded_photo = request.FILES['file']

    author = request.POST['author']
    try:
        user = User.objects.get(username=author)
    except:
        return HttpResponse('Usuário inexistente', status=404)

    img = Photo(image=uploaded_photo, author=user)
    img.save()

    return HttpResponse('OK')


#Lista as imagens autorizadas
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_photos(request):
    photos = list(Photo.objects.filter(is_visible=True).values())
    return HttpResponse(photos)


#Faz o envio de uma imagem, passando como parâmetro o id dela
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def send_photo(request, photo_id):
    try:
        photo = Photo.objects.get(id=photo_id, is_visible=True)
        photo_path = f"{settings.BASE_DIR}/{photo.image}"
        p = open(photo_path, 'rb')
        
        return HttpResponse(p)
    except:
        return HttpResponse('Foto não autorizada ou inexistente', status=404)


#Lista todas as imagens
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_all_photos(request):
    photos = list(Photo.objects.all().values())

    return HttpResponse(photos)


#Cadastra comentários dos usuários. Precisa passar na requisição, o o username do usuário e o id da foto. 
# Ex: {"author": "danield", "photo": 1, "comment": "muito legal isso"}
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment(request):
    json_data = json.loads(request.body.decode('utf-8'))
    try:
        json_data['author'] = User.objects.get(username=json_data['author'])
        json_data['photo'] = Photo.objects.get(id=json_data['photo'])
    except:
        return HttpResponse("Foto ou usuário inexistente", status=404)

    comment = Comment(author=json_data['author'], photo=json_data['photo'], comment=json_data['comment'])
    comment.save()

    return HttpResponse('OK')


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def like(request):
    json_data = json.loads(request.body.decode('utf-8'))

    try:
        user = User.objects.get(username=json_data['author'])
        photo = Photo.objects.get(id=json_data['photo'])
    except:
        return HttpResponse("Foto ou usuário inexistente", status=404)

    like = Like.objects.filter(author=user, photo=photo)
    if like.exists():
        photo.likes -= 1
        like.delete()
    else:
        photo.likes += 1
        like = Like(author=user, photo=photo)
        like.save()
    photo.save()

    return HttpResponse('OK')


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def photo_authorize(request):
    json_data = json.loads(request.body.decode('utf-8'))

    try:
        user = User.objects.get(username=json_data['author'])
        account = Account.objects.get(user=user)
    except:
        return HttpResponse("Usuário inexistente", status=404)

    photo = Photo.objects.get(id=json_data['photo'])

    if account.authority:
        photo.is_visible = json_data['authorize']
        photo.save()
    else:
        return HttpResponse("Ação não autorizada!", status=403)

    return HttpResponse('OK')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_all_comments(request):
    comments = list(Comment.objects.all().values())
    return HttpResponse(comments)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_comments_by_photo(request, photo_id):
    comments = list(Comment.objects.filter(photo=photo_id).values())
    return HttpResponse(comments)