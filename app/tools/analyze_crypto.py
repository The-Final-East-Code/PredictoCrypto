import os
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from django.conf import settings
from django.http import HttpResponse
from django.utils.timezone import now
from datetime import datetime
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import io

def summarize_data(file):
    # Load the CSV file
    df = pd.read_csv(file)

    # Ensure the 'Date' column is parsed as datetime format
    df['Date'] = pd.to_datetime(df['Date'])

    # Set the 'Date' column as the index
    df.set_index('Date', inplace=True)

    # Basic statistics for numerical columns (High, Low, Open, Close, Volume, Marketcap)
    basic_stats = df[['High', 'Low', 'Open', 'Close', 'Volume', 'Marketcap']].describe()

    # Missing value analysis
    missing_values = df[['High', 'Low', 'Open', 'Close', 'Volume', 'Marketcap']].isnull().sum()

    # Calculating rolling averages for the 'Close' price (7-day and 30-day)
    df['7_day_rolling_avg_close'] = df['Close'].rolling(window=7).mean()
    df['30_day_rolling_avg_close'] = df['Close'].rolling(window=30).mean()

    # Identify days with significant volume changes
    volume_mean = df['Volume'].mean()
    volume_std = df['Volume'].std()
    significant_volume_changes = df[df['Volume'] > volume_mean + 2 * volume_std]

    # Identify days with significant market cap changes
    marketcap_mean = df['Marketcap'].mean()
    marketcap_std = df['Marketcap'].std()
    significant_marketcap_changes = df[df['Marketcap'] > marketcap_mean + 2 * marketcap_std]

    # Combine all the analyses into a textual summary
    summary = f"Basic Statistics:\n{basic_stats}\n\n" \
              f"Missing Values:\n{missing_values}\n\n" \
              f"Significant Volume Changes:\n{significant_volume_changes[['Volume']]}\n\n" \
              f"Significant Marketcap Changes:\n{significant_marketcap_changes[['Marketcap']]}\n\n" \
              f"7-Day Rolling Avg Close:\n{df['7_day_rolling_avg_close'].dropna().to_string()}\n\n" \
              f"30-Day Rolling Avg Close:\n{df['30_day_rolling_avg_close'].dropna().to_string()}\n"

    # Generate the filename with the current date
    prompts_dir = os.path.join(settings.BASE_DIR, 'assets', 'prompts')
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"data_summary_{date_str}.txt"
    filepath = os.path.join(prompts_dir, filename)

    # Save the summary to a file
    with open(filepath, 'w') as f:
        f.write(summary)

    return summary


def call_cgpt_api(content):
        url = "https://api.openai.com/v1/chat/completions"
        api_key = os.getenv('CGPT_API')
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "model": "text-embedding-3-large",
            "messages": [
                {
                    "role": "system",
                    "content": f"Analyze the following CSV data and provide insights: {content}"
                },
                {
                    "role": "user",
                    "content": content
                }
            ],
            "max_tokens": 1024,
        }
        response = requests.post(url, json=data, headers=headers)
        response_data = response.json()

        # Generate a unique filename for the chats
        timestamp = now().strftime('%Y%m%d%H%M%S')
        filename = f"chat_{timestamp}.json"
        prompts_dir = os.path.join(settings.BASE_DIR, 'assets', 'prompts')
        filepath = os.path.join(prompts_dir, filename)
        # Save the response to a JSON file
        with open(filepath, 'w') as outfile:
            json.dump(response_data, outfile)
        
        return response


def plot_graph(file):
    data = pd.read_csv(file)

    target = data["Close"]
    features = data[["Open", "High", "Low", "Volume"]]

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2)

    model = LinearRegression()

    # Train the model on the training data
    model.fit(X_train, y_train)

    # Make predictions on the testing data
    predictions = model.predict(X_test)

    # Create a figure object to eventually return
    fig, axs = plt.subplots(2, 2, figsize=(10, 8))
    
    axs[0, 0].scatter(data["Open"], target)
    axs[0, 0].set_xlabel("Opening Price")
    axs[0, 0].set_ylabel("Closing Price")
    axs[0, 0].set_title("Opening Price vs Closing Price")

    axs[0, 1].scatter(data["High"], target)
    axs[0, 1].set_xlabel("Highest Price")
    axs[0, 1].set_ylabel("Closing Price")
    axs[0, 1].set_title("Highest Price vs Closing Price")

    axs[1, 0].scatter(data["Low"], target)
    axs[1, 0].set_xlabel("Lowest Price")
    axs[1, 0].set_ylabel("Closing Price")
    axs[1, 0].set_title("Lowest Price vs Closing Price")

    axs[1, 1].scatter(data["Volume"], target)
    axs[1, 1].set_xlabel("Trading Volume")
    axs[1, 1].set_ylabel("Closing Price")
    axs[1, 1].set_title("Trading Volume vs Closing Price")

    # Second plot for market volume difference
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    ax2.scatter(X_test["Volume"], predictions - y_test, color='orange', marker='x')
    ax2.set_xlabel("Trading Volume (Predicted)")
    ax2.set_ylabel("Price (Predicted) - Price (Actual)")
    ax2.set_title("Trading Volume (Predicted) vs Price (Predicted) - Price (Actual)")

    # Instead of plt.show(), you would return 
    # the figure object in a Django view
    return fig, fig2
