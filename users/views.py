import json
from django.views import View
from django.http import JsonResponse
from .models import Users

class SignUpView(View):
    #회원가입 폼에서 중복 방지 구현하기!
    def post(self, request):
        data = json.loads(request.body)
        if Users.objects.filter(username = data['username']).exists():
            return JsonResponse({'message': f'Username {data["username"]} already exists. Choose another one.'}, status=200)
        elif Users.objects.filter(username = data['email']).exists():
            return JsonResponse({'message': f'Account with email {data["email"]} already exists!'}, status=200)

        Users(
            username = data['username'],
            password = data['password'],
            email = data['email']
        ).save()

        return JsonResponse({'message': 'Registration Complete!'}, status=200)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)

        if Users.objects.filter(username = data['username']).exists():
            user = Users.objects.get(username = data['username'])
            if user.password == data['password']:
                return JsonResponse({'message': f'Successfully logged in. Welcome Back, {user.username}!'}, status=200)
            else:
                return JsonResponse({'message': f'Incorrect Password'}, status=200)
            
            return JsonResponse({'message': f'There was no account found with the given username.'}, status=200)

