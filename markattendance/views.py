from django.shortcuts import render
from django.http import HttpResponse
import cv2
import face_recognition
import pickle
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import numpy as np
import urllib
import json
import pymongo
import jsons
from datetime import datetime

# from imagetodat.settings import SECRET_KEY

# SECRET_KEY = 'django-insecure--z3#gzn=#311x%^5y6^#@nxr6*q=qgxr_@#)4ec46_wac=s(!0'

client=pymongo.MongoClient("mongodb://localhost:27017/")



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
 
	return image











def ver(request):
    if request.method=="POST":
        rawimage=_grab_image(stream=request.FILES["image"])
        curr_course=request.POST.get('course')
        db=client.FaceData
        collection=db[curr_course]
        

       

        now = datetime.now()
        year=now.strftime("%Y")
        month=now.strftime("%m")
        day=now.strftime("%d")
        date=year+'-'+month+'-'+day
        
        db2=client.attendance
        collection2=db2[date]

        total=item.objects.all()
        known_face_encodings=[]
        known_face_names = []
        known_face_roll=[]
        for document in collection.find():
            a=document.get('name')
            known_face_names.append(a)
            b=document.get('data')
            encoding=pickle.loads(b)
            c=document.get('roll')
            known_face_roll.append(c)
            known_face_encodings.append(encoding)

        all_face_locations = face_recognition.face_locations(rawimage,model='hog')
        all_face_encodings=face_recognition.face_encodings(rawimage,all_face_locations)
        for current_face_location, current_face_encoding in zip(all_face_locations,all_face_encodings):
                all_matches=face_recognition.compare_faces(known_face_encodings,current_face_encoding)
                name_of_person='Unknown face'
                if True in all_matches:
                    first_match_index=all_matches.index(True)
                    name_of_person = known_face_names[first_match_index]
                    my_dict = {"name": name_of_person,
                                "roll": known_face_roll[first_match_index],
                                "course":curr_course,}
        
                    collection2.insert_one(my_dict)
                    return render(request,'result.html',{'name':name_of_person})

            

    return render(request,'verify.html')


