
from fastapi import FastAPI, UploadFile, File
import pandas as pd
import re

myapp = FastAPI()

@myapp.post("/analyze")
async def analyze_chat(chat_file: UploadFile = File(...)):
    # Read the uploaded chat file as a DataFrame
    chat_df = pd.read_csv(chat_file.file, header=None, names=["Message"])
    
    # Extract the date, time, sender, and message from each row in the DataFrame
    chat_df[["Date", "Time", "Message_Info"]] = chat_df["Message"].str.split(" - ", n=2, expand=True)
    chat_df[["Sender", "Message"]] = chat_df["Message_Info"].str.split(": ", n=1, expand=True)
    
    # Clean the message column by removing unnecessary characters and converting to lowercase
    chat_df["Message"] = chat_df["Message"].apply(lambda x: re.sub(r"[^a-zA-Z0-9 ]", "", x).lower())
    
    # Perform analysis on the cleaned chat data
    sender_count = chat_df["Sender"].value_counts().to_dict()
    word_count = chat_df["Message"].str.split(expand=True).stack().value_counts().to_dict()
    
    # Return the analysis as a JSON response
    return {"sender_count": sender_count, "word_count": word_count}
