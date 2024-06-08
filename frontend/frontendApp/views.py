import requests
import openai
import os
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


openai.api_key = os.getenv('OPENAI_API_KEY')

def index(request):
    return render(request, 'index.html', {})

@csrf_exempt
def chat(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            # Send user message to Rasa
            rasa_responses = send_to_rasa(message)
            print("Rasa Responses:", rasa_responses)

            # Generate OpenAI response based on Rasa responses
            openai_response = generate_openai_response(rasa_responses)
            print("OpenAI Response:", openai_response)

            # Return the OpenAI response to the user
            return JsonResponse(openai_response)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def send_to_rasa(message):
    rasa_url = 'http://localhost:5005/webhooks/rest/webhook'
    headers = {'Content-Type': 'application/json'}
    data = {'sender': 'user', 'message': message}

    try:
        response = requests.post(rasa_url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        error_message = f"Failed to get response from Rasa server: {e}"
        return [{'recipient_id': 'user', 'text': error_message}]

def generate_openai_response(rasa_responses):
    try:
        bot_response = ""
        for response in rasa_responses:
            if 'text' in response:
                bot_response = response['text']
                break

        if not bot_response:
            return {'error': 'No valid response from Rasa'}

        print("Original Rasa Response:", bot_response)

        openai_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Rephrase the following response to make it more human-like while retaining the original content."},
                {"role": "user", "content": bot_response}
            ],
            max_tokens=150,
            temperature=0.5
        )

        rephrased_response = openai_response.choices[0].message['content'].strip()
        print("Rephrased OpenAI Response:", rephrased_response)

        return {'text': rephrased_response}
    except Exception as e:
        error_message = f"Failed to generate response from OpenAI: {e}"
        return {'error': error_message}