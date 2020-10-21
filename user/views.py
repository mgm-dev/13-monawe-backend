# autopep8: off
import os
import json
import bcrypt
import re
import jwt
import my_settings

from pathlib                import Path
from django.views           import View
from user.models            import User
from django.http            import JsonResponse
from django.db              import IntegrityError

class SignUp(View):
    def post(self, request):
        data  = json.loads(request.body)
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if not (re.search(regex, data.get('userInfo').get('email'))):
            return JsonResponse({"message": "INVALID_EMAIL"}, status=400)

        try:
            if User.objects.filter(account=data.get('userInfo').get('account')).exists():
                return JsonResponse({"message": "USER_ID_TAKEN"}, status=400)

            password       = data.get('userInfo').get('password').encode('utf-8')
            password_crypt = bcrypt.hashpw(password, bcrypt.gensalt())
            password_crypt = password_crypt.decode('utf-8')

            User(
                account         = data.get('userInfo').get('account'),
                password        = password_crypt,
                name            = data.get('userInfo').get('name'),
                email           = data.get('userInfo').get('email'),
                phone_number    = data.get('userInfo').get('phoneNumber'),
                date_of_birth   = data.get('userInfo').get('dateOfBirth'),
                sms_agreement   = data.get('userInfo').get('smsAgreement'),
                email_agreement = data.get('userInfo').get('smsAgreement'),
            ).save()

            return JsonResponse({"message": "SIGNUP_SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except IntegrityError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

class SignIn(View) :
    def post(self, request):
        data = json.loads(request.body)

        try:
            if not User.objects.filter(account=data.get('userInfo').get('account')).exists():
                return JsonResponse({"message": "INVALID_USER_ID"}, status=401)
            else :
                user = User.objects.get(account=data.get('userInfo').get('account'))

            if bcrypt.checkpw(data.get('userInfo').get('password').encode('UTF-8'), user.password.encode('UTF-8')):
                key       = my_settings.SECRET.get('JWT_KEY')
                algorithm = my_settings.SECRET.get('JWT_ALGORITHM')
                token     = jwt.encode({'user' : user.id},key, algorithm = algorithm).decode('UTF-8')
                return JsonResponse({"token": token}, status=200)
            else :
                return JsonResponse({"message": "INVALID_USER"}, status=401)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except IntegrityError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

