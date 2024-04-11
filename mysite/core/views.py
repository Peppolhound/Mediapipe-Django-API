from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy

from .forms import  ImageForm

import urllib
import numpy as np
from script.hand_image_detector import hand_detection
import cv2

from mysite.camera import VideoCamera, gen
from django.http import StreamingHttpResponse, HttpResponse


class Home(TemplateView):
    template_name = 'home.html'
    
def image_upload_view(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if request.FILES.get("image", None) is not None:
            uploaded_file = request.FILES.get("image")
            print(uploaded_file.name)
            annotated_image = hand_detection(uploaded_file.name)
            form.save()
            img_obj = form.instance
            # return render(request, 'image_upload.html', {'form': form, 'img_obj': img_obj})
            _, jpeg = cv2.imencode('.jpg', annotated_image)
            return HttpResponse(jpeg.tobytes(), content_type='image/jpeg')
    else:
        form = ImageForm()
    return render(request, 'image_upload.html', {'form': form})



def video_stream(request):
    vid = StreamingHttpResponse(gen(VideoCamera(), False), 
    content_type='multipart/x-mixed-replace; boundary=frame')
    return vid

def video_save(request):
    vid = StreamingHttpResponse(gen(VideoCamera(), True), 
    content_type='multipart/x-mixed-replace; boundary=frame')
    return vid

def video_input(request):
    return render(request, 'video_input.html')