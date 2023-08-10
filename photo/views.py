from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from django.conf import settings
from .models import Photo
from .models import Comment
from .models import Like
from account.models import Account
from django.contrib.auth.models import User
import json

@swagger_auto_schema(method='post', operation_description="Realiza o upload de uma imagem",
    responses={200: 'OK', 401: 'Unauthorized', 404: 'Usuário inexistente'})
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


@swagger_auto_schema(method='get', operation_description="Lista as imagens autorizadas",
    responses={200: 'OK', 401: 'Unauthorized'})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_photos(request):
    photos = list(Photo.objects.filter(is_visible=True).values())
    return HttpResponse(photos)


@swagger_auto_schema(method='get', operation_description="Faz o envio de uma imagem, passando como parâmetro o id dela",
    manual_parameters=[], responses={200: 'OK', 401: 'Unauthorized', 404: 'Foto não autorizada ou inexistente'})
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


@swagger_auto_schema(method='get', operation_description="Lista todas as imagens",
    responses={200: 'OK', 401: 'Unauthorized'})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_all_photos(request):
    photos = list(Photo.objects.all().values())

    return HttpResponse(photos)


@swagger_auto_schema(method='post', operation_description="Cadastra comentários dos usuários. Precisa passar na requisição, o o username do usuário e o id da foto.",
    responses={200: 'OK', 401: 'Unauthorized', 404: 'Foto ou usuário inexistente'})
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


@swagger_auto_schema(method='put', operation_description="Adiciona ou remove o like da imagem",
    responses={200: 'OK', 401: 'Unauthorized', 404: 'Foto ou usuário inexistente'})
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


@swagger_auto_schema(method='put', operation_description="Autoriza uma imagem",
    responses={200: 'OK', 401: 'Unauthorized', 404: 'Usuário inexistente', 403: "Ação proibida"})
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
        return HttpResponse("Ação proibida", status=403)

    return HttpResponse('OK')


@swagger_auto_schema(method='get', operation_description="Lista todos os comentários",
    responses={200: 'OK', 401: 'Unauthorized'})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_all_comments(request):
    comments = list(Comment.objects.all().values())
    return HttpResponse(comments)


@swagger_auto_schema(method='get', operation_description="Lista todos os comentários de uma foto",
    responses={200: 'OK', 401: 'Unauthorized'})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_comments_by_photo(request, photo_id):
    comments = list(Comment.objects.filter(photo=photo_id).values())
    return HttpResponse(comments)