# Literature Review Helper
An automated tool for academic literature review that helps researchers gather, analyze, and summarize scholarly articles efficiently.

## 🎯 Features

- 🔍 Automated article search through Google Scholar
- 📑 Full-text extraction from academic papers

  
- 🤖 AI-powered article summarization -- Menna

#AI
from openai import OpenAI

# Install the OpenAI SDK first: pip install openai
from openai import OpenAI

import requests
import json
import os

openai_api_key = 'API CODE HERE'

if openai_api_key is None:
    raise ValueError("OpenAI API key is not set in environment variables.")

url = "https://api.openai.com/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openai_api_key}"
}

data = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "write a summary about tipping behavior"
        }
    ]
}

response = requests.post(url, headers=headers, json=data)


# Check if the request was successful
if response.status_code == 200:
    print("Response from OpenAI:", response.json())
    print('\n')
    print(response.json()['choices'][0]['message']['content'])
else:
    print("Error:", response.status_code, response.text)



#output from the code: 
#Response from OpenAI: {'id': 'chatcmpl-B2S22oM1e8ObWUwE9TjNxDkAcokAq', 'object': 'chat.completion', 'created': 1739924110, 'model': 'gpt-3.5-turbo-0125', 'choices': [{'index': 0, 'message': {'role': 'assistant', 'content': 'Tipping behavior varies across cultures, industries, and individual preferences. Tipping is commonly practiced in service industries such as restaurants, hotels, and taxis as a way to show appreciation for good service. The amount and expectations for tipping can differ widely, with some countries having established customs while others do not practice tipping at all. Tipping etiquette can be influenced by factors such as local customs, economic considerations, and personal experiences. Additionally, the rise of technology and mobile payment options has led to new ways to tip service providers. In general, tipping behavior is a complex and nuanced aspect of social interaction that can reflect cultural norms, individual values, and societal expectations.', 'refusal': None}, 'logprobs': None, 'finish_reason': 'stop'}], 'usage': {'prompt_tokens': 23, 'completion_tokens': 132, 'total_tokens': 155, 'prompt_tokens_details': {'cached_tokens': 0, 'audio_tokens': 0}, 'completion_tokens_details': {'reasoning_tokens': 0, 'audio_tokens': 0, 'accepted_prediction_tokens': 0, 'rejected_prediction_tokens': 0}}, 'service_tier': 'default', 'system_fingerprint': None}

#'''Tipping behavior varies across cultures, industries, and individual preferences. 
Tipping is commonly practiced in service industries such as restaurants, hotels, and 
taxis as a way to show appreciation for good service. The amount and expectations for 
tipping can differ widely, with some countries having established customs while others do 
not practice tipping at all. Tipping etiquette can be influenced by factors such as local 
customs, economic considerations, and personal experiences. Additionally, the rise of 
technology and mobile payment options has led to new ways to tip service providers. 
In general, tipping behavior is a complex and nuanced aspect of social interaction 
that can reflect cultural norms, individual values, and societal expectations'''.


- 📊 Interactive Streamlit web interface
- 📥 Exportable results in CSV format
