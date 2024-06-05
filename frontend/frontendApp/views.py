import requests
import openai
import os
from django.shortcuts import render
from django.http import JsonResponse

openai.api_key = os.getenv('OPENAI_API_KEY')

def index(request):
    return render(request, 'index.html', {})

def chat(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            # Send user message to Rasa
            rasa_responses = send_to_rasa(message)
            
            # Generate OpenAI response based on Rasa responses
            openai_response = generate_openai_response(rasa_responses)
            
            # Return the OpenAI response
            return JsonResponse(openai_response)
    
    # Return an error response if the request method is not POST
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def send_to_rasa(message):
    # Rasa server URL
    rasa_url = 'http://localhost:5005/webhooks/rest/webhook'
    
    # Headers for the request
    headers = {'Content-Type': 'application/json'}
    
    # Data to be sent to the Rasa server
    data = {'sender': 'user', 'message': message}
    
    try:
        # Send the POST request to the Rasa server
        response = requests.post(rasa_url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        error_message = f"Failed to get response from Rasa server: {e}"
        return {'error': error_message}

def generate_openai_response(rasa_responses):
    try:
        # Construct the prompt based on Rasa responses
        prompt = "User: " + rasa_responses[0]['text'] + "\nBot:"
        
        # Call OpenAI API to generate response
        openai_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=600,
            temperature=0.1
        )
        
        return {'text': openai_response.choices[0]['text']}
    except Exception as e:
        error_message = f"Failed to generate response from OpenAI: {e}"
        return {'error': error_message}
