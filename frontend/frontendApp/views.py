from django.shortcuts import render
from django.http import JsonResponse
import requests

def index(request):
    return render(request, 'index.html', {})

def chat(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            # Define the URL of the Rasa server
            rasa_url = 'http://localhost:5005/webhooks/rest/webhook'
            
            # Define the headers for the request
            headers = {'Content-Type': 'application/json'}
            
            # Define the data to be sent to the Rasa server
            data = {'sender': 'user', 'message': message}
            
            try:
                # Send the POST request to the Rasa server via a proxy
                response = requests.post(rasa_url, headers=headers, json=data)
                
                # Check if the request was successful
                response.raise_for_status()
                
                # Parse the JSON response from the Rasa server
                bot_responses = response.json()
                
                # Return the bot responses as a JSON response
                return JsonResponse(bot_responses, safe=False)
                
            except requests.exceptions.RequestException as e:
                # Handle any exceptions that occur during the request
                error_message = f"Failed to get response from Rasa server: {e}"
                return JsonResponse({'error': error_message}, status=500)
    
    # Return an error response if the request method is not POST
    return JsonResponse({'error': 'Invalid request method'}, status=400)
