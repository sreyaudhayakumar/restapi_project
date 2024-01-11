from django.shortcuts import render
from asyncio.windows_events import NULL
from rest_framework.response import Response
from .models import Person
from rest_framework import status, permissions
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Create your views here.
def success_response(response, status_code=None):
    json_obj = {
        "hasError": False,
        "errorCode": -1,
        "message": "Success",

    }
    json_obj["response"] = response
    if status_code is None:
        return Response(json_obj, status=status.HTTP_200_OK)
    return Response(json_obj, status=status_code)


def failure_response(response, status_code=None, error_code=1001, message="Failure"):
    json_obj = {
        "hasError": True,
        "errorCode": error_code,
        "message": message,

    }
    json_obj["response"] = response
    if status_code is None:
        return Response(json_obj, status=status.HTTP_200_OK)
    return Response(json_obj, status_code)


class addUser(APIView):
    def post(self, request):
        data = {}
        response = {}

        try:
            p = User()
            p1 = Person()
            p.first_name = request.data['firstname']
            p.last_name = request.data['lastname']
            p.username = request.data['username']
            p.email = request.data['email']
            password = request.data['password']
            p.set_password(password)
            p1.username = request.data['username']
            p1.name = request.data['name']
            p1.age = request.data['age']
            p1.gender = request.data['gender']
            p1.phone = request.data['phone']
            p1.email = request.data['email']
            p1.status = 1
            p1.photo = request.FILES['photo']
            p1.save()
            p.save()

            data = {
                "Username": p.username,
                "Email": p.email,
                "Password": p.password,
                "FirstName": p.first_name,
                "LastName": p.last_name,
                "Name": p1.username,
                "Age": p1.age,
                "gender": p1.gender,
                "phone": p1.phone,
                "email": p1.email,
                "status": p1.status,

            }

        except Exception as e:
            response['statusMessage'] = 'wrong data'
            return failure_response(response)

        response = {}
        response["isSuccess"] = True
        response['statusMessage'] = 'succesffully done'
        response['data'] = data
        return success_response(response)


class auth_login(APIView):
    def post(self, request):
        data = {}
        response = {}

        try:
            userName = request.data['username']
            password = request.data['password']

            p = authenticate(username=userName, password=password)

            if p is not None:
                p1 = Person.objects.get(username=p)

                data = {
                    "Username": p.username,
                    "First Name": p.first_name,
                    "Last Name": p.last_name,
                    "Email": p.email,
                    "Password": p.password,
                    "Name": p1.username,
                    "Age": p1.age,
                    "Gender": p1.gender,
                    "phone": p1.phone,
                    "email": p1.email,
                    "status": p1.status,
                }
            else:
                response['statusMessage'] = 'User not found'
                return failure_response(response)

        except Exception as e:
            response['statusMessage'] = 'wrong entris'
            return failure_response(response)


        response["isSuccess"] = True
        response['statusMessage'] = 'succesffully done'
        response['data'] = data
        return success_response(response)


class search_item(APIView):
    def get(self, request):
        info=[]

        name=request.data['name']

        q=Person.objects.get(name=name)

        if q is not NULL:
                    datas = {
                        "NAME": q.name,
                        "AGE": q.age,
                        "GENDER": q.gender,
                        "EMAIL": q.email,
                        "PHONE": q.phone,
                    }
                    info.append(datas)
                    response = {}
                    response['isSuccess'] = True
                    response["statusMessage"] = ''
                    response["DATA"] = info
                    return success_response(response)

        else:
            return failure_response(response)
class add_items(APIView):
    def post(self, request):
        permission_classes = (permissions.AllowAny,)

        response = {}
        try:
            user = Person()

            user.name = request.data['name']
            user.age = request.data['age']
            user.gender = request.data['gender']
            user.phone = request.data['phone']
            user.email = request.data['email']
            user.photo = request.data['photo']
            user.status = 1
            user.save()
            datas = {"NAME": user.name,
                     "AGE": user.age,
                     "GENDER": user.gender,
                     "PHONE": user.phone,
                     "EMAIL": user.email,
                     "PHOTO":user.photo.url,
                     "STATUS": "true"}
        except Exception as e:
            return failure_response(response)

        response = {}
        response['isSuccess'] = True
        response["statusMessage"] = ''
        response["DATA"] = datas
        return success_response(response)

class view_items(APIView):
    def get(self,request):
        personData = Person.objects.all()
        info = []
        if personData is not NULL:

            for user in personData:

                datas={
                            "NAME": user.name,
                            "AGE":  user.age,
                            "GENDER":  user.gender,
                            "PHONE": user.phone,
                            "EMAIL": user.email,
                }
                info.append(datas)
            response={}
            response['isSuccess'] = True
            response["statusMessage"]=''
            response["DATA"]=info
            return success_response(response)
        else:
            return failure_response(response)

class update_items(APIView):
        def post(self, request):

            permission_classes = (permissions.AllowAny,)

            datas = {}
            response = {}
            person_id = request.data['person_id']

            try:
                user = Person.objects.get(id=person_id)

                if user is not NULL:
                    user.name = request.data['name']
                    user.age = request.data['age']
                    user.gender = request.data['gender']
                    user.phone= request.data['phone']
                    user.email = request.data['email']
                    user.status = 1
                    user.save()
                    datas = {"NAME": user.name,
                             "AGE": user.age,
                             "GENDER": user.gender,
                             "PHONE": user.phone,
                             "EMAIL": user.email,
                             "STATUS": "true"}
                else:
                    response["statusMessage"] = 'user does not exist'
                    return failure_response(response)

            except Exception as e:
                response["statusMessage"] = 'user does not exist'
                return failure_response(response)

            response = {}
            response['isSuccess'] = True
            response["statusMessage"] = ''
            response["DATA"] = datas
            return success_response(response)


class delete_items(APIView):
    def post(self, request):

        permission_classes = (permissions.AllowAny,)

        datas = {}
        response = {}
        person_id = request.data['person_id']

        try:
            user = Person.objects.get(id=person_id)
            if user:
                user.delete()
            else:
                response["statusMessage"] = 'user does not exist'
                return failure_response(response)

        except Exception as e:
            response["statusMessage"] = 'user does not exist'
            return failure_response(response)

        response = {}
        response['isSuccess'] = True
        response["statusMessage"] = 'Removed'
        response["DATA"] = datas
        return success_response(response)