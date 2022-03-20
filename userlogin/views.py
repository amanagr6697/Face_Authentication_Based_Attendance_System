from django.http import HttpResponse
from django.shortcuts import render, redirect
# from pytest import Instance
# from django.http import HttpResponse
# Create your views here.
from userlogin.forms import Myform, imageform
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
import cv2
import face_recognition
import pickle
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import numpy as np
import urllib
import json
from urllib.request import urlopen
import tempfile
from binascii import a2b_base64
import datetime
import time
def home(request):
    return render(request, 'home.html')

def remove(name):
  yo=""
  for i in range(len(name)):
      if (name[i]=='-' or name[i]==' ' or name[i]==':'):
       pass
      else:
       yo+=str(name[i])
  return yo

def _grab_image(path=None, stream=None, url=None):
    if path is not None:
        image = cv2.imread(path)
    else:
        if url is not None:
            resp = urllib.urlopen(url)
            data = resp.read()
        elif stream is not None:
            data = stream.read()
        image = np.asarray(bytearray(data), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    print(image)
    return image


@login_required(login_url='login')
def profile(request):
    return render(request, 'profile.html')


@login_required(login_url='login')
def upload_comp(request):
    if request.method == 'POST':
        form = imageform(request.POST, request.FILES)
        # print(form)
        if form.is_valid():
            wait_for_now = form.save(commit=False)
            wait_for_now.user_map = request.user
            # print(type(request.FILES["pic"]))
            rawimage = _grab_image(stream=request.FILES["pic"])
            try:
            #  encodings = face_recognition.face_encodings(rawimage)[0]
             encodings = face_recognition.face_encodings(rawimage)[0]
             wait_for_now.facedata = encodings
             wait_for_now.save()
             messages.success(request, f'Your image was uploaded.')
            #  webcam.facedata = encodings
            #  webcam.save()
            except:
             messages.warning(request, f'Image not detected. Try again')
    else:
        form = imageform()
    return render(request, 'upload_comp.html', {'form': form})


@login_required(login_url='login')
def upload_webcam(request):
    if request.method == 'POST':
        # print(form)
        
      aman = request.POST.get('data')
    #   cur=time.time()
      cur=datetime.datetime.now()
      cur=remove(str(cur))
      response = urllib.request.urlopen(aman)
      name="D:\javascript\Face_recog\learning\media\images\\"+cur
      filename="%s.jpg"%name
      with open(filename, 'wb') as f:
       f.write(response.file.read())
      webcam=image()
      yo="images/" + cur+".jpg"
      webcam.pic=yo
    #   print(type(f.read()))
    #   webcam.pic=f.read()
    #   print("mai ab thak gya aaaaaaaaaaaaaaaaaaaaa, continuous 9 hrssssssssssssssssssssssssssssssssssssssssssssssss")
    #   wait_for_now = form.save(commit=False)
      webcam.user_map = request.user
    #   yp
    #   rawimage = _grab_image(stream=webcam.pic)
      rawimage=face_recognition.load_image_file(filename)
    #   encodings = face_recognition.face_encodings(rawimage)[0]
    try:
     encodings = face_recognition.face_encodings(rawimage)[0]
     webcam.facedata = encodings
     webcam.save()
     messages.success(request, f'Your image was uploaded.')
    except:
     messages.warning(request, f'Face not captured. Try again')
    #  return redirect('/profile')
    else:
     print("subah nashta kar ke fir sounga")
    return render(request,'upload_webcam.html')
# @login_required(login_url='login')
# def upload_webcam(request):
#     path = request.POST["src"]
#     image = tempfile.NamedTemporaryFile()
#     image.write(urlopen(path).read())
#     image.flush()
#     image = File(image)
#     name = str(image.name).split('\\')[-1]
#     name += '.jpg'
#     image.name = name
#     obj = Image.objects.create(image=image)
#     obj.save()
    # if request.method == 'POST':
    #     form = imageform(request.POST, request.FILES)
    #     # print(form)
    #     if form.is_valid():
    #         wait_for_now = form.save(commit=False)
    #         wait_for_now.user_map = request.user
    #         rawimage=_grab_image(stream=request.FILES["pic"])
    #         encodings = face_recognition.face_encodings(rawimage)[0]
    #         wait_for_now.facedata = encodings
    #         wait_for_now.save()

    #         messages.success(request, f'Your image was uploaded.')
    # else:
    #     form = imageform()
    # return render(request, 'userlogin/upload_webcam.html', {'form': form})













@login_required(login_url='login')
def view(request):
    if request.method == 'GET':
        all = image.objects.filter(user_map=request.user)
    return render(request, 'view.html', {'images': all})


def register(request):
    if request.method == "POST":
        form = Myform(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Your {username} account was created successfully.')
        #   return redirect('login')
    else:
        form = Myform()
    return render(request, 'register.html', {
        'form': form
    })
# def profile(request):
#   return render(request,'userlogin/profile.html')
# def index(request):
#   return render(request,'userlogin/home.html')
# def index(request):
#   return render(request,'userlogin/home.html')
