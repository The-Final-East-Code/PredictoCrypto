# import os
# import tiktoken
# import pandas as pd
import time
from django.conf import settings
from openai import OpenAI
from typing_extensions import override


api_key = getattr(settings, 'OPENAI_API_KEY', None)
client = OpenAI(api_key=api_key)

def chat(user_message):
    assistant_id = 'asst_BZclSbXKUAWEjO2SEAzDWE43'
    thread = client.beta.threads.create()

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="I need to solve the equation `3x + 11 = 14`. Can you help me?"
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
        instructions="Please thoroughly analyze the user's message for a detailed response."
    )

    while run.status in ['queued', 'in_progress', 'cancelling']:
        time.sleep(1) # Wait for 1 second
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
    )

    if run.status == 'completed': 
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        return messages
    else:
        return(run.status)