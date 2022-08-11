from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout

import auth_app.myauth as myauth

# Create your views here.


def index(request):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))

def homepage(request):
    if request.user.is_authenticated:
        template = loader.get_template('homepage.html')
        context = {"user" : request.user}
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template('index.html')
        context = {}
        return HttpResponse(template.render(context, request))

def logout_user(request):
    try:
        logout(request)
    except:
        raise

    return HttpResponse("/auth/", status=200)



@csrf_exempt
def check_tfa(request):
    if request.user.is_authenticated: 
        return myauth.check_tfa(request)
    else:
        return HttpResponse("{'error':'User failed authentication'}", status=403)

def delete_tfa(request):
    if request.user.is_authenticated:
        myauth.drop_tfa(request.user)
        return HttpResponse("{'success':'OK'}", status=200)
    else:
        return HttpResponse("{'error':'User is not authenticated'}", status_code=403)
def setup_tfa(request):
    if request.user.is_authenticated:
        myauth.setup_TFA_secret(request.user)
        return HttpResponse("{'success':'OK'}", status=200)
    else:
        return HttpResponse("{'error':'User is not authenticated'}", status_code=403)

def get_qr_code(request):
    if request.user.is_authenticated:
        b64 = myauth.generate_user_qrcode(request.user)
        return HttpResponse(b64, status=200)
    else:
        return HttpResponse("{'error':'User is not authenticated'}", status=403)

def create_users(request):
    return myauth.create_users(request)

def fetch_all_users(request):
    return myauth.fetch_all_users(request)

@csrf_exempt
def fetch_user(request):
    #return myauth.fetch_user(request)
    return myauth.my_auth(request)

