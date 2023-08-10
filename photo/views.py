from django.http import HttpResponse
from django.conf import settings
from .models import Photo
from .models import Comment
from .models import Like
from user.models import User
import json

#Realiza o upload de uma imagem
def upload(request):
    if request.method == 'POST':
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
def list_photos(request):
    if request.method == 'GET':
        photos = list(Photo.objects.filter(is_visible=True).values())
        return HttpResponse(photos)

    return HttpResponse('Method not allowed', status=405)


#Faz o envio de uma imagem, passando como parâmetro o id dela
def send_photo(request, photo_id):
    if request.method == 'GET':
        try:
            photo = Photo.objects.get(id=photo_id, is_visible=True)
            photo_path = f"{settings.BASE_DIR}/{photo.image}"
            p = open(photo_path, 'rb')
            
            return HttpResponse(p)
        except:
            return HttpResponse('Foto não autorizada ou inexistente', status=404)
    return HttpResponse('Method not allowed', status=405)


#Lista todas as imagens
def list_all_photos(request):
    if request.method == 'GET':
        photos = list(Photo.objects.all().values())

    return HttpResponse(photos)


#Cadastra comentários dos usuários. Precisa passar na requisição, o o username do usuário e o id da foto. 
# Ex: {"author": "danield", "photo": 1, "comment": "muito legal isso"}
def comment(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        try:
            json_data['author'] = User.objects.get(username=json_data['author'])
            json_data['photo'] = Photo.objects.get(id=json_data['photo'])
        except:
            return HttpResponse("Foto ou usuário inexistente", status=404)

        comment = Comment(author=json_data['author'], photo=json_data['photo'], comment=json_data['comment'])
        comment.save()

        return HttpResponse('OK')
    return HttpResponse('Method not allowed', status=405)


def like(request):
    if request.method == 'PUT':
        json_data = json.loads(request.body.decode('utf-8'))
        user = User.objects.get(username=json_data['author'])
        photo = Photo.objects.get(id=json_data['photo'])

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
    return HttpResponse('Method not allowed', status=405)


def photo_authorize(request):
    if request.method == 'PUT':
        json_data = json.loads(request.body.decode('utf-8'))
        user = User.objects.get(username=json_data['author'])
        photo = Photo.objects.get(id=json_data['photo'])

        if user.authority:
            photo.is_visible = json_data['authorize']
            photo.save()
        else:
            return HttpResponse("Ação não autorizada!", status=403)

        return HttpResponse('OK')
    return HttpResponse('Method not allowed', status=405)


def list_all_comments(request):
    if request.method == 'GET':
        comments = list(Comment.objects.all().values())
        return HttpResponse(comments)
    return HttpResponse('Method not allowed', status=405)


def list_comments_by_photo(request, photo_id):
    if request.method == 'GET':
        comments = list(Comment.objects.filter(photo=photo_id).values())
    
        return HttpResponse(comments)
    return HttpResponse('Method not allowed', status=405)