import requests
import json

# Replace these with actual values
YOUR_SITE_URL = "https://your-site-url.com"
YOUR_APP_NAME = "YourAppName"
API_KEY = "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"  # Replace with your actual API key
MODEL_NAME = "mistralai/mistral-7b-instruct"  # The chat model you want to use

# Initialize an empty chat template and an instructions variable
chat_template = []
instructions = "You are interviewing for a software developer position, Your personality, attitude, and language should simulate an interviewer, you have asked following questions please continue interview by asking only one question based on following questions you asked and answers you got ask only one next question if there is no question below start interview by asking first question start interview with introduction if user is answering unapropriate answers or missbehaves then stop the interview and say get out to candidate.please starts with the introduce your self question for any converstaion."

def clear_chat_history():
    # Clear the chat history while retaining instructions
    global chat_template
    chat_template = []
    
def function(prompt):
    
    # Ask the user for input
    user_input = prompt

    # Append the user's message to the chat template
    chat_template.append({"role": "user", "content": user_input})

    if user_input.lower() == "clear chat":
        clear_chat_history()
        print("Chat history cleared.")
            # Skip the rest of the loop

    # Add any instructions to the instructions variable (won't be summarized)
    # For example, if you have instructions in a text file, you can read and append them here.
    # instructions = "Some instructions for the user."

    # Summarize the conversation so far
    conversation_summary = "\n".join(msg["content"] for msg in chat_template)

    # Send the conversation summary as a prompt to the chatbot along with instructions
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "HTTP-Referer": YOUR_SITE_URL,
            "X-Title": YOUR_APP_NAME,
            "Authorization": f"Bearer {API_KEY}"
        },
        json={
            "model": MODEL_NAME,
            "messages": [
                {"role": "user", "content": instructions},  # Include instructions
                {"role": "user", "content": conversation_summary}  # Include summarized conversation
            ]
        }
    )

    # Check if the request was successful
    if response.status_code == 200:
        data = json.loads(response.content)
        # Extract the AI's response text
        ai_response = data['choices'][0]['message']['content']
        print(f"AI: {ai_response}")
        # Append the AI's message to the chat template
        chat_template.append({"role": "assistant", "content": ai_response})
        CHUNK_SIZE = 1024
        url = "https://api.elevenlabs.io/v1/text-to-speech/Yko7PKHZNXotIFUBG7I9/stream"

        headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": "10fbb73c3a2da8ae8439b8a8d0e87dba"
        }

        data = {
        "text": ai_response,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.6,
            "similarity_boost": 0.5
        }
        }

        response = requests.post(url, json=data, headers=headers, stream=True)

        with open('static/audio/output.mp3', 'wb') as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)
        return str(ai_response)
    else:
        # Print an error message if the request was not successful
        print(f"Request failed with status code: {response.status_code}")
        print(response.text)
        
