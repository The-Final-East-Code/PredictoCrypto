import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import io

def plot_graph(file):
    # Assuming 'file' is a file-like object (e.g., uploaded file in Django)
    # No need to change how pandas reads the csv data
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

    # Instead of plt.show(), you would return the figure object in a Django view
    return fig, fig2  # Return both figure objects for use in Django response
