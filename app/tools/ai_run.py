import os
import time
import json
from datetime import datetime
from django.conf import settings
from openai import OpenAI

client = OpenAI(api_key=getattr(settings, 'OPENAI_API_KEY', None))

def chat_with_openai(user_message):
    assistant_id = getattr(settings, 'AI_ASSISTANT_ID', None)
    try:
        thread = client.beta.threads.create()

        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_message
        )

        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id,
            instructions="You are a cryptocurrency data analysis chatbot. When presented with data, you will analyze the data and respond with valuable insights. Do not answer any questions that are not related to cryptocurrency. When asked about historical data, you will retrieve all the data available to you and respond with valuable insights. At the end of each run, generate a sample python code to retrieve the current thread messages and responses using the API."
        )

        while run.status in ['queued', 'in_progress', 'cancelling']:
            print(f"RUN STATUS: {run.status}")
            time.sleep(1)  # Wait for 1 second before checking the status again
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )

        if run.status == 'completed':
            prompts_dir = os.path.join(settings.BASE_DIR, 'assets', 'prompts')
            date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            filename = f"ai_asst_run{date_str}.txt"
            filepath = os.path.join(prompts_dir, filename)

            messages = client.beta.threads.messages.list(thread.id)
            response = str(messages.data[0].content[0].text.value)

            # with open(filepath, 'w') as f:
            #     f.writelines(response)

            return response
        else:
            print(f"RUN ERROR: {run.status}")
            return "Error: Run status is " + run.status
    except Exception as e:
        print(f"RUN ERROR: {run.status} | EXCEPTION: {e}")
        return "An error occurred: " + str(e)
