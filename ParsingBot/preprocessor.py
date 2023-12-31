import pandas as pd

from googletrans import Translator


def translate_text(text: str, dest='en') -> str:
    try:
        translator = Translator()
        return translator.translate(text, dest=dest).text
    except:
        return text
    

def preprocess_csv(csv_file_path: str) -> str:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Translate every row to english
    df['message'] = df['message'].apply(translate_text)
    
    # Check if there is reply to message
    df['is_reply_to'] = df['reply_to'].str.strip().str.len() == 0
    
    # Concatenate text by row
    df['ConcatText'] = df.apply(lambda row: row['sender'] + ": " + row['message'] + 
                                (" Replied to: " + row['reply_to'] if row['is_reply_to'] else ""), axis=1)

    # Concatenate all text from the column
    concatenated_text = df['ConcatText'].str.cat(sep=' ')
    
    return concatenated_text
