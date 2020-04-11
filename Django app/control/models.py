from django.db import models
from django.utils.timezone import now


# Create your models here.
class Institutions (models.Model):
    name = models.CharField(max_length=70,null=False,default='')
    commercialName = models.CharField( max_length=70,default='')
    acronimo = models.CharField(max_length=15,null=False,default='')
    rnc = models.CharField(max_length=70,default='')
    phone = models.CharField(max_length=70,default='')
    email = models.CharField(max_length=70, null=True)
    city = models.CharField( max_length=70,default='')
    direction = models.CharField( max_length=70, null=True)
    director = models.CharField( max_length=70,default='')
    status = models.BooleanField(default=1)
    createAt = models.DateTimeField(default=now, editable=False)
    updatedAt = models.DateTimeField(default=now, editable=False)
    updatedBy = models.DateTimeField(default=now, editable=False)
    
    
    def __str__(self):
        return self.acronimo



class Campus (models.Model):
    Institution = models.ForeignKey("Institutions", verbose_name=("Institutions"), on_delete=models.CASCADE)
    name = models.CharField(max_length=70,default='')
    city = models.CharField( max_length=70,default='')
    direction = models.CharField( max_length=70, null=True)
    phone = models.CharField( max_length=15,default='')
    email = models.CharField( max_length=70, null=True)
    manager = models.CharField( max_length=70,)
    status = models.BooleanField(default=1)
    createAt = models.DateTimeField(default=now, editable=False)
    updatedAt = models.DateTimeField(default=now, editable=False)
    updatedBy = models.DateTimeField(default=now, editable=False)
    
    def __str__(self):
        return self.name


class Building (models.Model):
    Campus = models.ForeignKey("Campus", verbose_name=("Campus"), on_delete=models.CASCADE)
    name = models.CharField(max_length=70,default='No Name')
    number = models.IntegerField(default=1)
    status = models.BooleanField(default=1)
    createAt = models.DateTimeField(default=now, editable=False)
    updatedAt = models.DateTimeField(default=now, editable=False)
    updatedBy = models.DateTimeField(default=now, editable=False)
    
    def __str__(self):
        return self.name


class Locks (models.Model):
    name = models.CharField(max_length=70,default='No Name')
    string = models.CharField(max_length=200,default='')
    button = models.CharField(max_length=20,default='')
    controller = models.CharField(max_length=70,default='')
    status = models.BooleanField(default=1)
    createAt = models.DateTimeField(default=now, editable=False)
    updatedAt = models.DateTimeField(default=now, editable=False)
    updatedBy = models.DateTimeField(default=now, editable=False)
    
    def __str__(self):
        return str(self.id) +' | '+ self.name 



class Rooms (models.Model):
    building = models.ForeignKey("Building", verbose_name=("Building"), on_delete=models.CASCADE)
    name = models.CharField(max_length=70,default='No Name')
    number = models.IntegerField(default=1)
    floor = models.IntegerField(default=1)
    lab = models.BooleanField(default=0)
    capacity = models.IntegerField(default=30)
    lock = models.ForeignKey("Locks", verbose_name=("Locks"), on_delete=models.CASCADE,default='')
    status = models.BooleanField(default=1)
    createAt = models.DateTimeField(default=now, editable=False)
    updatedAt = models.DateTimeField(default=now, editable=False)
    updatedBy = models.DateTimeField(default=now, editable=False)
    
    def __str__(self):
        return f'{self.number:02}'+f'{self.floor:02}' + ' - ' + self.name


class Control (models.Model):
    user = models.ForeignKey("Building", verbose_name=("Building"), on_delete=models.CASCADE)
    room = models.ForeignKey("Rooms", verbose_name=("Room"), on_delete=models.CASCADE)
    name = models.CharField(max_length=70,default='No Name')
    number = models.IntegerField(default=1)
    floor = models.IntegerField(default=1)
    lab = models.BooleanField(default=0)
    capacity = models.IntegerField(default=30)
    lock = models.ForeignKey("Locks", verbose_name=("Locks"), on_delete=models.CASCADE,default='')
    status = models.BooleanField(default=1)
    createAt = models.DateTimeField(default=now, editable=False)
    updatedAt = models.DateTimeField(default=now, editable=False)
    updatedBy = models.DateTimeField(default=now, editable=False)
    
    def __str__(self):
        return f'{self.number:02}'+f'{self.floor:02}' + ' - ' + self.name