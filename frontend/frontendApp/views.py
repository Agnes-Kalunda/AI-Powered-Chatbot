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
            rasa_data = send_to_rasa(message)
            print("Rasa Responses:", rasa_data)

            # Check if the intent is related to Agnes
            if is_agnes_related_intent(rasa_data):
                # Generate OpenAI response based on Rasa responses
                openai_response = generate_openai_response(rasa_data)
                print("OpenAI Response:", openai_response)
                return JsonResponse(openai_response)
            else:
                # Generate response directly from OpenAI
                openai_response = generate_direct_openai_response(message)
                print("Direct OpenAI Response:", openai_response)
                return JsonResponse(openai_response)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def send_to_rasa(message):
    rasa_url = 'http://localhost:5005/webhooks/rest/webhook'
    headers = {'Content-Type': 'application/json'}
    data = {'sender': 'user', 'message': message}

    try:
        response = requests.post(rasa_url, headers=headers, json=data)
        response.raise_for_status()
        rasa_data = response.json()
        print("Raw Rasa Data:", rasa_data)
        return {'message': message, 'responses': rasa_data}
    except requests.exceptions.RequestException as e:
        error_message = f"Failed to get response from Rasa server: {e}"
        return {'message': message, 'responses': [{'recipient_id': 'user', 'text': error_message}]}

def is_agnes_related_intent(rasa_data):
    agnes_intents = ['greet', 'ask_about_agnes', 'agnes_help']  # Define relevant intents here
    for response in rasa_data['responses']:
        if 'intent' in response:
            intent_name = response['intent'].get('name', '')
            if intent_name in agnes_intents:
                print("Agnes-related intent detected:", intent_name)
                return True
    print("No Agnes-related intent detected")
    return False

def generate_openai_response(rasa_data):
    try:
        bot_response = ""
        for response in rasa_data['responses']:
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
        print(error_message)
        return {'error': error_message}

def generate_direct_openai_response(message):
    try:
        openai_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI Assistant called AggieBot, created by Agnes to help with just programming tasks. Any  information regarding Agnes they can directly ask her Via +254 707606316."},
                {"role": "user", "content": message}
            ],
            max_tokens=150,
            temperature=0.5
        )

        direct_response = openai_response.choices[0].message['content'].strip()
        print("Direct OpenAI Response:", direct_response)

        return {'text': direct_response}
    except Exception as e:
        error_message = f"Failed to generate response from OpenAI: {e}"
        print(error_message)
        return {'error': error_message}
