from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from .models import Locks,Institutions,Campus,Building,Rooms,Account,Control,Permission,Carrier,Subject,SubjectSchedule,Permission,UserSubject
import requests

def accion (sentencia):
    URL = 'http://192.168.1.15'
    params = {sentencia[0:3]:sentencia[-1]}
    requests.get(url = URL,params=params)


def beginClass (user,lock):
    entries = Control.objects.get()
    pass

def EndClass ():
    pass


#@login_required(login_url="/login/")
def index(request):
    return render(request, "index.html")

def locksView(request):
    i = Locks.objects.all()
    context = {'locks':i}
    
    for i in request.GET:
        accion(i)
    return render(request, "pages/locks.html",context)

def controlView(request):
    entries = Locks.objects.all()
    context = {'elements':entries}
    
    return render(request, "pages/control.html",context)

def registroView(request):
    context = {}
    
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