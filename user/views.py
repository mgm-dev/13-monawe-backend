# autopep8: off
import os
import json
import bcrypt
import re
import jwt
import my_settings
import utils

from datetime               import datetime
from django.views           import View
from user.models            import User
from django.http            import JsonResponse
from django.db              import IntegrityError
from django.core.exceptions import ValidationError

class SignUp(View):
    def post(self, request):
        data  = json.loads(request.body)
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if not (re.search(regex, data.get('email'))):
            return JsonResponse({"message": "INVALID_EMAIL"}, status=400)

        try:
            if User.objects.filter(account=data.get('account')).exists():
                return JsonResponse({"message": "USER_ID_TAKEN"}, status=400)

            password       = data.get('password').encode('utf-8')
            password_crypt = bcrypt.hashpw(password, bcrypt.gensalt())
            password_crypt = password_crypt.decode('utf-8')

            dateString = data.get('dateOfBirth')
            date = datetime.strptime(dateString, '%Y%m%d').strftime('%Y-%m-%d')

            User(
                account         = data.get('account'),
                password        = password_crypt,
                name            = data.get('name'),
                email           = data.get('email'),
                phone_number    = data.get('phoneNumber'),
                date_of_birth   = date,
                sms_agreement   = data.get('smsAgreement'),
                email_agreement = data.get('smsAgreement'),
            ).save()

            return JsonResponse({"message": "SIGNUP_SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except IntegrityError:
            return JsonResponse({"message": "INTEGRITY_ERROR"}, status=400)

        except ValidationError:
            return JsonResponse({"message": "VALUE_ERROR"}, status=400)

class SignIn(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if not User.objects.filter(account=data.get('account')).exists():
                return JsonResponse({"message": "INVALID_USER_ID"}, status=401)
            else :
                user = User.objects.get(account=data.get('account'))

            if bcrypt.checkpw(data.get('password').encode('UTF-8'), user.password.encode('UTF-8')):
                key       = my_settings.SECRET.get('JWT_KEY')
                algorithm = my_settings.SECRET.get('JWT_ALGORITHM')
                token     = jwt.encode({'user' : user.id},key, algorithm = algorithm).decode('UTF-8')
                return JsonResponse({"token": token, "message": "SIGNIN_SUCCESS"}, status=200)
            else :
                return JsonResponse({"message": "INVALID_USER"}, status=401)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except IntegrityError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except ValidationError:
            return JsonResponse({"message": "VALUE_ERROR"}, status=400)

class CheckEmail(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            duplicate = User.objects.filter(email=data.get('email')).exists()
            if duplicate:
                return JsonResponse({"message" : "USER_EMAIL_TAKEN"}, status=400)
            else :
                return JsonResponse({"message" : "USER_EMAIL_OK"}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except IntegrityError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except ValidationError:
            return JsonResponse({"message": "VALUE_ERROR"}, status=400)

class CheckAccount(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            duplicate = User.objects.filter(account=data.get('account')).exists()
            if duplicate:
                return JsonResponse({"message" : "USER_ID_TAKEN"}, status=400)
            else :
                return JsonResponse({"message" : "USER_ID_OK"}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except IntegrityError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except ValidationError:
            return JsonResponse({"message": "VALUE_ERROR"}, status=400)

class UserInfo(View):
    @utils.signin_decorator
    def get(self, request):
        user_id = request.user.id
        user_info = User.objects.get(id=user_id)
        data = {
            "id" : user_id,
            "name" : user_info.name,
            "account" : user_info.account,
            "email" : user_info.email,
            "phone_number" : user_info.phone_number,
            "date_of_birth" : user_info.date_of_birth
        }

        return JsonResponse({"data" : data}, status=400)
