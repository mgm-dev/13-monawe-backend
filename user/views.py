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
            if not (re.search(regex, data.get('email'))):
                return JsonResponse({"message": "INVALID_EMAIL"}, status=400)

            if User.objects.filter(account=data.get('account')).exists():
                return JsonResponse({"message": "USER_ID_TAKEN"}, status=400)

            password       = data.get('password').encode('utf-8')
            password_crypt = bcrypt.hashpw(password, bcrypt.gensalt())
            password_crypt = password_crypt.decode('utf-8')

            date_string = data.get('dateOfBirth')
            date = datetime.strptime(date_string, '%Y%m%d').strftime('%Y-%m-%d')

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

        except IntegrityError:
            return JsonResponse({"message": "INTEGRITY_ERROR"}, status=400)

        except ValueError:
            return JsonResponse({"message": "VALUE_ERROR"}, status=400)

class SignIn(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = User.objects.filter(account=data.get('account'))

            if not user.exists():
                return JsonResponse({"message": "INVALID_USER"}, status=409)

            if bcrypt.checkpw(data.get('password').encode('UTF-8'), user[0].password.encode('UTF-8')):
                key       = my_settings.SECRET.get('JWT_KEY')
                algorithm = my_settings.SECRET.get('JWT_ALGORITHM')
                token     = jwt.encode({'user' : user[0].id},key, algorithm = algorithm).decode('UTF-8')
                return JsonResponse({"token": token, "message": "SIGNIN_SUCCESS", "name" : user[0].name}, status=200)
            else :
                return JsonResponse({"message": "INVALID_USER"}, status=401)

        except IntegrityError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except ValueError:
            return JsonResponse({"message": "VALUE_ERROR"}, status=400)

class CheckEmail(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if User.objects.filter(email=data.get('email')).exists():
                return JsonResponse({"message" : "USER_EMAIL_TAKEN"}, status=400)
            else :
                return JsonResponse({"message" : "USER_EMAIL_OK"}, status=200)

        except IntegrityError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except ValueError:
            return JsonResponse({"message": "VALUE_ERROR"}, status=400)

class CheckAccount(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if User.objects.filter(account=data.get('account')).exists():
                return JsonResponse({"message" : "USER_ID_TAKEN"}, status=400)
            else :
                return JsonResponse({"message" : "USER_ID_OK"}, status=200)

        except IntegrityError:
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
                "id" : user_id,
                "name" : user_info.name,
                "account" : user_info.account,
                "email" : user_info.email,
                "phone_number" : user_info.phone_number,
                "date_of_birth" : user_info.date_of_birth
            }
            return JsonResponse({"data" : data}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message': 'USER_DOES_NOT_EXIST'}, status=404)


class AddAddress(View):
    @utils.signin_decorator
    def post(self, request):
        data = json.loads(request.body)        
        user_id = request.user.id
        # user_id = User.objects.get(id = data['user_id'])
        address = data['address']
        detailed_address = data['detailed_address']
        zip_code = data['zip_code']
        existing_default = Address.objects.get(user = user_id, is_default = 1)

        if Address.objects.filter(user = user_id, address = address, detailed_address = detailed_address).exists():
            return JsonResponse({"MESSAGE" : "Given address already exists"}, status = 404)
        
        else:
            if (Address.objects.filter(user = user_id, is_default = 1).exists()) and data['is_default'] == 1:
                existing_default.is_default = 0
                existing_default.save()
                Address(
                    user                = user_id,
                    address             = address,
                    detailed_address    = detailed_address,
                    zip_code            = zip_code,
                    is_default          = 1
                ).save()
                return JsonResponse({"MESSAGE":"ADDRESS ADDED AND CHANGE THE DEFAULT ADDRESS"}, status=201)
            else:
                Address(
                    user                = user_id,
                    address             = address,
                    detailed_address    = detailed_address,
                    zip_code            = zip_code,
                    is_default          = data['is_default']
                ).save()
                return JsonResponse({"MESSAGE": "ADDRESS ADDED"}, status=201)

    @utils.signin_decorator
    def get(self, request):

        user_id = request.user.id   
        addresses = Address.objects.filter(user = user_id).values()
        addresses_list = [address for address in addresses]

        return JsonResponse({"Addresses": addresses_list}, status =200)

    @utils.signin_decorator
    def patch(self, request):
        user_id = request.user.id
        Address(
            user                = user_id,
            address             = address,
            detailed_address    = detailed_address,
            zip_code            = zip_code,
            is_default          = data['is_default']
        ).save()
        return JsonResponse({"MESSAGE": "ADDRESS CHANGED"}, status = 200)

    # @utils.signin_decorator
    def delete(self, request):
        # user_id = request.user.id
        data = json.loads(request.body)
        user_id = data['user_id']
        target = Address.objects.get(id = data['address_id'])
        
        target.delete()

        return JsonResponse({"MESSAGE": "ADDRESS DELETED"}, status = 200)
    

