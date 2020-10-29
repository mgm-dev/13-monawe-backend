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
from user.models            import User, Address
from django.http            import JsonResponse
from django.db              import IntegrityError

class SignUp(View):
    def post(self, request):
        try:
            data  = json.loads(request.body)
            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
            if not (re.search(regex, data['email'])):
                return JsonResponse({"message": "INVALID_EMAIL"}, status=400)

            if User.objects.filter(account=data['account']).exists():
                return JsonResponse({"message": "USER_ID_TAKEN"}, status=400)

            password       = data['password'].encode('utf-8')
            password_crypt = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

            date_string = data['date_of_birth']
            date = datetime.strptime(date_string, '%Y%m%d').strftime('%Y-%m-%d')

            User(
                account         = data['account'],
                password        = password_crypt,
                name            = data['name'],
                email           = data['email'],
                phone_number    = data['phone_number'],
                date_of_birth   = date,
                sms_agreement   = data['sms_agreement'],
                email_agreement = data['email_agreement'],
            ).save()

            return JsonResponse({"message": "SIGNUP_SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except ValueError:
            return JsonResponse({"message": "VALUE_ERROR"}, status=400)

class SignIn(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = User.objects.get(account=data['account'])

            if bcrypt.checkpw(data['password'].encode('UTF-8'), user.password.encode('UTF-8')):
                key       = my_settings.SECRET.get('JWT_KEY')
                algorithm = my_settings.SECRET.get('JWT_ALGORITHM')
                token     = jwt.encode({'user' : user.id},key, algorithm = algorithm).decode('UTF-8')
                return JsonResponse({"token": token, "message": "SIGNIN_SUCCESS", "name" : user.name}, status=200)

            return JsonResponse({"message": "INVALID_USER"}, status=401)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except ValueError:
            return JsonResponse({"message": "VALUE_ERROR"}, status=400)

        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status=401)

class CheckEmail(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({"message" : "USER_EMAIL_TAKEN"}, status=400)
            return JsonResponse({"message" : "USER_EMAIL_OK"}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except ValueError:
            return JsonResponse({"message": "VALUE_ERROR"}, status=400)

class CheckAccount(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if User.objects.filter(account=data['account']).exists():
                return JsonResponse({"message" : "USER_ID_TAKEN"}, status=400)
            return JsonResponse({"message" : "USER_ID_OK"}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except ValueError:
            return JsonResponse({"message": "VALUE_ERROR"}, status=400)

class UserInfo(View):
    @utils.signin_decorator
    def get(self, request):
        try:
            user_id = request.user.id
            user_info = User.objects.get(id=user_id)
            data = {
                "id"           : user_id,
                "name"         : user_info.name,
                "account"      : user_info.account,
                "email"        : user_info.email,
                "phone_number" : user_info.phone_number,
                "date_of_birth": user_info.date_of_birth
            }
            return JsonResponse({"data" : data}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'message': 'USER_DOES_NOT_EXIST'}, status=404)


class AddressView(View):
    @utils.signin_decorator
    def post(self, request):
        try:
            user_id = request.user.id
            data  = json.loads(request.body)

            if data['is_default']:
                Address.objects.filter(user_id=user_id).update(is_default=0)

            Address(
                name = data['name'],
                phone_number = data['phone_number'],
                user_id = user_id,
                address = data['address'],
                detailed_address = data['detailed_address'],
                zip_code = data['zip_code'],
                is_default = data['is_default']
            ).save()
            return JsonResponse({"message": "ADDRESS_CREATED"}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except ValueError:
            return JsonResponse({"message": "VALUE_ERROR"}, status=400)

    @utils.signin_decorator
    def get(self, request):
        try:
            user_id = request.user.id
            data = [address for address in Address.objects.filter(user_id=user_id).order_by('-is_default').values()]
            return JsonResponse({"data" : data}, status=200)
        except Address.DoesNotExist:
            return JsonResponse({'message': 'ADDRESS_DOES_NOT_EXIST'}, status=404)

    @utils.signin_decorator
    def patch(self, request):
        try:
            user_id = request.user.id
            data = json.loads(request.body)
            target_address = Address.objects.get(id=data['address_id'])

            if not target_address:
                return JsonResponse({'message': 'ADDRESS_DOES_NOT_EXIST'}, status=404)

            if not target_address.user_id == user_id:
                return JsonResponse({'message': 'NO_PERMISSION'}, status=403)

            if data['is_default']:
                Address.objects.filter(user_id=user_id).update(is_default=0)

            if data['name']: target_address.name                         = data['name']
            if data['address']: target_address.address                   = data['address']
            if data['detailed_address']: target_address.detailed_address = data['detailed_address']
            if data['zip_code']: target_address.zip_code                 = data['zip_code']
            if "is_default" in data: target_address.is_default           = data['is_default']

            target_address.save()

            return JsonResponse({'message': 'ADDRESS_UPDATED'}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except Address.DoesNotExist:
            return JsonResponse({'message': 'ADDRESS_DOES_NOT_EXIST'}, status=404)

    @utils.signin_decorator
    def delete(self, request):
        try:
            user_id = request.user.id
            data = json.loads(request.body)
            target_address = Address.objects.get(id=data['address_id'])

            if not target_address:
                return JsonResponse({'message': 'ADDRESS_DOES_NOT_EXIST'}, status=404)

            if not target_address.user_id == user_id:
                return JsonResponse({'message': 'NO_PERMISSION'}, status=403)

            target_address.delete()
            return JsonResponse({'message': 'ADDRESS_DELETED'}, status=202)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except Address.DoesNotExist:
            return JsonResponse({'message': 'ADDRESS_DOES_NOT_EXIST'}, status=404)
