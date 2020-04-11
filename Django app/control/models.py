from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

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
    
    def __str__(self):
        return self.name


class Building (models.Model):
    Campus = models.ForeignKey("Campus", verbose_name=("Campus"), on_delete=models.CASCADE)
    name = models.CharField(max_length=70,default='No Name')
    number = models.IntegerField(default=1)
    status = models.BooleanField(default=1)
    createAt = models.DateTimeField(default=now, editable=False)
    updatedAt = models.DateTimeField(default=now, editable=False)
    
    def __str__(self):
        return str(self.number) +' | '+ self.name


class Locks (models.Model):
    name = models.CharField(max_length=70,default='No Name')
    idstring = models.CharField(max_length=9,default='')
    controller = models.CharField(max_length=70,default='')
    status = models.BooleanField(default=1)
    createAt = models.DateTimeField(default=now, editable=False)
    updatedAt = models.DateTimeField(default=now, editable=False)
    
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
    available = models.BooleanField(default=1)
    status = models.BooleanField(default=1)
    createAt = models.DateTimeField(default=now, editable=False)
    updatedAt = models.DateTimeField(default=now, editable=False)
    
    def __str__(self):
        return f'{self.number:02}'+f'{self.floor:02}' + ' - ' + self.name

class Carrier(models.Model):
    institution = models.ForeignKey("Institutions", verbose_name=("Institutions"), on_delete=models.CASCADE)
    name = models.CharField(max_length=70,null=False,default=' ')
    
    def __str__(self):
        return self.name

class Account(models.Model):
    accountTypes = [
    ('ES', 'Estudiante'),
    ('PR', 'Profesor'),
    ('ST', 'Staf'),
]
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    type = models.CharField(max_length=2,choices=accountTypes,default='ES')

    def __str__(self):
        return str(self.user) +' | '+ self.user.first_name+' '+self.user.last_name


class Subject (models.Model):
    career = models.ForeignKey("Carrier", verbose_name=("Carrier"), on_delete=models.CASCADE)
    quater = models.IntegerField(default=0)
    name = models.CharField(max_length=70,default='')
    code = models.CharField(max_length=10,default='')
    credits = models.IntegerField()
    prerequirements = models.CharField(max_length=70,null=True)

    def __str__(self):
        return str(self.id) +' | '+ self.name 

class Control (models.Model):
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    room = models.ForeignKey("Rooms", verbose_name=("Room"), on_delete=models.CASCADE)
    status = models.BooleanField(default=1)
     
    
    def __str__(self):
        return f'{self.number:02}'+f'{self.floor:02}' + ' - ' + self.name



class SubjectSchedule (models.Model):
    WEEKDAYS = [
  (1, ("Lunes")),
  (2, ("Martes")),
  (3, ("Miercoles")),
  (4, ("Jueves")),
  (5, ("Viernes")),
  (6, ("Sabado")),
  (7, ("Domingo")),
]
    subject = models.ForeignKey("Subject", verbose_name=("Subject"), on_delete=models.CASCADE)
    status = models.BooleanField(default=1)
    weekday = models.IntegerField(choices=WEEKDAYS)
    fromHour = models.TimeField()
    toHour = models.TimeField() 
     
    
    def __str__(self):
        return str(self.subject)

    class Meta:
        ordering = ('weekday', 'fromHour')
        unique_together = ('weekday', 'fromHour', 'toHour')

    def __unicode__(self):
        return u'%s: %s - %s' % (self.get_weekday_display(),
                                 self.fromHour, self.toHour)


class Permission (models.Model):
    WEEKDAYS = [
  (1, ("Lunes")),
  (2, ("Martes")),
  (3, ("Miercoles")),
  (4, ("Jueves")),
  (5, ("Viernes")),
  (6, ("Sabado")),
  (7, ("Domingo")),
]
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    room = models.ForeignKey("Rooms", verbose_name=("Room"), on_delete=models.CASCADE)
    status = models.BooleanField(default=1)
    weekday = models.IntegerField(choices=WEEKDAYS)
    fromHour = models.TimeField()
    toHour = models.TimeField() 
     
    
    def __str__(self):
        return str(self.user)+' | '+self.room

    class Meta:
        ordering = ('weekday', 'fromHour')
        unique_together = ('weekday', 'fromHour', 'toHour')

    def __unicode__(self):
        return u'%s: %s - %s' % (self.get_weekday_display(),
                                 self.fromHour, self.toHour)


class UserSubject (models.Model):
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    subject = models.ForeignKey(Subject, verbose_name=("Subject"), on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)+' | '+ str(self.subject)