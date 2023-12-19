import os
import pandas as pd

# Function to save data to a CSV file
def save_to_csv(data: pd.DataFrame, filename: str) -> None:
    # Load the existing data
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        df.loc[len(df)] = data[0]  # Add the new row at the end
    else:
        df = pd.DataFrame(data, columns=['message', 'sender', 'time', 'reply_to'])

    # If there are more than 1000 rows, remove the oldest ones
    if len(df) > 1000:
        df = df.tail(1000)  # Keep only the last 1000 rows

    # Save the data back to the CSV file
    df.to_csv(filename, index=False)