import openai
import os

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_openai_response(message):
    try:
        # Call OpenAI API to generate response
        openai_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ],
            max_tokens=50,
            temperature=0.1
        )
        
        return {'text': openai_response.choices[0]['message']['content'].strip()}
    except Exception as e:
        print("OpenAI Error:", e)  # Print the error message
        return {'error': str(e)}

# Test the OpenAI integration
def test_openai_integration():
    # Get user input
    message = input("Enter your message: ")

    # Generate OpenAI response based on the message
    openai_response = generate_openai_response(message)
    print("OpenAI Response:", openai_response)  # Print OpenAI response

# Example usage
if __name__ == "__main__":
    test_openai_integration()
