from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import StockSerializer
from django.http import HttpResponse, Http404
from .models import Post
import face_recognition
from PIL import Image
import requests
from io import BytesIO
import urllib.request

# this function parses a picture and loads it with facial recognition features 

def download_jpg (url, file_path, file_name):
    full_path = file_path + file_name + ".jpg"
    urllib.request.urlretrieve(url, full_path)

def image_parser (picture):
    image = face_recognition.load_image_file(picture)
    return image

def compare_picture (first_image, second_image):
    first_encoding = face_recognition.face_encodings(first_image)[0]
    second_encoding = face_recognition.face_encodings(second_image)[0]
    results = face_recognition.compare_faces([first_encoding], second_encoding)
    if results[0] == True:
        return True
    else:
        return False

# List all Post or create a new one
# recog

class RecogList(APIView):
    def get(self, requests):
        post = Post.objects.all()
        serializer = StockSerializer(post, many=True)
        return Response(serializer.data)

    def post(self, requests):
        download_jpg(requests.data["url"], "recog/images/", requests.data["name"])
        current = "recog/images/" + requests.data["name"] + ".jpg"
        compare = "recog/images/" + requests.data["compare"] + ".jpg"
        current_image = image_parser(current)
        comparison_image = image_parser(compare)
        results = compare_picture(current_image, comparison_image)
        result = {
            "results": results
        }
        return Response(result)

class CreateList(APIView):
    def post(self, requests):
        download_jpg(requests.data["url"], "recog/images/", requests.data["name"])
        result = {
            "results": "success"
        }
        return Response(result)

def home (request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'recog/home.html', context)

def about (request):
    return render(request, 'recog/about.html')

# Create your views here.
