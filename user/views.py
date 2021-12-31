from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from user.model_data import DbUploader
from user.models import User
from user.serializers import UserSerializer
from rest_framework.authtoken.models import Token



@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@parser_classes([JSONParser])
def users(request):
    if request.method == 'GET':
        all_users = User.objects.all().values()
        serializer = UserSerializer(all_users, many=True)
        return JsonResponse(data=serializer.data, safe=False)
    elif request.method == 'POST':
        new_user = request.data
        print(new_user)
        serializer = UserSerializer(data=new_user)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'join': 'SUCCESS'})
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        modifyemail = request.data
        try:
            user = User.objects.get(id=modifyemail['id'])
            dbuser = User.objects.all().filter(id=modifyemail['id']).values()[0]
            for i in modifyemail:
                dbuser[i] = modifyemail[i]
            serializer = UserSerializer(data=dbuser)
            if serializer.is_valid():
                serializer.update(user, dbuser)
            return JsonResponse({'modify': 'SUCCESS'})
        except:
            return JsonResponse({'modify': '수정하고자 하는 user가 없습니다.'})
    # elif request.method == 'DELETE':
    #     deluser = request.data
    #     try:
    #         dbuser = User.objects.get(user_email=deluser['email'])
    #         if deluser['user_email'] == dbuser.user_email:
    #             dbuser.delete()
    #             return JsonResponse({'remove': 'SUCCESS'})
    #     except:
    #         return JsonResponse({'remove': 'error 지우고자 하는 user가 없습니다.'})



@api_view(['POST'])
@parser_classes([JSONParser])
def login(request):
    loginuser = request.data
    dbUser = User.objects.all().filter(user_email=loginuser['email']).values()[0]
    if loginuser['password'] == dbUser['password']:
        # token = Token.objects.create(user_email=loginuser['email'])
        # print(f'생성된 토큰값 : {token}')
        userSerializer = UserSerializer(data=dbUser, many=False)
        print(userSerializer)
        if userSerializer.is_valid():
            return JsonResponse(data=userSerializer.data, safe=False)
        print(userSerializer.errors)
        return JsonResponse(userSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def user(request):
    try:
        finduser = request.data
        dbUser = User.objects.all().filter(user_email=finduser['email']).values()[0]
        return JsonResponse(data=dbUser, safe=False)
    except:
        return JsonResponse({'find': 'fail'})


@api_view(['GET'])
@parser_classes([JSONParser])
def exist(request, email):
    try:
        gettest = User.objects.get(user_email=email)
        return JsonResponse(data={'exist': '해당 이메일은 있습니다'}, status=status.HTTP_404_NOT_FOUND)
    except:
        return JsonResponse({'exist': '해당 이메일은 사용 가능합니다'})


@api_view(['DELETE'])
def remove(request, email):
    dbuser = User.objects.get(user_email=email)
    dbuser.delete()
    return JsonResponse({'remove': 'SUCCESS'})


# @api_view(['GET'])
# @parser_classes([JSONParser])
# def upload(request):
#     print('######## 1 ########')
#     DbUploader().insert_data()
#     return JsonResponse({'Product Upload': 'SUCCEESS'})
