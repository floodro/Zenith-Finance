from django.db import models

# Create your models here.
class Director(models.Model):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    
    def get_name(self):
        return self.name
    
class Administrator(models.Model):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    
    def get_name(self):
        return self.name

class Performer(models.Model):
    name = models.CharField(max_length=200)
    sr_code = models.CharField(max_length=200)
    program = models.CharField(max_length=200)
    campus = models.CharField(max_length=200)
    org = models.CharField(max_length=200)

    def get_name(self):
        return self.name    
    
