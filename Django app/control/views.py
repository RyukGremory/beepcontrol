from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from .models import Locks,Institutions,Campus,Building,Rooms,Account,Control,Permission,Carrier,Subject,SubjectSchedule,Permission,UserSubject
import requests
from django.contrib.auth.models import User
from .forms import ControlForm


def lockAccion (lock,accion):
    print('****************')
    print(lock,accion)
    print('****************')
    URL = 'http://192.168.1.15'
    params = {lock:accion}
    requests.get(url = URL,params=params)


def beginClass (user,room,lock,accion):
    permiso = Permission.objects.filter(user=user).filter(room=room)
    if permiso.count() >= 1:
        userI = User.objects.get(id=user)
        roomI = Rooms.objects.get(id=room)
        entry = Control(user=userI,room=roomI,status=1,accion=accion)
        #entry.save()
        lockAccion(lock,accion)
    else:
        print('****************')
        print('No tiene Permiso')
        print('****************')


def EndClass ():
    pass


def index(request):
    return render(request, "index.html")

def locksView(request):
    i = Locks.objects.all()
    context = {'locks':i}
    
    for i in request.GET:
        accion(i)
    return render(request, "pages/locks.html",context)

def controlView(request):
    form = ControlForm()
    entries = Rooms.objects.all()
    users = User.objects.all()
    context = {'form':form,'elements': entries,'usuarios':users}
    
    if request.method == 'POST':
        user = ''
        room = ''
        accion = ''
        form = ControlForm(request.POST)
        if form.is_valid():
            user = request.POST.get('user')
            room = request.POST.get('room')
            accion = request.POST.get('accion')
            lock = Rooms.objects.filter(id=room,status=1)[0].lock.idstring
            beginClass(user,room,lock,accion)

    return render(request, "pages/control.html",context)

def registroView(request):
    data = Control.objects.filter(status=1)
    context = {'data':data}
    
    return render(request, "pages/registro.html",context)


#@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        template = loader.get_template('pages/' + load_template)
        return HttpResponse(template.render(context, request))

    except:

        template = loader.get_template( 'pages/error-404.html' )
        return HttpResponse(template.render(context, request))