from django.shortcuts import render
from django.http import JsonResponse
import requests
import os

RASA_SERVER_URL = "http://localhost:5005/webhooks/rest/webhook"

def index(request):
    return render(request, 'index.html')

def chat(request):
    if request.method == "POST":
        user_message = request.POST.get('message')
        response = requests.post(RASA_SERVER_URL, json={"message": user_message})
        bot_response = response.json()
        return JsonResponse({"response": bot_response})
