from django.shortcuts import HttpResponse
from ..models import User
import uuid
import json
from django.http import JsonResponse
from decimal import Decimal
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

class UserController:
    @staticmethod
    def createUser(request):
        if request.method == 'POST':
            try:
                body_unicode = request.body.decode('utf-8')
                body_data = json.loads(body_unicode)
                
                email_exists = User.objects.filter(email=body_data.get('email')).exists()
                username_exists = User.objects.filter(username=body_data.get('username')).exists()
                phone_exists = User.objects.filter(phone=body_data.get('phone')).exists()
                
                if email_exists:
                    return HttpResponse('email already exists, login instead?', status=400)
                if username_exists:
                    return HttpResponse('Username already exists login instead?', status=400)
                if phone_exists:
                    return HttpResponse('Phone already exists, login instead?', status=400)

                user_data = {
                    'userId': uuid.uuid4(),
                    'first_name': body_data.get('first_name'),
                    'last_name': body_data.get('last_name'),
                    'acc_balance':0,
                    'phone': body_data.get('phone'),
                    'username': body_data.get('username'),
                    'role': body_data.get('role'),
                    'email': body_data.get('email'),
                    'password': body_data.get('password')
                }
                new_user = User.objects.create(**user_data)

                subject = 'Welcome to Agromart!'
                message = f'Hello {new_user.username} Welcome to agromart!'
                sender = settings.EMAIL_HOST_USER
                recipient = [new_user.email]
                send_mail(subject,message, sender,recipient)

                return HttpResponse('Success', status=200)
            except Exception as e:
                print('error', e)
                return HttpResponse(f'Error: {e}', status=500)
        else:
            return HttpResponse('Method Not Allowed', status=405)

    @staticmethod
    def loginUser(request):
        if request.method == 'POST':
            try:
                body_unicode = request.body.decode('utf-8')
                body_data = json.loads(body_unicode)

                email = body_data.get('email')
                password = body_data.get('password')
                user_data = User.objects.get(email=email)
                if user_data.password != password:
                    return HttpResponse('Wrong password', status=403)
                
                if user_data.role == 'buyer':
                    return JsonResponse({'userId': user_data.userId, 'url': '/products/'}, status=200)
                elif user_data.role == 'admin':
                    return JsonResponse({'userId': user_data.userId, 'url': '/admindash/'}, status=200)
                elif user_data.role == 'seller':
                    return JsonResponse({'userId': user_data.userId, 'url': '/sellerdash/'}, status=200)
                
            except User.DoesNotExist:
                return HttpResponse('No such user exists', status=404)
            except Exception as e:
                return HttpResponse(f'Error: {e}', status=500)
        else:
            return HttpResponse('Method Not Allowed', status=405)

    from django.core import serializers

    @staticmethod
    def getUser(request):
        if request.method == 'POST':
            try:
                body_unicode = request.body.decode('utf-8')
                body_data = json.loads(body_unicode)
                userID = body_data.get('userId')
                user_data = User.objects.get(userId=userID)
                user = {
                    'userId':user_data.userId,
                    'first_name':user_data.first_name,
                    'last_name':user_data.last_name,
                    'acc_balance':user_data.acc_balance,
                    'phone':user_data.phone,
                    'email':user_data.email,
                    'username':user_data.username
                }
                return JsonResponse({'user':user},status=200)
            except User.DoesNotExist:
                return HttpResponse('No such user found', status=404)
            except Exception as e:
                return HttpResponse(f'Error: {e}', status=500)
        else:
            return HttpResponse('Method Not Allowed', status=405)
  
    @staticmethod
    def getAllUsers(request):
        if request.method == 'GET':
            try:
                users = User.objects.all()
                users_list = [{'userId': user.userId,
                               'role': user.role,
                               'first_name': user.first_name,
                               'last_name': user.last_name,
                               'phone': user.phone,
                               'email': user.email,
                               'username': user.username,
                               'password': user.password} for user in users]
                return JsonResponse({'users': users_list})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)
        
    @staticmethod
    def loadCash(request):
        if request.method == 'POST':
            try:
                body_unicode = request.body.decode('utf-8')
                body_data = json.loads(body_unicode)
                user = User.objects.get(userId=body_data.get('userId'))
                amount = Decimal(body_data.get('amount'))
                user.acc_balance += amount
                user.save()
                return JsonResponse({'message': f'Added {amount} to account balance'}, status=200)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    @staticmethod
    def spendCash(request):
        if request.method == 'POST':
            try:
                body_unicode = request.body.decode('utf-8')
                body_data = json.loads(body_unicode)
                user = User.objects.get(userId=body_data.get('userId'))
                amount = Decimal(body_data.get('amount'))
                userBalance = Decimal(user.acc_balance)
                if userBalance < amount:
                    return JsonResponse({'error': 'Insufficient funds'}, status=400)
                user.acc_balance -= amount
                user.save()
                return JsonResponse({'message': f'Withdrawn {amount} from account balance'}, status=200)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)
        
    @staticmethod
    def deleteUser(request):
        if request.method == 'POST':
            try:
                body_unicode = request.body.decode('utf-8')
                body_data = json.loads(body_unicode)
                user_id = body_data.get('userId')
                user = User.objects.get(userId=user_id)
                user.delete()
                return JsonResponse({'message': 'User deleted successfully'}, status=200)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)