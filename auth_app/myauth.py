
import json
import bcrypt
import qrcode
import PIL
import base64
import pyotp
from io import BytesIO
from .models import MyUser, TwoFactorAuth
from django.http import HttpResponse
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import authenticate, login
from django.conf import settings



def drop_TFA(user: MyUser):
    TwoFactorAuth.objects.filter(username=user).delete()

def setup_TFA_secret(user: MyUser):
    TwoFactorAuth.objects.filter(username=user).delete()
    secret = pyotp.random_base32()
    nfa = TwoFactorAuth.objects.create(is_enabled=True, token=secret, username=user)
    nfa.save()
    


def my_auth(request):
    print(request.body)
    my_data = json.loads(request.body)
    email = my_data.get('email', '')
    password = my_data.get('password', '')
    totp = my_data.get('totp', '')
    my_user = authenticate(request = request, email=email, password=password)
    my_user.backend = settings.AUTHENTICATION_BACKENDS[1]
    if my_user is not None:
        try:
            tfa = TwoFactorAuth.objects.get(username=my_user)
            if totp is '':
                return HttpResponse("Error: second factor is enabled", status=401)
            else:
                valid_totp = pyotp.totp.TOTP(tfa.token)
                if(valid_totp.verify(totp)):
                    login(request, my_user)
                    return HttpResponse("/auth/homepage", status=200)
                else:
                    return HttpResponse("Failed", status=403)
        except TwoFactorAuth.DoesNotExist:
            login(request, my_user)
            return HttpResponse("/auth/homepage", status=200)
    else:
        return HttpResponse("Failed", status=403)


def generate_user_qrcode(user: MyUser):
    try:
        tfa = TwoFactorAuth.objects.get(username=user)
    except TwoFactorAuth.DoesNotExist:
        return ""
    qr_url = pyotp.totp.TOTP(tfa.token).provisioning_uri(name=user.email, issuer_name="My Auth App")
    img = qrcode.make(qr_url)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode("UTF-8")

    return img_str




def fetch_all_users(request):
    data= []
    for e in MyUser.objects.all():
        data.append(repr(e))
        jdata = json.dumps(data)
        return HttpResponse(jdata, status=200)

def fetch_user(request):
    try:
        my_data = json.loads(request.body)
        tentative_user = MyUser.objects.filter(email=my_data['email'])[0]
        if(bcrypt.checkpw(my_data['password'].encode('UTF-8'), tentative_user.password.encode('UTF-8'))):
            return HttpResponse("OK", status=200)

    except AssertionError:
        return HttpResponse("Unauthorized", status=401)


def create_users(request):
    if not MyUser.objects.filter(email="alain.delon@tf1.fr"):
        salt = bcrypt.gensalt()
        u1pw = bcrypt.hashpw(b"test", salt).decode('UTF-8')
        dbsalt = salt.decode('UTF-8')
        u1 = MyUser.objects.create(first_name="Alain", last_name="Delon", email="alain.delon@tf1.fr", password=u1pw, salt=dbsalt)
    return HttpResponse("OK", status=200)

class MyAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, otp=None):
        tentative_user = MyUser.objects.get(email=email)
        if tentative_user is not None:
            if(bcrypt.checkpw(password.encode('UTF-8'), tentative_user.password.encode('UTF-8'))):
                return tentative_user
        return None


    def get_user(self, user_id):
        try:
            return MyUser.objects.get(id=user_id)
        except MyUser.DoesNotExist:
            return None
