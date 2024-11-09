from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User
from api_app.models import Person
from django.contrib.auth import authenticate
from rest_framework.test import APITestCase
from django.urls import reverse



def success_response(response, status_code=None):
    json_obj = {
        "hasError": False,
        "errorCode": -1,
        "message": "Success",
    }
    json_obj["response"] = response
    return Response(json_obj, status=status_code or status.HTTP_200_OK)


def failure_response(response, status_code=None, error_code=1001, message="Failure"):
    json_obj = {
        "hasError": True,
        "errorCode": error_code,
        "message": message,
    }
    json_obj["response"] = response
    return Response(json_obj, status=status_code or status.HTTP_400_BAD_REQUEST)


class AddUser(APIView):
    def post(self, request):
        data = {}
        response = {}

        try:
            # Validate input data
            required_fields = ['firstname', 'lastname', 'username', 'email', 'password', 'name', 'age', 'gender', 'phone', 'photo']
            for field in required_fields:
                if field not in request.data:
                    return failure_response({"field": field}, message=f"Missing {field}")

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
            p1.status = 1  # Assuming '1' means active or valid status
            p1.photo = request.FILES.get('photo')  # Safely handle file input

            if not p1.photo:
                return failure_response({"photo": "Photo is required"}, message="No photo uploaded")

            p1.save()
            p.save()

            data = {
                "Username": p.username,
                "Email": p.email,
                "FirstName": p.first_name,
                "LastName": p.last_name,
                "Name": p1.username,
                "Age": p1.age,
                "Gender": p1.gender,
                "Phone": p1.phone,
                "Email": p1.email,
                "Status": p1.status,
            }

        except Exception as e:
            response['statusMessage'] = f"Error occurred: {str(e)}"
            return failure_response(response, message="Error while creating user")

        response = {
            "isSuccess": True,
            "statusMessage": 'User created successfully',
            "data": data
        }
        return success_response(response)
    

def success_response(response, status_code=None):
    json_obj = {
        "hasError": False,
        "errorCode": -1,
        "message": "Success",
    }
    json_obj["response"] = response
    return Response(json_obj, status=status_code or status.HTTP_200_OK)

def failure_response(response, status_code=None, error_code=1001, message="Failure"):
    json_obj = {
        "hasError": True,
        "errorCode": error_code,
        "message": message,
    }
    json_obj["response"] = response
    return Response(json_obj, status=status_code or status.HTTP_400_BAD_REQUEST)


class AuthLogin(APIView):
    def post(self, request):
        data = {}
        response = {}

        try:
            # Get username and password from request
            userName = request.data['username']
            password = request.data['password']

            # Authenticate the user
            user = authenticate(username=userName, password=password)

            if user is not None:
                # Attempt to retrieve the corresponding Person object
                try:
                    person = Person.objects.get(username=user)

                    # Prepare data for successful login response
                    data = {
                        "Username": user.username,
                        "First Name": user.first_name,
                        "Last Name": user.last_name,
                        "Email": user.email,
                        "Name": person.username,
                        "Age": person.age,
                        "Gender": person.gender,
                        "Phone": person.phone,
                        "Email": person.email,
                        "Status": person.status,
                    }

                except Person.DoesNotExist:
                    response['statusMessage'] = 'Person record not found'
                    return failure_response(response, status_code=status.HTTP_404_NOT_FOUND)

            else:
                response['statusMessage'] = 'Invalid username or password'
                return failure_response(response, status_code=status.HTTP_401_UNAUTHORIZED)

        except KeyError as e:
            response['statusMessage'] = f'Missing required field: {str(e)}'
            return failure_response(response, status_code=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            response['statusMessage'] = f'Error occurred: {str(e)}'
            return failure_response(response)

        # Success response
        response["isSuccess"] = True
        response['statusMessage'] = 'Login successful'
        response['data'] = data
        return success_response(response)
    
