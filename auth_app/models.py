from django.db import models

# Create your models here.


class MyUser(models.Model):
    first_name = models.CharField(max_length = 200)
    last_name = models.CharField(max_length = 200)
    email = models.CharField(max_length = 200)
    password = models.CharField(max_length = 200)
    salt = models.CharField(max_length = 200, null=True)
    last_login = models.DateTimeField(null=True)
    is_authenticated = models.BooleanField(default=True)

    def __repr__(self):
        return "{fn} {ln}, {em}".format(fn=self.first_name, ln=self.last_name, em=self.email)

class TwoFactorAuth(models.Model):
    is_enabled = models.BooleanField(default=False)
    token = models.CharField(max_length=400)
    username = models.ForeignKey(MyUser, on_delete=models.CASCADE)
